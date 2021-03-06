import math
from django.db import models

from billing.models import BillingProfile
from carts.models import Cart
from addresses.models import Address
from ecommerce.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save

# Create your models here.
ORDER_STATUS_CHOICES = (
    ('Created','Created'),
    ('Paid','Paid'),
    ('Shipped','Shipped'),
    ('Refunded','Refunded'),
)

class OrderManager(models.Manager):
    def get_or_new(self,billing_profile, cart_obj):
        created=False
        qs = self.get_queryset().filter(billing_profile=billing_profile,cart=cart_obj,active=True,status='created')
        if qs.count()==1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile, 
                cart=cart_obj
                )
            created=True
        return obj,created


PAYMENT_METHODS = (
    ("Cash on Delivery","Cash on Delivery"),
    ("Khalti","Khalti"),
    ("Esewa","Esewa"),
)

class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile,null=True, blank=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(Address,related_name="shipping_address", null=True, blank=True,on_delete=models.SET_NULL)
    billing_address = models.ForeignKey(Address, related_name="billing_address",null=True,blank=True, on_delete=models.SET_NULL)
    cart = models.ForeignKey(Cart,null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)   
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active= models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHODS, default="Cash on Delivery")


    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        print(cart_total)
        shipping_total = self.shipping_total
        print(shipping_total)
        new_total = math.fsum([cart_total , shipping_total])
        self.total=new_total
        self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        shipping_address = self.shipping_address
        billing_address = self.billing_address
        total = self.total
        if billing_profile and shipping_address and billing_address and total > 0:
            return True
        return False
    
    def mark_paid(self):
        if self.check_done():
            self.status = "Paid"
            self.save()
        return self.status

    def mark_shipped(self):
        if self.check_done():
            self.status = 'Shipped'
            self.save()
        return self.status



def pre_save_create_order_id(instance, sender, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


def post_save_cart_total(instance, sender,created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        print(cart_total)
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count()==1:
            order_obj = qs.first()
            order_obj.update_total()


def post_save_order(instance, sender, created, *args, **kwargs):
    if created:
        instance.update_total()
    


pre_save.connect(pre_save_create_order_id,sender=Order)
post_save.connect(post_save_cart_total,sender=Cart)
post_save.connect(post_save_order,sender=Order)