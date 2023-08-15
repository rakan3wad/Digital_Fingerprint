import requests

url = "https://api.salla.dev/admin/v2/orders/statuses/status_id"

headers = {
    "Accept": "application/json",
    "Authorization": ""
}

response = requests.get(url, headers=headers)

print(response.json())