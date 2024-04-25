from django.shortcuts import render
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
from django.http import HttpResponse


import os
import requests
from requests.structures import CaseInsensitiveDict
import json
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from django.conf import settings

from requests.structures import CaseInsensitiveDict

from .models import Order
from .models import OrderDeliver
from .models import Pincode
from .models import CustomerReview
from .models import TruecallerCustomer

# saloni staging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import string
import random
import time
from django.http import JsonResponse
from .forms import ImageFileUploadForm
from .multipass import ShopifyMultipass

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# saloni live
@api_view(['GET', 'POST', 'DELETE'])
def order_create_stag(request):
    if request.method == 'GET':
        # print('Logging from terminal order create request get request')
       
        return HttpResponse('I am get request from saloni order creation')
       
 
    elif request.method == 'POST':
        try:
            tutorial_data = JSONParser().parse(request)
            print('Order creation event')
            
            line_items = tutorial_data['line_items']

            for line_item in line_items:
                if line_item['gift_card']:
                    line_item_id = line_item['id']
                    line_item_price = line_item['price']
                    break

            if line_item_id:
                randStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))
                
                # Gift Card details
                code          = str(randStr)
                initial_value = line_item_price
                attributes    = tutorial_data['note_attributes']
                order_id      = tutorial_data['id']
                order_name    = tutorial_data['name']
                sender_email  = tutorial_data['email']
                customer_id   = tutorial_data['customer']['id']
                customer_name = tutorial_data['customer']['first_name']
                phone         = tutorial_data['billing_address']['phone']

                phone         = str(phone)
                if phone:
                    phone     = '+91'+phone

                # print(code,initial_value,order_id,attributes,sender_email,line_item_id,customer_id,phone,order_name)

                order_status  = False
                try:
                    Order.objects.get(order_name = order_name)
                    order_status = False
                except:
                    q = Order(phone_no = phone,order_name = order_name)
                    q.save()
                    order_status = True
                    
                if order_status:
                    for attributeArr in attributes:
                        if attributeArr['name'] == "recipient_email":
                            recipient_email = attributeArr['value']
                        if attributeArr['name'] == "recipient_name":
                            recipient_name = attributeArr['value']
                        if attributeArr['name'] == "message":
                            custom_message = attributeArr['value']

                    to_emails = [recipient_email,sender_email]

                    # print(to_emails,custom_message)

                    # Shopify API Key and Store URL
                    store_url = settings.SHOP_URL
                    access_token = settings.ACCESS_TOKEN

                    # API endpoint for creating a Gift Card
                    gift_card_url = store_url + "/admin/api/2023-01/gift_cards.json"

                    # Set headers
                    headers = {
                        "Content-Type": "application/json",
                        "X-Shopify-Access-Token": access_token
                    }

                    # Data to be sent in the request body
                    gc_data = {
                        "gift_card": {
                            "note": custom_message,
                            "code": code,
                            "initial_value": initial_value,
                            "line_item_id": line_item_id,
                            "order_id": order_id,
                            "customer_id": customer_id,
                            "currency": "INR"
                        }
                    }

                    # Make the create Gift card API request
                    response = requests.post(gift_card_url, headers=headers, data=json.dumps(gc_data))

                    # Check the response status code
                    if response.status_code == 201:
                        # print("Gift Coupon code created successfully!")
                        message = Mail(
                            from_email='no-reply@discoverpilgrim.com',
                            to_emails=to_emails,
                            subject="""Discover Pilgrim Rs. """+initial_value+""" Gift Card""",
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
                                                        Enjoy skincare and haircare products made with the world’s best beauty ingredients!<br><br>
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
                                                                        <td colspan="2" style="border:1px solid #eaeaea"><img src="https://cdn.shopify.com/s/files/1/0620/1629/1045/files/Women_s_Day_E-Gift_Card.png?v=1678104250" alt="" border="0" style="width:800px" class="CToWUd a6T" data-bit="iit" tabindex="0"><div class="a6S" dir="ltr" style="opacity: 0.01; left: 604px; top: 971.406px;"><div id=":143" class="T-I J-J5-Ji aQv T-I-ax7 L3 a5q" role="button" tabindex="0" aria-label="Download attachment " jslog="91252; u014N:cOuCgd,Kr2w4b,xr6bB" data-tooltip-class="a1V" data-tooltip="Download"><div class="akn"><div class="aSK J-J5-Ji aYr"></div></div></div></div></td>
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
                            # print(response.status_code)
                        except Exception as e:
                            print(e.message)
                    # else:
                        # print("Failed to create Gift Coupon code. Error:", response.text)

                    time.sleep(3)

                    order_url = store_url + "/admin/api/2023-01/orders/" + str(order_id) + "/fulfillments.json"

                    # Make the create Gift card API request
                    order_fulfillment = requests.get(order_url, headers=headers)
                    order_fulfillment_json = order_fulfillment.json()

                    gift_card_id = order_fulfillment_json['fulfillments'][0]['receipt']['gift_cards'][0]['id']
                    # print(gift_card_id)

                    get_gift_card_url = store_url + "/admin/api/2023-01/gift_cards/" + str(gift_card_id) + "/disable.json"

                    disable_gc_data = {
                        "gift_card": {
                            "id": gift_card_id
                        }
                    }

                    # Make the create Gift card API request
                    disable_giftcard = requests.post(get_gift_card_url, headers=headers, data=json.dumps(disable_gc_data))
                    # print(disable_giftcard.json())
                else:
                    print("Order already created")
            # print('Order creation event new')
        except:
            print('Create gift card order exception')
            return HttpResponse('I am post error request gift card order creation event on live')
            pass

        return HttpResponse('I am post gift card order creation request event on live')

@api_view(['GET', 'POST', 'DELETE'])
def clickpost_order_deliver(request):
    if request.method == 'GET':
        print('Logging from terminal clickpost order deliver get request')
        return HttpResponse('I am get request from clickpost order deliver')
 
    elif request.method == 'POST':
        print('Logging from terminal clickpost order deliver post request')
        request_data = JSONParser().parse(request)
        # print(request_data)

        order_name = request_data['additional']['order_id']
        # print(order_name)

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # API endpoint for fetching an Order
        order_url = store_url + "/admin/api/2023-01/orders.json?name="+order_name+"&status=any"

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        try:
            # Make the get Order API request
            order_data = requests.get(order_url, headers=headers)
            orderJson = order_data.json()
            orderJson = orderJson['orders'][0]

            phone = orderJson['billing_address']['phone']
            phone = str(phone)
            phone = '+91'+phone

            order_id = orderJson['name']
            
            # print(phone,order_id)
            orderdeliver_status  = False
            try:
                OrderDeliver.objects.get(order_name = order_id)
                orderdeliver_status = False
            except:
                q = OrderDeliver(phone_no = phone,order_name = order_id)
                q.save()
                orderdeliver_status = True
                
            if orderdeliver_status:
                pid=''
                pname=''
                pquantity=''
                try:
                    # print(orderJson["line_items"][0]["product_id"])
                    count = 0
                    for i in orderJson["line_items"]:
                        if count == 0:
                            pid=pid+str(i["product_id"])
                            pname=pname+str(i["title"])
                            pquantity=pquantity+str(i["quantity"])
                        else:
                            pid=pid+','+str(i["product_id"])
                            pname=pname+','+str(i["title"])
                            pquantity=pquantity+','+str(i["quantity"])
                        count = count + 1
                    #pid=tutorial_data["line_items"][0]["product_id"]
                    #pname=tutorial_data["line_items"][0]["title"]
                    #pquantity=tutorial_data["line_items"][0]["quantity"]
                except:
                    print('IN ORDERdelivered exception product section')
                    pass

                url = "https://api.webengage.com/v1/accounts/11b564785/events"

                headers = CaseInsensitiveDict()
                webengagekey=settings.WEBENGAGE
                headers["Authorization"] = "Bearer {}".format(webengagekey)
                headers["Content-Type"] = "application/json"

                data = {
                    "userId": phone,
                    "eventName": "Order Delivered",
                    "eventData": 
                    {
                        "orderID":order_id,
                        "orderGrandTotal":orderJson['total_price'],
                        "Product ID": pid,
                        "Quantity": pquantity,
                        "Product": pname
                    }
                }
                data=json.dumps(data)
                # print(data)
                resp = requests.post(url, headers=headers, data=data)
                print(resp.text)
            else:
                print("Order deliver already created")
                return HttpResponse(json.dumps({"message": "Order deliver already created"}))
        except Exception as e:
            print(e.message)

        return HttpResponse(json.dumps(resp))

@api_view(['GET', 'POST'])
def check_customer_account(request):
    if request.method == 'GET':
        phone = request.GET.get("phone")

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # API endpoint for search a Customer
        customer_url = store_url + "/admin/api/2023-01/customers/search.json?query=phone:" + phone

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        # Make the fetch Customer API request
        customer_data = requests.get(customer_url, headers=headers)
        customerJson = customer_data.json()
        # print(customerJson)
        if(len(customerJson['customers']) != 0):
            cust_response = {"has_account": True, "customer_id": customerJson['customers'][0]['id']}
            # print(cust_response)
        else:
            cust_response = {"has_account": False}
            # print(cust_response)

        # final_resp = cust_response.json()
        return HttpResponse(json.dumps(cust_response))
        # return HttpResponse('I am post request from check customer account')

        # print('Logging from terminal check customer account get request')
        # return HttpResponse('I am get request from check customer account')
    elif request.method == "POST":
        print('Logging from terminal check customer account post request')
        return HttpResponse('I am post request from check customer account')


@api_view(['GET', 'POST'])
def register_webhook(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        address = request_data['address']
        topic = request_data['topic']
        webhook_data = {
            "webhook": {
                "address": address,
                "topic": topic,
                "format": "json"
            }
        }
        print(webhook_data)

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # API endpoint for fetching an Order
        webhook_url = store_url + "/admin/api/2023-01/webhooks.json"

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        try:
            # Make the get Webhook API request
            order_data = requests.post(webhook_url, headers=headers, data=json.dumps(webhook_data))
            orderJson = order_data.json()
            print(orderJson)
            return HttpResponse(json.dumps(orderJson))
        except Exception as e:
            print(e.message)
            return HttpResponse(json.dumps(e))


@api_view(['GET', 'POST', 'DELETE'])
def order_create_webhook(request):
    if request.method == 'GET':
        print('Logging from terminal order create get request')
        order_response = {"status": 200, "message": "Sample get request"}
        return HttpResponse(json.dumps(order_response))

    elif request.method == 'POST':
        order_data = JSONParser().parse(request)
        print('Order creation webhook event')

        try:
            line_items = order_data['line_items']

            for line_item in line_items:
                if line_item['gift_card']:
                    line_item_id = line_item['id']
                    line_item_price = line_item['price']
                    product_id = line_item['product_id']
                    break

            if line_item_id:
                randStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16))
                
                # Gift Card details
                code          = str(randStr)
                initial_value = line_item_price
                attributes    = order_data['note_attributes']
                order_id      = order_data['id']
                order_name    = order_data['name']
                sender_email  = order_data['email']
                customer_id   = order_data['customer']['id']
                customer_name = order_data['customer']['first_name']
                phone         = order_data['billing_address']['phone']

                phone         = str(phone)
                if phone:
                    phone     = '+91'+phone

                print(code,initial_value,order_id,attributes,sender_email,line_item_id,customer_id,phone,order_name)

                order_status  = False
                try:
                    Order.objects.get(order_name = order_name)
                    order_status = False
                except:
                    q = Order(phone_no = phone,order_name = order_name)
                    q.save()
                    order_status = True
                    
                if order_status:
                    for attributeArr in attributes:
                        if attributeArr['name'] == "recipient_email":
                            recipient_email = attributeArr['value']
                        if attributeArr['name'] == "recipient_name":
                            recipient_name = attributeArr['value']
                        if attributeArr['name'] == "message":
                            custom_message = attributeArr['value']

                    to_emails = [recipient_email,sender_email]

                    print(to_emails,custom_message)

                    # Shopify API Key and Store URL
                    store_url = settings.SHOP_URL
                    access_token = settings.ACCESS_TOKEN

                    # API endpoint for creating a Gift Card
                    gift_card_url = store_url + "/admin/api/2023-01/gift_cards.json"

                    # Set headers
                    headers = {
                        "Content-Type": "application/json",
                        "X-Shopify-Access-Token": access_token
                    }

                    # Data to be sent in the request body
                    gc_data = {
                        "gift_card": {
                            "note": custom_message,
                            "code": code,
                            "initial_value": initial_value,
                            "line_item_id": line_item_id,
                            "order_id": order_id,
                            "customer_id": customer_id,
                            "currency": "INR"
                        }
                    }

                    # Make the create Gift card API request
                    response = requests.post(gift_card_url, headers=headers, data=json.dumps(gc_data))

                    # Check the response status code
                    if response.status_code == 201:
                        print("Gift Coupon code created successfully!")
                        # API endpoint for fetching a product image
                        product_url = store_url + "/admin/api/2023-01/products/" + str(product_id) + ".json?fields=image"

                        # Make the create Gift card API request
                        presponse = requests.get(product_url, headers=headers)

                        image_url = ""
                        # Check the response status code
                        if presponse.status_code == 200:
                            productData = presponse.json()
                            print("Product fetched successfully!")
                            image_url = productData['product']['image']['src']
                            # print(image_url)

                        message = Mail(
                            from_email='no-reply@discoverpilgrim.com',
                            to_emails=to_emails,
                            subject="""Discover Pilgrim Rs. """+initial_value+""" Gift Card""",
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
                                                        Enjoy skincare and haircare products made with the world’s best beauty ingredients!<br><br>
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
                            # print(response.status_code)
                        except Exception as e:
                            print(e.message)
                    else:
                        print("Failed to create Gift Coupon code. Error:", response.text)

                    time.sleep(3)

                    order_url = store_url + "/admin/api/2023-01/orders/" + str(order_id) + "/fulfillments.json"

                    # Make the create Gift card API request
                    order_fulfillment = requests.get(order_url, headers=headers)
                    order_fulfillment_json = order_fulfillment.json()

                    gift_card_id = order_fulfillment_json['fulfillments'][0]['receipt']['gift_cards'][0]['id']
                    print(gift_card_id)

                    get_gift_card_url = store_url + "/admin/api/2023-01/gift_cards/" + str(gift_card_id) + "/disable.json"

                    disable_gc_data = {
                        "gift_card": {
                            "id": gift_card_id
                        }
                    }

                    # Make the create Gift card API request
                    disable_giftcard = requests.post(get_gift_card_url, headers=headers, data=json.dumps(disable_gc_data))
                    print(disable_giftcard.json())
                else:
                    print("Order already created")
            print('Order creation webhook event new')
        except:
            print('Create gift card order webhook exception')
            return HttpResponse('I am post error request gift card order creation webhook event on live')

        return HttpResponse('I am post gift card order creation webhook request event on live')


@api_view(['GET', 'POST', 'DELETE'])
def pincode_list_db(request):
    if request.method == 'GET':
        return HttpResponse('I am get request pincode db')
 
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        # print(request_data)
        pincode = request_data['pincode']
        pincode = str(pincode)
		
        
    result_data = {"status":"200","data":{"cod":"","service":""}}

    try:
        cod_pincodes = Pincode.objects.get(mode = "COD")
        cod_pincodes_list = cod_pincodes.pincode_list
        cod_pincodes_list = list(map(str.strip, cod_pincodes_list.translate( { ord(i): None for i in '[]'} ).split(',')))
        
        if pincode in cod_pincodes_list:
            result_data['data']['cod'] = True
        else:
            result_data['data']['cod'] = False

        prepaid_pincodes = Pincode.objects.get(mode = "Prepaid")
        prepaid_pincodes_list = prepaid_pincodes.pincode_list
        prepaid_pincodes_list = list(map(str.strip, prepaid_pincodes_list.translate( { ord(i): None for i in '[]'} ).split(',')))

        if pincode in prepaid_pincodes_list:
            result_data['data']['service'] = True
        else:
            result_data['data']['service'] = False
    except:
        print("Error in db")

    return HttpResponse(json.dumps(result_data))


@api_view(['GET', 'POST', 'DELETE'])
def vamaship_to_db(request):
    if request.method == 'GET': 
        url = "https://api.vamaship.com/ecom/api/v1/dom/coverage"

        headers = CaseInsensitiveDict()
        key = settings.VAMAPI
        headers["Authorization"] = "Bearer {}".format(key)
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        # cod pincodes
        data = '{"type": "cod", "origin": 110061}'
        resp = requests.post(url, headers=headers, data=data)
        result = resp.json()
        cod_dest_pincodes = result["destinations"]
        # cod_dest_pincodes = ','.join(cod_dest_pincodes)

        # prepaid pincodes
        data_prepaid = '{"type": "prepaid", "origin": 110061}'
        resp_prepaid = requests.post(url, headers=headers, data=data_prepaid)
        result_prepaid=resp_prepaid.json()
        prepaid_dest_pincodes = result_prepaid["destinations"]
        # prepaid_dest_pincodes = ','.join(prepaid_dest_pincodes)

        # update cod pincodes in db
        qcod = Pincode.objects.get(mode="COD")
        qcod.pincode_list = cod_dest_pincodes
        qcod.save()

        # update prepaid pincodes in db
        qprepaid = Pincode.objects.get(mode="Prepaid")
        qprepaid.pincode_list = prepaid_dest_pincodes
        qprepaid.save()

        return HttpResponse("Vamaship to DB execution successful")


@api_view(['GET', 'POST'])
def update_customer_profile(request):
    if request.method == "GET":
        print("Update customer get method called")
        return HttpResponse("Update customer get method called")
    elif request.method == "POST":
        print("Update customer post method called")
        request_data = JSONParser().parse(request)
        print(request_data)
        formName = request_data['form']
        customerId = request_data['customerId']
        if formName == "account-details":
            first_name = request_data['first_name']
            last_name = request_data['last_name']
            phone = "+91"+request_data['phone']
            email = request_data['email']
        elif formName == "edit-profile":
            profileImg = request_data['profile-img']
            dob = request_data['dob']
            concerns = request_data['concerns']
            choices = request_data['choices']
            profession = request_data['profession']
            gender = request_data['gender']
        elif formName == "update-image":
            profileImg = request_data['profile-img']
        # elif formName == "select-language":
        #     language = request_data['language']

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        if formName == "account-details":
            customer_data = {
                "customer": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "email": email
                }
            }
        elif formName == "edit-profile":
            # API endpoint for fetching a Customer metafields
            customermetafield_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + "/metafields.json"
            gender_metafield_id = ""
            dob_metafield_id = ""
            image_metafield_id = ""
            concerns_metafield_id = ""
            choices_metafield_id = ""
            profession_metafield_id = ""
            language_metafield_id = ""
            try:
                # Make the get Webhook API request
                customermeta_data = requests.get(customermetafield_url, headers=headers)
                customerMetaJson = customermeta_data.json()
                print(customerMetaJson)
                metafields = customerMetaJson['metafields']
                for metafield in metafields:
                    if metafield['key'] == "gender":
                        gender_metafield_id = metafield['id']
                    if metafield['key'] == "dob":
                        dob_metafield_id = metafield['id']
                    if metafield['key'] == "profile_image":
                        image_metafield_id = metafield['id']
                    if metafield['key'] == "concerns":
                        concerns_metafield_id = metafield['id']
                    if metafield['key'] == "in_love_with":
                        choices_metafield_id = metafield['id']
                    if metafield['key'] == "profession":
                        profession_metafield_id = metafield['id']
                    if metafield['key'] == "language":
                        language_metafield_id = metafield['id']
            except Exception as e:
                print(e)
                # logger.error('Failed to upload to ftp: '+ str(e))

            time.sleep(3)
            print(gender_metafield_id,dob_metafield_id,image_metafield_id,concerns_metafield_id,choices_metafield_id,profession_metafield_id,language_metafield_id)

            imgObj = {
                "key": "profile_image",
                "value": profileImg,
                "type": "url",
                "namespace": "custom"
            }
            if(image_metafield_id):
                imgObj["id"] = image_metafield_id

            dobObj = {
                "key": "dob",
                "value": dob,
                "type": "date",
                "namespace": "custom"
            }
            if(dob_metafield_id):
                dobObj["id"] = dob_metafield_id
            
            concernsObj = {
                "key": "concerns",
                "value": concerns,
                "type": "list.single_line_text_field",
                "namespace": "custom"
            }
            if(concerns_metafield_id):
                concernsObj["id"] = concerns_metafield_id

            choicesObj = {
                "key": "in_love_with",
                "value": choices,
                "type": "list.single_line_text_field",
                "namespace": "custom"
            }
            if(choices_metafield_id):
                choicesObj["id"] = choices_metafield_id

            professionObj = {
                "key": "profession",
                "value": profession,
                "type": "single_line_text_field",
                "namespace": "custom"
            }
            if(profession_metafield_id):
                professionObj["id"] = profession_metafield_id

            genderObj = {
                "key": "gender",
                "value": gender,
                "type": "single_line_text_field",
                "namespace": "custom"
            }
            if(gender_metafield_id):
                genderObj["id"] = gender_metafield_id

            customer_data = {
                "customer": {
                    "metafields": [
                        imgObj,
                        dobObj,
                        concernsObj,
                        choicesObj,
                        professionObj,
                        genderObj
                    ]
                }
            }
        elif formName == "update-image":
            # API endpoint for fetching a Customer metafields
            customermetafield_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + "/metafields.json"
            image_metafield_id = ""
            try:
                # Make the get Webhook API request
                customermeta_data = requests.get(customermetafield_url, headers=headers)
                customerMetaJson = customermeta_data.json()
                print(customerMetaJson)
                metafields = customerMetaJson['metafields']
                for metafield in metafields:
                    if metafield['key'] == "profile_image":
                        image_metafield_id = metafield['id']
            except Exception as e:
                print(e)
                # logger.error('Failed to upload to ftp: '+ str(e))

            time.sleep(3)
            print(image_metafield_id)

            imgObj = {
                "key": "profile_image",
                "value": profileImg,
                "type": "url",
                "namespace": "custom"
            }
            if(image_metafield_id):
                imgObj["id"] = image_metafield_id

            customer_data = {
                "customer": {
                    "metafields": [
                        imgObj
                    ]
                }
            }
        # elif formName == "select-language":
        #     languageObj = {
        #         "key": "language",
        #         "value": language,
        #         "type": "single_line_text_field",
        #         "namespace": "custom"
        #     }
        #     if(language_metafield_id):
        #         languageObj["id"] = language_metafield_id

        #     customer_data = {
        #         "customer": {
        #             "metafields": [
        #                 languageObj
        #             ]
        #         }
        #     }

        # API endpoint for updating a Customer
        customer_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + ".json"
        
        print(customer_data)
        # return HttpResponse(json.dumps(customer_data))

        try:
            # Make the get Webhook API request
            customer_data = requests.put(customer_url, headers=headers, data=json.dumps(customer_data))
            customerJson = customer_data.json()
            print(customerJson)
            return HttpResponse(json.dumps({"status": "success","message": "Profile updated successfully"}))
            # return HttpResponse(json.dumps(customer_data))
        except Exception as e:
            print(e)
            # logger.error('Failed to upload to ftp: '+ str(e))
            return HttpResponse(json.dumps(e))
        

@api_view(['GET', 'POST'])
def upload_customer_image(request):
    if request.method == 'GET':
        print("Upload customer profile get method called")
        return HttpResponse("Upload customer profile get method called")
    elif request.method == 'POST':
       print("Upload customer profile post method called")
       form = ImageFileUploadForm(request.POST, request.FILES)
       if form.is_valid():
           saveForm = form.save()
           imgUrl = "https://gift.discoverpilgrim.com/"+str(saveForm.profile_image)
           print(imgUrl)
           return JsonResponse({"status": "success", 'error': False, 'message': 'Uploaded Successfully', 'imgUrl': imgUrl})
       else:
           return JsonResponse({"status": "failed", 'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'django_image_upload_ajax.html', {'form': form})
    

@api_view(['GET', 'POST'])
def set_default_address(request):
    if request.method == 'GET':
        print("Set default address get method called")
        return HttpResponse("Set default address get method called")
    elif request.method == 'POST':
        print("Set default address post method called")
        request_data = JSONParser().parse(request)
        print(request_data)
        customerId = request_data['customerId']
        addressId = request_data['addressId']

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        cust_address_data = {
            "customer_address": {
                "id": addressId,
                "customer_id": customerId,
                "default": True
            }
        }

        # API endpoint for updating a Customer
        cust_address_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + "/addresses/" + str(addressId) + "/default.json"

        try:
            customer_data = requests.put(cust_address_url, headers=headers, data=json.dumps(cust_address_data))
            return HttpResponse(json.dumps({"status": "success","message": "Default address updated successfully"}))
        except Exception as e:
            print(e)
            # logger.error('Failed to upload to ftp: '+ str(e))
            return HttpResponse(json.dumps(e))
            return HttpResponse("Set default address post method called")
        

@api_view(['GET', 'POST'])
def save_customer_review(request):
    if request.method == 'GET':
        print("Save customer request get method")
        return JsonResponse({"status": "success", "message": "Save customer review get method called"})
    elif request.method == 'POST':
        print("Save customer review post method")
        request_data = JSONParser().parse(request)
        print(request_data)
        page = request_data['page']
        answer1 = request_data['answer1']
        answer2 = request_data['answer2']
        try:
            saveReview = CustomerReview(page = page, answer1 = answer1, answer2 = answer2)
            saveReview.save()
            review_status = True
        except:
            review_status  = False
            
        if review_status:
            return JsonResponse({"status": "success", "message": "Review submitted"})
        else:
            return JsonResponse({"status": "failes", "message": "Review submission failed"})
        return JsonResponse({"status": "success", "message": "Review submitted"})
    

@api_view(['GET', 'POST'])
def autologin_customer(request):
    if request.method == 'GET':
        print("Auto login customer get method")
        return JsonResponse({"status": "success", "message": "Auto login customer get method called"})
    elif request.method == 'POST':
        print("Auto login customer post method")
        request_data = JSONParser().parse(request)
        print(request_data)
        email = request_data['email']

        # Replace these values with your domain name and Multipass secret
        domain_name = settings.SHOP
        multipass_secret = "97413d838c9d8328e770f1f8db3ad0ba"

        customer_data = {
            "email": email,
        }

        # Generate the Multipass token
        multipassData = ShopifyMultipass(multipass_secret)
        token = multipassData.generate_token(customer_data)

        # Generate the Multipass URL for your domain
        url = "https://{domain_name}/account/login/multipass/{token}"
        print(url)
        return JsonResponse({"status": "success", "message": "Auto login customer post method called", "redirect_url": url})


# @api_view(['GET', 'POST', 'DELETE'])
# def customer_create_webhook(request):
#     if request.method == 'GET':
#         print('Logging from terminal customer create get request')
#         customer_response = {"status": 200, "message": "Sample get request"}
#         return HttpResponse(json.dumps(customer_response))

#     elif request.method == 'POST':
#         customer_data = JSONParser().parse(request)
#         print('Customer creation webhook event')


@api_view(['GET', 'POST'])
def update_newsletter_customer(request):
    if request.method == 'GET':
        print('Logging from terminal update customer newsletter get request')
        newsletter_response = {"status": 200, "message": "Sample get request"}
        return HttpResponse(json.dumps(newsletter_response))

    elif request.method == 'POST':
        newsletter_data = JSONParser().parse(request)
        print('Update customer newsletter post request')

        email = newsletter_data['email']
        phone = newsletter_data['phone']
        tags = newsletter_data['tags']

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # API endpoint for search a Customer
        get_customer_url = store_url + "/admin/api/2023-01/customers/search.json?query=email:" + email

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        time.sleep(10)

        # Make the fetch Customer API request
        customer_data = requests.get(get_customer_url, headers=headers)
        customerJson = customer_data.json()
        customerId = customerJson['customers'][0]['id']
        customerTags = customerJson['customers'][0]['tags']
        if customerTags:
            final_tags = customerTags + ", " + tags
        else:
            final_tags = tags

        customerPhone = customerJson['customers'][0]['phone']
        if not customerPhone:
            customerPhone = phone

        if(len(customerJson['customers']) != 0):
            customer_data = {
                "customer": {
                    "phone": customerPhone,
                    "tags": final_tags
                }
            }

            # API endpoint for updating a Customer
            customer_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + ".json"

            try:
                # Make the get Webhook API request
                customer_data = requests.put(customer_url, headers=headers, data=json.dumps(customer_data))
                customerJson = customer_data.json()
                return HttpResponse(json.dumps({"status": "success", "has_account": True, "message": "Customer updated successfully"}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps(e))
        else:
            return HttpResponse(json.dumps({"status": "failed", "has_account": False, "message": "Customer not found"}))


@api_view(['GET', 'POST'])
def create_authentication_customer(request):
    if request.method == 'GET':
        print('Logging from terminal update customer authentication get request')
        authentication_response = {"status": 200, "message": "Sample get request"}
        return HttpResponse(json.dumps(authentication_response))

    elif request.method == 'POST':
        newsletter_data = JSONParser().parse(request)
        print('Update customer authentication post request')

        name = newsletter_data['name']
        email = newsletter_data['email']
        phone = newsletter_data['phone']
        tags = newsletter_data['tags']

        # Shopify API Key and Store URL
        store_url = settings.SHOP_URL
        access_token = settings.ACCESS_TOKEN

        # API endpoint for search a Customer
        get_customer_url = store_url + "/admin/api/2023-01/customers/search.json?query=email:" + email
        get_customer_phone_url = store_url + "/admin/api/2023-01/customers/search.json?query=phone:" + phone

        # Set headers
        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }

        # Make the fetch Customer API request
        customer_data = requests.get(get_customer_url, headers=headers)
        customerJson = customer_data.json()

         # Make the fetch Customer API request
        customer_phone_data = requests.get(get_customer_phone_url, headers=headers)
        customerPhoneJson = customer_phone_data.json()

        create_customer = False
        if len(customerJson['customers']) == 0 and len(customerPhoneJson['customers']) == 0:
            create_customer = True

        if create_customer:
            splitName = " " in name
            if splitName:
                customer_name = name.split(" ", 1)
                firstName = customer_name[0]
                lastName = customer_name[1]
            else:
                firstName = name
                lastName = ""

            new_customer_data = {
                "customer": {
                    "first_name": firstName,
                    "last_name": lastName,
                    "email": email,
                    "phone": phone,
                    "tags": tags
                }
            }

            # API endpoint for updating a Customer
            customer_url = store_url + "/admin/api/2023-01/customers.json"

            try:
                # Make the get Webhook API request
                customer_data = requests.post(customer_url, headers=headers, data=json.dumps(new_customer_data))
                newCustomerJson = customer_data.json()
                if customer_data.status_code == 201:
                    return HttpResponse(json.dumps({"status": "success", "message": "Customer created successfully"}))
                else:
                    return HttpResponse(json.dumps({"status": "failed", "message": "Customer not created", "error": newCustomerJson}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps(e))
        else:
            if len(customerJson['customers']) != 0:
                customerId = customerJson['customers'][0]['id']
                customerTags = customerJson['customers'][0]['tags']
                customerPhone = customerJson['customers'][0]['phone']
                customerEmail = customerJson['customers'][0]['email']
            elif len(customerPhoneJson['customers']) != 0:
                customerId = customerPhoneJson['customers'][0]['id']
                customerTags = customerPhoneJson['customers'][0]['tags']
                customerPhone = customerPhoneJson['customers'][0]['phone']
                customerEmail = customerPhoneJson['customers'][0]['email']

            if customerTags:
                final_tags = customerTags + ", " + tags
            else:
                final_tags = tags

            if not customerPhone:
                customerPhone = phone

            if not customerEmail:
                customerEmail = email

            customer_data = {
                "customer": {
                    "email": customerEmail,
                    "phone": customerPhone,
                    "tags": final_tags
                }
            }

            # API endpoint for updating a Customer
            customer_url = store_url + "/admin/api/2023-01/customers/" + str(customerId) + ".json"

            try:
                # Make the get Webhook API request
                customer_data = requests.put(customer_url, headers=headers, data=json.dumps(customer_data))
                newCustomerJson = customer_data.json()
                if customer_data.status_code == 200:
                    return HttpResponse(json.dumps({"status": "success", "message": "Customer updated successfully"}))
                else:
                    return HttpResponse(json.dumps({"status": "failed", "message": "Customer not updated", "error": newCustomerJson}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps(e))
            

@api_view(['GET', 'POST'])
def truecaller_callback_url(request):
    if request.method == 'GET':
        print('Logging from terminal truecaller callback url get request')
        truecaller_response = {"status": 200, "message": "Sample get request"}
        return HttpResponse(json.dumps(truecaller_response))

    elif request.method == 'POST':
        print(request)
        truecaller_data = JSONParser().parse(request)
        print('Truecaller callback url post request')
        print(json.dumps(truecaller_data))
        requestId = truecaller_data['requestId']
        if "status" in truecaller_data.keys():
            print("Has status in response")
            flowStatus = truecaller_data['status']
            try:
                u = TruecallerCustomer.objects.get(request_id = requestId)
                u.flow_status = truecaller_data['status']
                u.save()
            except:
                q = TruecallerCustomer(request_id = requestId, flow_status = flowStatus)
                q.save()
        elif "accessToken" in truecaller_data.keys():
            print("Has access token in response")
            try:
                t = TruecallerCustomer.objects.get(request_id=requestId)
                t.access_token = truecaller_data['accessToken']
                t.save()
            except:
                accessToken = truecaller_data['accessToken']
                q = TruecallerCustomer(request_id = requestId, flow_status = "flow_invoked", access_token = accessToken)
                q.save()
        else:
            q = TruecallerCustomer(request_id = requestId, flow_status = "Error in truecaller response")
            q.save()
            truecaller_data = {"requestId": requestId, "status" : 500, "message": "Internal server error"}

        return HttpResponse(json.dumps(truecaller_data))
    
@api_view(['GET', 'POST'])
def fetch_tc_customer(request):
    if request.method == 'GET':
        print('Logging from terminal fetch truecaller user get request')
        requestId = request.GET.get("requestId")
        print(requestId)
        try:
            tc_result = TruecallerCustomer.objects.get(request_id = requestId)
            if tc_result.flow_status == "flow_invoked":
                if tc_result.access_token:
                    access_token = tc_result.access_token
                    url = "https://profile4-noneu.truecaller.com/v1/default"

                    headers = CaseInsensitiveDict()
                    headers["Authorization"] = "Bearer {}".format(access_token)
                    headers["Cache-Control"] = "no-cache"

                    # truecalller fetch user profile
                    resp = requests.get(url, headers=headers)
                    result = resp.json()
                    print(result)
                    print(type(result))
                    findKey = "phoneNumbers"
                    if findKey in result:
                        tc_result.user_status = "user found"
                        tc_result.save()
                    else:
                        tc_result.user_status = result.status
                        tc_result.save()
                    user_response = {"status": 200, "message": "Trucaller api response", "data": result}
                else:
                    user_response = {"status": 404, "message": "Access token not found"}
            else:
                user_response = {"status": 202, "message": "Flow dropped"}
        except:
            user_response = {"status": 404, "message": "Request not found"}
        
        print(user_response)
        return HttpResponse(json.dumps(user_response))

    elif request.method == 'POST':
        truecaller_data = JSONParser().parse(request)
        print('Fetch truecaller user post request')
        return HttpResponse(json.dumps(truecaller_data))