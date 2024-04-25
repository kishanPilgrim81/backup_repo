import requests
import json

import sys

from django.conf import settings
 
# # Data to be written
# dictionary = {
#     "name": "sathiyajith",
#     "rollno": 56,
#     "cgpa": 8.6,
#     "phonenumber": "9976770500"
# }
 
# # Serializing json
# json_object = json.dumps(dictionary, indent=4)
 
# # Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)

# sys.exit(0)


# Shopify API Key and Store URL
store_url = "https://" + settings.STAG_SHOP
access_token = settings.STAG_ACCESS_TOKEN

# API endpoint for fetching an Order
webhook_url = store_url + "/admin/api/2023-01/webhooks.json"

# Set headers
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": access_token
}

try:
    # Make the get Webhook API request
    webhook_data = requests.get(webhook_url, headers=headers)
    webhookJson = webhook_data.json()
    print(webhookJson)
except Exception as e:
    print(e.message)

# webhook_data = {
#     "webhook": {
#         "address": "https://gift.discoverpilgrim.com/polls/order_create_webhook",
#         "topic": "orders/create",
#         "format": "json"
#     }
# }
# print(webhook_data)

# try:
#     # Make the get Webhook API request
#     order_data = requests.post(webhook_url, headers=headers, data=json.dumps(webhook_data))
#     orderJson = order_data.json()
#     print(orderJson)
# except Exception as e:
#     print(e.message)