from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # saloni live
    path('order_create_stag',views.order_create_stag,name='order_create_stag'),
    path('clickpost_order_deliver',views.clickpost_order_deliver,name='clickpost_order_deliver'),
    path('check_customer_account',views.check_customer_account,name='check_customer_account'),
    path('register_webhook',views.register_webhook,name='register_webhook'),
    path('order_create_webhook',views.order_create_webhook,name='order_create_webhook'),
    path('pincode_list_db',views.pincode_list_db,name='pincode_list_db'),
    path('vamaship_to_db',views.vamaship_to_db,name='vamaship_to_db'),
    path('update_customer_profile',views.update_customer_profile,name='update_customer_profile'),
    path('upload_customer_image',views.upload_customer_image,name='upload_customer_image'),
    path('set_default_address',views.set_default_address,name='set_default_address'),
    path('save_customer_review',views.save_customer_review,name='save_customer_review'),
    path('autologin_customer',views.autologin_customer,name='autologin_customer'),
    # path('customer_create_webhook',views.customer_create_webhook,name='customer_create_webhook'),
    path('update_newsletter_customer',views.update_newsletter_customer,name='update_newsletter_customer'),
    path('create_authentication_customer',views.create_authentication_customer,name='create_authentication_customer'),
    path('truecaller_callback_url',views.truecaller_callback_url,name='truecaller_callback_url'),
    path('fetch_tc_customer',views.fetch_tc_customer,name='fetch_tc_customer'),
]
