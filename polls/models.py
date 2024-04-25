from django.db import models

# Create your models here.

class Order(models.Model):
    order_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=30)

class Pincode(models.Model):
    mode = models.CharField(max_length=30)
    pincode_list = models.TextField(max_length=10000)

class OrderDeliver(models.Model):
    order_name = models.CharField(max_length=30)
    phone_no = models.CharField(max_length=30)

class Profile(models.Model):
    customer_id = models.BigIntegerField()
    profile_image = models.ImageField(upload_to="profile-images")

class CustomerReview(models.Model):
    Homepage = 'HP'
    OtherPage = 'OP'
    CartPage = 'CP'
    Transaction = 'TP'
    PAGES = [
        (Homepage, 'Homepage'),
        (OtherPage, 'Other Page'),
        (CartPage, 'Cart Page'),
        (Transaction, 'Transaction'),
    ]
    ANSWER = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    page = models.CharField(
        max_length = 2,
        choices = PAGES,
    )
    answer1 = models.IntegerField(
        choices = ANSWER,
    )
    answer2 = models.IntegerField(
        choices = ANSWER,
    )

class TruecallerCustomer(models.Model):
    request_id = models.CharField(max_length=25)
    flow_status = models.CharField(max_length=100)
    access_token = models.CharField(max_length=100, blank=True)
    user_status = models.CharField(max_length=100, blank=True)