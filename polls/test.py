# import sys
import json
import requests

from django.conf import settings

# # from io import BytesIO
# from PIL import Image
# import io
# from bytesbufio import BytesBufferIO
# bytesbuf = BytesBufferIO()
# # from requests.structures import CaseInsensitiveDict

# store_url = settings.SHOP_URL
# access_token = settings.ACCESS_TOKEN

# headers = {
#     "Content-Type": "application/json",
#     "X-Shopify-Access-Token": access_token
# }

# # change img format to png
# imgUrl = "https://cdn.shopify.com/s/files/1/0620/1629/1045/files/icon.png?v=1678107896"
# imgResponse = requests.get(imgUrl)
# image = Image.open(bytesbuf(imgResponse))
# image.save("../static/profile-img/profile-image-3.png", format="PNG")

# customerId = 6926252343525

# customermetafield_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + "/metafields.json"
# image_metafield_id = ""
# try:
#     # Make the get Webhook API request
#     customermeta_data = requests.get(customermetafield_url, headers=headers)
#     customerMetaJson = customermeta_data.json()
#     # print(customerMetaJson)
#     metafields = customerMetaJson['metafields']
#     for metafield in metafields:
#         if metafield['key'] == "profile_image":
#             image_metafield_id = metafield['id']
# except Exception as e:
#     print(e)

# url = "https://gift.discoverpilgrim.com/static/profile-img/icon.png"
# #"https://cdn.shopify.com/s/files/1/0620/1629/1045/files/no-image.webp?v=1677743651"

# imgObj = {
#     "key": "profile_image",
#     "value": url,
#     "type": "url",
#     "namespace": "custom"
# }
# if(image_metafield_id):
#     imgObj["id"] = image_metafield_id

# customer_data = {
#     "customer": {
#         "id": customerId,
#         "metafields": [
#             imgObj,
#         ]
#     }
# }

# # API endpoint for updating a Customer
# customer_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + ".json"
# print(customer_data)

# try:
#     # Make the get Webhook API request
#     customer_data = requests.put(customer_url, headers=headers, data=json.dumps(customer_data))
#     customerJson = customer_data.json()
#     print(customerJson)
# except Exception as e:
#     print(e)



# url = "{settings.SHOP_URL}/admin/api/2023-01/graphql.json"
# STAGED_UPLOADS_CREATE = """
#   mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
#     stagedUploadsCreate(input: $input) {
#       stagedTargets {
#         resourceUrl
#         url
#         parameters {
#           name
#           value
#         }
#       }
#       userErrors {
#         field
#         message
#       }
#     }
#   }
# """

# COLLECTION_UPDATE = """
#   mutation collectionUpdate($input: CollectionInput!) {
#     collectionUpdate(input: $input) {
#       collection {
#         id
#         image {
#           originalSrc
#         }
#       }
#       userErrors {
#         field
#         message
#       }
#     }
#   }
# """



# query = """
# query {
#     customers(first: 5) {
#         edges {
#             node {
#                 id
#                 email
#             }
#         }
#     }
# }
# """
 
# try:
#     response = requests.post(url, data=query, headers=headers)
#     if response.status_code == 200:
#         result = response.json()
#         print(type(result))
#         print(result['data']['customers']['edges'][0]['node']['email'])
#     else:
#         print("error: ", response)
# except Exception as e:
#     print("Error: ", e)



# order deliver event test
# request_data = {
#     'waybill': '81125552141', 'status': 'Delivered', 'timestamp': '2023-02-07T18:09:00Z', 'location': 'SRM COLLEGE (MMC)', 'remark': 'SHIPMENT DELIVERED', 'clickpost_status_code': 8, 'clickpost_city': '', 'clickpost_status_description': 'Delivered', 'account_code': 'Vamaship1', 'cp_id': 21, 'rto_awb': None, 'additional': {'is_rvp': False, 'notification_event_id': 5, 'courier_partner_edd': None, 'order_id': '00030761872', 'latest_status': {'clickpost_status_code': 8, 'location': 'SRM COLLEGE (MMC)', 'clickpost_city': '', 'status': 'Delivered', 'clickpost_status_description': 'Delivered', 'clickpost_status_bucket': 6, 'clickpost_status_bucket_description': 'Delivered', 'timestamp': '2023-02-07T18:09:00Z', 'remark': 'SHIPMENT DELIVERED', 'reference_number': '4569960218853'}}
# }

# order_name = request_data['additional']['order_id']
# # print(order_name)

# # Shopify API Key and Store URL
# store_url = settings.SHOP_URL
# access_token = settings.ACCESS_TOKEN

# # API endpoint for creating a Gift Card
# order_url = store_url + "/admin/api/2023-01/orders.json?name="+order_name+"&status=any"

# # Set headers
# headers = {
#     "Content-Type": "application/json",
#     "X-Shopify-Access-Token": access_token
# }

# # Make the create Gift card API request
# try:
#     order_data = requests.get(order_url, headers=headers)
#     orderJson = order_data.json()
#     orderJson = orderJson['orders'][0]
#     # print(orderJson['id'])
# except Exception as e:
#     print(e.message)

# phone = orderJson['billing_address']['phone']
# phone = str(phone)
# phone = '+91'+phone

# order_id = orderJson['name']

# # print(phone,order_id)

# pid=''
# pname=''
# pquantity=''
# try:
#     print(orderJson["line_items"][0]["product_id"])
#     count = 0
#     for i in orderJson["line_items"]:
#         if count == 0:
#             pid=pid+str(i["product_id"])
#             pname=pname+str(i["title"])
#             pquantity=pquantity+str(i["quantity"])
#         else:
#             pid=pid+','+str(i["product_id"])
#             pname=pname+','+str(i["title"])
#             pquantity=pquantity+','+str(i["quantity"])
#         count = count + 1
#     #pid=tutorial_data["line_items"][0]["product_id"]
#     #pname=tutorial_data["line_items"][0]["title"]
#     #pquantity=tutorial_data["line_items"][0]["quantity"]
# except:
#     print('IN ORDERdelivered exception product section')
#     pass

# print("pid: " + pid)
# print("pname: " + pname)
# print("pquantity: " + pquantity)

# url = "https://api.webengage.com/v1/accounts/11b564785/events"

# headers = CaseInsensitiveDict()
# webengagekey=settings.WEBENGAGE
# headers["Authorization"] = "Bearer {}".format(webengagekey)
# headers["Content-Type"] = "application/json"

# data = {
#     "userId": phone,
#     "eventName": "Order Delivered",
#     "eventData": 
#     {
#         "orderID":order_id,
#         "orderGrandTotal":orderJson['total_price'],
#         "Product ID": pid,
#         "Quantity": pquantity,
#         "Product": pname
#     }
# }
# data=json.dumps(data)
# print(data)
# resp = requests.post(url, headers=headers, data=data)
# print(resp.text)

# sys.exit(0)


# how to join two values test
# # sender_email = 'saloni@discoverpilgrim.com'
# # attributes = [{'name': 'recipient_email', 'value': 'saloni.agrawal@growisto.com'}, {'name': 'recipient_name', 'value': 'Saloni'}, {'name': 'sender_name', 'value': 'DP'}, {'name': 'sender_email', 'value': 'saloni@discoverpilgrim.com'}, {'name': 'message', 'value': 'Congratulations!!'}]

# # for attributeArr in attributes:
# #     if attributeArr['name'] == "recipient_email":
# #         recipient_email = attributeArr['value']
# #     if attributeArr['name'] == "recipient_name":
# #         recipient_name = attributeArr['value']
# #     if attributeArr['name'] == "message":
# #         custom_message = attributeArr['value']

# # print(recipient_email,recipient_name,custom_message)

# # to_email = "".join([sender_email,",",recipient_email])

# # print(to_email,custom_message)

# # sys.exit(0)


# send email test
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# configure .env
# import sys
# from django.conf import settings
# settings.configure()

# from django.test.utils import setup_test_environment
# setup_test_environment()

# print(settings.WEBENGAGE)
# sendgridkey=settings.SENDGRID_API_KEY
# print(format(sendgridkey))
# sys.exit(0)

product_id = 8209166368997

# Shopify API Key and Store URL
store_url = settings.SHOP_URL
access_token = settings.ACCESS_TOKEN

# API endpoint for fetching a product image
product_url = store_url + "/admin/api/2023-01/products/" + str(product_id) + ".json?fields=image"

# Set headers
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": access_token
}

# Make the create Gift card API request
response = requests.get(product_url, headers=headers)

image_url = ""
# Check the response status code
if response.status_code == 200:
    productData = response.json()
    print("Product fetched successfully!")
    image_url = productData['product']['image']['src']
    # print(image_url)

recipient_name="Saloni"
customer_name="S"
initial_value="500.00"
code="hdke847jhw0wmdke"
sender_email = 'saloni@discoverpilgrim.com'
recipient_email = 'saloni.agrawal@growisto.com'
to_emails = [sender_email,recipient_email]
custom_message = "Test"

message = Mail(
    from_email='no-reply@discoverpilgrim.com',
    to_emails=to_emails,
    subject="""Staging Pilgrim Rs. """+initial_value+""" Gift Card""",
    html_content="""<table cellspacing="0" cellpadding="0" border="0" width="100%">
    <tbody>
        <tr>
            <td style="padding:20px 20px 40px" background="https://ci3.googleusercontent.com/proxy/Qs6ro6gSuqiqlOfgNiwKcKJ2F9-pTSxQ3Z91W5vmRrN4OdJZVSUHXBHdtv0hAQxtcvUiF9uPcMyfa4bdBsOlNdNL5eJyIqLuXHE=s0-d-e1-ft#http://media.giftbig.com/media/gb_email_images/wrap.png">
                <table border="0" style="width:800px;font-size:20px;color:#000000;font-family:Gautami,Helvetica,sans-serif" cellspacing="0" cellpadding="0" align="center">
                    <tbody><tr>
                            <td style="height:5px" colspan="2">
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:20px 20px 40px">
                                <table align="center" cellspacing="0" cellpadding="0" border="0">
                                    <tbody><tr>
                                            <td colspan="2" style="padding-left:10px;padding-right:10px" align="left">
                                                  <p style="text-align:justify;font-size:30px;line-height:24px;">
                                                Dear <strong>"""+recipient_name+"""</strong>,</p>
                                                <p style="text-align:left;font-size:20px;line-height:24px;">
                                                    You have been gifted a <strong>Pilgrim e-Gift card</strong> by """+customer_name+""". <br>
                                                    Enjoy skincare and hairare products made with the world’s best beauty ingredients!<br><br>
                                                    PS: To redeem the gift card, you will need the e-gift card number. Don’t forget to save the email or the number!
                                                </p><p style="text-align:left">
                                                    <strong>"""+customer_name+"""'s Message:</strong>: “"""+custom_message+""""
                                                </p><p style="text-align:justify"></p><p></p><p></p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="height:5px" colspan="2"></td>
                                        </tr>
                                        <tr>
                                            <td colspan="2">
                                                <table border="0" style="width:800px;font-size:12px;color:#000000;font-family:Gautami,Helvetica,sans-serif" cellspacing="0" cellpadding="0" align="center">
                                                    <tbody><tr>
                                                        <td width="1" style="background-color:#eceaeb"></td>
                                                        <td style="background-color:#ffffff;padding:10px;border-top:1px solid #eae9e9;border-right:1px solid #d4d2d3;border-bottom:1px solid #b2b1b1;border-left:1px solid #d4d2d3">
                                                            <table border="0" cellspacing="0" cellpadding="0" align="center">
                                                                <tbody><tr>
                                                                    <td colspan="2" style="border:1px solid #eaeaea"><img src="""+image_url+""" alt="" border="0" style="width:800px" class="CToWUd a6T" data-bit="iit" tabindex="0"><div class="a6S" dir="ltr" style="opacity: 0.01; left: 604px; top: 971.406px;"><div id=":143" class="T-I J-J5-Ji aQv T-I-ax7 L3 a5q" role="button" tabindex="0" aria-label="Download attachment " jslog="91252; u014N:cOuCgd,Kr2w4b,xr6bB" data-tooltip-class="a1V" data-tooltip="Download"><div class="akn"><div class="aSK J-J5-Ji aYr"></div></div></div></div></td>
                                                                </tr>
                                                                <tr>
                                                                    <td style="padding:10px" colspan="2">
                                                                        <table cellspacing="0" cellpadding="0" style="border-bottom:1px solid #eaeaea;font-size:12px;width:760px;text-align:center;color:#000000" border="0">
                                                                            <tbody><tr>
                                                                                <td style="font-weight:bold;border-right:1px solid #eaeaea;vertical-align:top;padding-right:15px;text-align:left" width="50%">
                                                                                    <p style="margin:0;padding:0 0 15px 0">
                                                                                        <span style="font-size:15px">Pilgrim e-Gift Card</span>
                                                                                    </p>
                                                                                </td>
                                                                                <td style="font-weight:bold;vertical-align:top;padding-left:15px;text-align:left" width="50%" rowspan="2">
                                                                                    <p style="margin:0;padding:0 0 10px 0">
                                                                                        <span style="font-size:30px">Rs. """+initial_value+"""</span>
                                                                                    </p>
                                                                                    <p style="margin:0;padding:0">
                                                                                        <span>
                                                                                            Can be Redeemed at <a href="https://discoverpilgrim.com/" rel="noreferrer noreferrer" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://discoverpilgrim.com/"> discoverpilgrim.com/</a>* <br>
                                                                                        </span>
                                                                                    </p>
                                                                                    <p style="font-weight:normal;margin:0;padding-top:5px">
                                                                                        * Conditions apply.
                                                                                    </p>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="border-right:1px solid #eaeaea;vertical-align:top;padding-right:15px;text-align:left;font-size:12px;color:#666666">
                                                                                    <table cellspacing="0" cellpadding="0" style="font-size:12px;text-align:left;color:#000000" border="0">
                                                                                    <tbody><tr>
                                                                                        <td style="padding-bottom:5px;border-right:1px solid #e6e6e6;padding-right:5px">
                                                                                            Card Number
                                                                                        </td>
                                                                                        <td style="font-size:24px;font-weight:normal;width:190px;border-left:1px solid #e6e6e6;padding-right:5px">
                                                                                          &nbsp;&nbsp;"""+code+"""
                                                                                        </td>
                                                                                    </tr>
                                                                                    </tbody></table>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="height:10px" colspan="2">
                                                                                </td>
                                                                            </tr>
                                                                        </tbody></table>
                                                                    </td>
                                                                </tr>
                                                            </tbody></table>
                                                        </td>
                                                        <td width="1" style="background-color:#eceaeb"></td>
                                                    </tr>
                                                    <tr>
                                                        <td width="1" style="background-color:#eceaeb"></td>
                                                        <td height="1" style="background-color:#d5d3d4"></td>
                                                        <td width="1" style="background-color:#eceaeb"></td>
                                                    </tr>
                                                    <tr>
                                                        <td width="1"></td>
                                                        <td height="1" style="background-color:#e8e6e7"></td>
                                                        <td width="1"></td>
                                                    </tr>
                                                </tbody></table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="padding:10px" colspan="2">
                                                <table cellspacing="0" cellpadding="0" style="font-size:18px;text-align:justify;color:#666666;width:800px" border="0">
                                                    <tbody><tr>
                                                        <td align="left">
                                                            <span style="font-weight:bold;font-size:30px;line-height:1.6">Terms &amp; Conditions</span>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="line-height:1.6">
                                                        <ul style="margin:0;padding:0">
                                                            • <span style="line-height:24px"> Pilgrim e-gift cards are valid only at <a href="https://discoverpilgrim.com/" rel="noreferrer noreferrer" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://discoverpilgrim.com/">discoverpilgrim.com</a> and expire <strong>3 months </strong>from receipt.<br>
                                                            • <span style="line-height:24px"> E-Gift Card validity cannot be extended under any circumstances.<br>
                                                            • <span style="line-height:24px"> E-Gift Card cannot be exchanged for cash. <br>
                                                            • <span style="line-height:24px"> E-Gift Card are non-refundable and cannot be canceled. <br>
                                                            • <span style="line-height:24px"> Redeemable during sales, promotions &amp; offers. <br>
                                                            • <span style="line-height:24px"> Any remaining balance can be used for future purchases.<br>
                                                            • <span style="line-height:24px"> In case the value of the order exceeds the value of the voucher, the difference shall be paid by the bearer.<br>
                                                            • <span style="line-height:24px"> Only valid on Online Payments.<br>
                                                            • <span style="line-height:24px"> E-gift card details shall only be communicated to the recipient via email.<br>
                                                            • <span style="line-height:24px"> Any offer/promotion running on the site is not applicable on purchase of E-Gift Cards.<br>
                                                            • <span style="line-height:24px"> Pilgrim has the final authority on the interpretation of these terms and conditions.<br>
                                                        </span></span></span></span></span></span></span></span></span></span></span></ul>
                                                        </td>
                                                    </tr>
                                                </tbody></table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#cccccc;padding:10px;width:200px">
                                            </td>
                                            <td align="right" style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:#cccccc;padding-right:10px">
                                                <b>  <a href="https://discoverpilgrim.com/" alt="Pilgrim Gift Card" title="Pilgrim Gift Card" border="0" rel="noreferrer noreferrer" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://discoverpilgrim.com/"> </a></b>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody></table>"""
)
try:
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)