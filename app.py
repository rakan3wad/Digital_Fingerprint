from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session
import os
import json
import logging

from DataBase.DB_Salla_Orders import add_NewOrder_details
from DataBase.Db_Salla_Product import add_Product_details
from DataBase.DB_Salla_Customer import add_NewCustomer_details
from DataBase.DB_Salla_InstallApp import add_to_Salla_InstallApp,add_access_token,app_uninstalled,app_reinstalled

from grab_baseURL import grab_base_URL

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = os.urandom(24)


# auth_base_url = 'https://accounts.salla.sa/oauth2/authorize'
# token_url = 'https://accounts.salla.sa/oauth2/token'
# redirect_uri = 'https://saudi-bot.com/'
# # client_id = 'ada40be86e4ae02012cc00913707dbde'
# client_id = 'b453ebef-c62d-4bd2-b324-3af790ee1438'#saudi-bot
# # client_secret = '164e49e8130a4a380f607f738ccddb3e'
# client_secret = 'b5ebfd4b3062458a8e8eda82351111ed' #saudi-bot

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    event_details = request.json
    print(f"Webhook data: {json.dumps(event_details,indent=4,ensure_ascii=False)}")
    ###########################################################################

    event = json.dumps(event_details["event"]).replace('"', "")
    if "app.installed" in event:
        merchant_id = json.dumps(event_details["merchant"])
        installation_date = json.dumps(event_details["data"]["installation_date"])
        add_to_Salla_InstallApp(event, merchant_id , installation_date)
        app_reinstalled(merchant_id)
    if "app.store.authorize" in event:
        access_token = json.dumps(event_details["data"]["access_token"])
        merchant_id = json.dumps(event_details["merchant"])
        add_access_token(merchant_id, access_token)
    if "app.uninstalled" in event:
        merchant_id = json.dumps(event_details["merchant"])
        app_uninstalled(merchant_id)

    ###########################################################################

    if "order.created" in event:
        merchant_id = json.dumps(event_details["merchant"])
        created_at = json.dumps(event_details["created_at"]).replace('"', "")
        order_id = json.dumps(event_details["data"]["id"])
        source_device = json.dumps(event_details["data"]["source_device"]).replace('"', "")
        order_status_id = json.dumps(event_details["data"]["status"]["id"])
        order_status_name = json.dumps(event_details["data"]["status"]["name"], ensure_ascii=False).replace('"', "")
        payment_method = json.dumps(event_details["data"]["payment_method"]).replace('"', "")
        currency = json.dumps(event_details["data"]["currency"]).replace('"', "")
        price = json.dumps(event_details["data"]["amounts"]["sub_total"]["amount"])
        try:
            discounts = json.dumps(event_details["data"]["amounts"]["discounts"][0]["code"], ensure_ascii=False).replace('"', "")
        except:
            discounts = "-"

        final_price = json.dumps(event_details["data"]["amounts"]["total"]["amount"])
        # total = json.dumps(event_details["data"]["items"][0]["amounts"]["total"]["amount"])

        add_NewOrder_details(event,created_at[:-9], merchant_id, order_id, source_device, order_status_id, order_status_name, payment_method, currency,price, discounts, final_price)

    ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###

        customer_id = json.dumps(event_details["data"]["customer"]["id"])
        customer_first_name = json.dumps(event_details["data"]["customer"]["first_name"], ensure_ascii=False).replace('"', "")
        customer_last_name = json.dumps(event_details["data"]["customer"]["last_name"], ensure_ascii=False).replace('"', "")
        customer_phone_code = json.dumps(event_details["data"]["customer"]["mobile_code"]).replace('"', "")
        customer_phone_number = json.dumps(event_details["data"]["customer"]["mobile"])
        customer_email = json.dumps(event_details["data"]["customer"]["email"]).replace('"', "")
        customer_gender = json.dumps(event_details["data"]["customer"]["gender"]).replace('"', "")

        if (event_details.get("data") and
                event_details["data"].get("customer") and
                event_details["data"]["customer"].get("birthday") and
                "date" in event_details["data"]["customer"]["birthday"]):
            # process the date
            customer_birthday = json.dumps(event_details["data"]["customer"]["birthday"]["date"]).replace('"', "")
        else:
            customer_birthday=""

        customer_city = json.dumps(event_details["data"]["customer"]["city"], ensure_ascii=False).replace('"', "")
        customer_country = json.dumps(event_details["data"]["customer"]["country"], ensure_ascii=False).replace('"', "")

        add_NewCustomer_details(customer_id, customer_first_name, customer_last_name,customer_phone_code+customer_phone_number, customer_email, customer_gender, customer_birthday[:-16], customer_city, customer_country)

    ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###   ###

        product_id = json.dumps(event_details["data"]["items"][0]["product"]["id"])
        product_name = json.dumps(event_details["data"]["items"][0]["product"]["name"], ensure_ascii=False).replace('"', "")
        is_available = json.dumps(event_details["data"]["items"][0]["product"]["is_available"], ensure_ascii=False).replace('"', "")
        product_price = json.dumps(event_details["data"]["items"][0]["product"]["price"]["amount"])
        product_URL_page = json.dumps(event_details["data"]["items"][0]["product"]["url"], ensure_ascii=False).replace('"', "")
        PDF_download_link = json.dumps(event_details["data"]["items"][0]["files"][0]["url"], ensure_ascii=False).replace('"', "")
        store_link = grab_base_URL(product_URL_page)

        add_Product_details(product_id, product_name, is_available, product_price, product_URL_page,PDF_download_link, store_link)

    ###########################################################################

    # Handle the incoming data here.
    if "id" in event_details:
        event_details = request.json
        logging.info(f"Entered /webhook with data: {event_details}")

    if "access_token" in event_details:
        store_access_token = request.json
        store_id = event_details["data"]["id"]
        add_to_Salla_InstallApp(store_id, store_access_token)
        logging.info(f"Received access token: {store_access_token}")

    return "Webhook data processed successfully!"


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # If the code is not in the request args, start the OAuth2 flow.
    if 'code' not in request.args:
        salla = OAuth2Session(client_id, redirect_uri=redirect_uri)
        authorization_url, state = salla.authorization_url(auth_base_url)
        session['oauth_state'] = state
        return redirect(authorization_url)

    # Exchange the authorization code for an access token.
    salla = OAuth2Session(client_id, state=session['oauth_state'])
    token = salla.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url
    )
    logging.info(f"Received token: {token}")

    # Merchant Details
    user_info = salla.get('https://accounts.salla.sa/oauth2/user/info').json()
    logging.info(f"User Info: {user_info}")

    # Fetch data from authenticated APIs
    headers = {'Authorization': f'Bearer {token["access_token"]}'}
    orders = salla.get('https://api.salla.dev/admin/v2/orders', headers=headers).json()
    logging.info(f"Received orders: {orders}")

    return 'OAuth process complete.'

if __name__ == '__main__':
    app.run(debug=True)
