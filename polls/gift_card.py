import requests
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string    
import random # define the random module
import sys
import time
from django.conf import settings

sys.exit()

order_id = "5256916107559"
print(order_id)

time.sleep(3)

# Shopify API Key and Store URL
store_url = "https://{settings.STAG_SHOP}"
access_token = settings.STAG_ACCESS_TOKEN

# Set headers
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": access_token
}

# API endpoint for creating a Gift Card
gift_card_url = store_url + "/admin/api/2023-01/gift_cards.json"

# API endpoint for fetching location
location_url = store_url + "/admin/api/2023-01/locations.json"

order_url = store_url + "/admin/api/2023-01/orders/" + order_id + "/fulfillments.json"

# Make the create Gift card API request
order_fulfillment = requests.get(order_url, headers=headers)
print(order_fulfillment.json())
order_fulfillment_json = order_fulfillment.json()

gift_card_id = order_fulfillment_json['fulfillments'][0]['receipt']['gift_cards'][0]['id']
print(gift_card_id)

get_gift_card_url = store_url + "/admin/api/2023-01/gift_cards/" + str(gift_card_id) + "/disable.json"

disable_gc_data = {
    "gift_card": {
        "id": gift_card_id
    }
}
print(disable_gc_data)

# Make the create Gift card API request
diable_giftcard = requests.post(get_gift_card_url, headers=headers, data=json.dumps(disable_gc_data))
print(diable_giftcard.json())

sys.exit("Stop execution")

# Make the API request to get the location
get_location = requests.get(location_url, headers=headers)
locationJson = get_location.json()
locationId   = locationJson['locations'][1]['id'] #72976531751

orderfu_url = store_url + "/admin/api/2022-04/orders/5254961758503/fulfillments/4658926616871.json"

# Define the data for the fulfillment
fulfillmentu_data = {
    "fulfillment": {
        "location_id": locationId,
        "receipt": {
            "gift_cards": [{
                "id": 643856302375,
                "line_item_id": 13729345798439,
                "masked_code": "•••• •••• •••• ofw3"
            }]
        }
    }
}

# Make the API request to fulfill the order
fulfillment = requests.put(orderfu_url, headers=headers, json=fulfillmentu_data)
print(fulfillment)
print(fulfillment.json())

sys.exit(0)

randStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))
print(str(randStr))

# Gift Card details
code = str(randStr)
initial_value = 500.00
line_item_id = 13724829384999
order_id = 5253078876455
customer_id = 6786984083751
custom_message = "Test message."

# Data to be sent in the request body
gc_data = {
    "gift_card": {
        "note": custom_message,
        "code": code,
        "initial_value": initial_value,
        # "line_item_id": line_item_id,
        # "order_id": order_id,
        "customer_id": customer_id,
        "currency": "INR"
    }
}

# Make the API request
create_gift_card = requests.post(gift_card_url, headers=headers, data=json.dumps(gc_data))
# print(response.json())
gift_card_json = create_gift_card.json()

# Check the response status code
if create_gift_card.status_code == 201:
    print("Gift Coupon code created successfully!")
    gift_card_id = gift_card_json['gift_card']['id']
    gift_card_code = code[-4:]

    print(gift_card_id)

    # Make the API request to get the location
    get_location = requests.get(location_url, headers=headers)
    locationJson = get_location.json()
    locationId   = locationJson['locations'][1]['id'] #72976531751

    # API endpoint for creating a order fulfillment
    fulfillment_url = store_url + "/admin/api/2023-01/orders/" + str(order_id) + "/fulfillments.json"
    
    # Define the data for the fulfillment
    fulfillment_data = {
        "fulfillment": {
            # "order_id": order_id,
            "location_id": locationId,
            # "tracking_number": "asnbcjhxsb",
            # "send_receipt": False,
            # "notify_customer": False,
            "line_items": [
                {
                    "id": line_item_id,
                    "gift_card": True,
                    "fulfillment_service": "gift_card",
                    "fulfillment_status": "fulfilled",
                    "requires_shipping": False,
                }
            ],
            "receipt": {
                "gift_cards": [{
                    "id": gift_card_id,
                    "line_item_id": line_item_id,
                    "masked_code": "•••• •••• •••• " + gift_card_code
                }]
            },
            "service": "gift_card"
        }
    }
    print(fulfillment_data)

    # Make the API request to fulfill the order
    create_fulfillment = requests.post(fulfillment_url, headers=headers, json=fulfillment_data)
    print(create_fulfillment)

    # Check the response status code
    if create_fulfillment.status_code == 201:
        print("Fulfillment created successfully")
    else:
        print("Failed to create order fulfillment. Error:", create_fulfillment.text)
        
    # message = Mail(
    #     from_email='saloni@discoverpilgrim.com',
    #     to_emails='saloni.agrawal@growisto.com,test@mailinator.com',
    #     subject='Staging Pilgrim Gift Card',
    #     html_content="""<h3>Your gift card</h3><br />
    #     <p>Your Rs. 200 gift card for Staging Pilgrim is active. Keep this email or write down your gift card number.</p>
    #     <p>"""+custom_message+"""</p>
    #     <p>"""+code+"""</p>"""
    # )
    # try:
    #     sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    #     response = sg.send(message)
    #     print(response.status_code)
    #     # print(response.body)
    #     # print(response.headers)
    # except Exception as e:
    #     print(e.message)
else:
    print("Failed to create Gift Coupon code. Error:", create_gift_card.text)



# # API endpoint for fetching order fulfillment
# fulfillment_url = store_url + "/admin/api/2023-01/orders/"+order_id+"/fulfillment_orders.json?fulfillment[location_id]="+locationId

# # Make the API request to fulfill the order
# get_fulfillment = requests.get(fulfillment_url, headers=headers)
# fulfillmentJson = get_fulfillment.json()
# fulfillment_id  = fulfillmentJson['fulfillment_orders'][0]['id']
# fmline_item_id  = fulfillmentJson['fulfillment_orders'][0]['line_items'][0]['id']

# # API endpoint for creating a Gift Card
# orderf_url = store_url + "/admin/api/2023-01/fulfillments.json"

# # Define the data for the fulfillment
# fulfillment_data = {
#     "fulfillment": {
#         "line_items_by_fulfillment_order": [
#         {
#             "fulfillment_order_id": fulfillment_id,
#             "fulfillment_order_line_items": [
#             {
#                 "id": fmline_item_id,
#                 "quantity": "1"
#             }]
#         }],
#         "notify_customer": False
#         # "tracking_info": {
#         #     "number": "1562678",
#         #     "url": "https://www.my-shipping-company.com",
#         #     "company": "my-shipping-company"
#         # },
#         # "origin_address": None,
#         # "message": "The package was shipped this morning.",
#     }
# }

# # Make the API request to fulfill the order
# fulfillment = requests.post(orderf_url, headers=headers, json=fulfillment_data)
# print(fulfillment.json())

# # Check if the API request was successful
# if fulfillment.status_code == 201:
#     print("Order fulfillment created successfully.")
# else:
#     print("Error while fulfilling the order. Error: "+fulfillment.text)


# orderfu_url = store_url + "/admin/api/2023-01/orders/5254901301543/fulfillments/4658883559719.json"

# # Define the data for the fulfillment
# fulfillmentu_data = {
#     "fulfillment": {
#         "location_id": locationId,
#         "tracking_number": "74tbsfsdkj3",
#         "send_receipt": False
#     }
# }

# # Make the API request to fulfill the order
# fulfillment = requests.put(orderfu_url, headers=headers, json=fulfillmentu_data)
# print(fulfillment)