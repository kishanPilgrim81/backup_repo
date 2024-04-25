from django.contrib import admin

# Register your models here.
# Register your models here.
from .models import Order
from .models import Pincode
from .models import OrderDeliver
from .models import Profile
from .models import CustomerReview
from .models import TruecallerCustomer
   
admin.site.register(Order)
admin.site.register(Pincode)
admin.site.register(OrderDeliver)
admin.site.register(Profile)
admin.site.register(CustomerReview)
admin.site.register(TruecallerCustomer)