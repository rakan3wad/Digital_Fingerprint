import requests

url = "https://api.salla.dev/admin/v2/orders"

payload = {
    "receiver": {
        "name": "Mohammed Ali",
        "country_code": "SA",
        "phone": "581893573",
        "country_prefix": "+966",
        "email": "Mohammed@test.test",
        "notify": True
    },
    "shipping_address": {
        "country_id": 566146469,
        "city_id": 2097610897,
        "block": "Om El 9823489237",
        "street_number": "jmoh El 8912749823764",
        "address": "building 124234324, floor 212423",
        "postal_code": "23874982374",
        "geocode": "21.4283792, 21.4283792"
    },
    "payment": {
        "status": "waiting",
        "accepted_methods": ["bank", "credit_card"]
    },
    "products": [
        {
            # "id": 227183668,
            "name": "كتيب تجريبي",
            "price": 25,
            "quantity": 1
        }
    ]
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer ory_at_X9nGY6XBVjHCEM3IfP0_DpBmE_WBiEHUBdq5eBLybMo.rWIWFmKiJGGwUGuUE0faR_IVA6b1-mB5uqb7zDV2rCc"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())