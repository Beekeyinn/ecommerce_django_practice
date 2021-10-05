from accounts.models import GuestEmail
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save
User = settings.AUTH_USER_MODEL



class BillingProfileManager(models.Manager):
    def get_or_new(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        obj=None
        created=False
        if user.is_authenticated:
            # Logged in checkout
            obj, created = self.model.objects.get_or_create(user=user,email=user.email)
        elif guest_email_id is not None:
            # Guest user checkout
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


# def billing_profile_created_receiver(sender, instance, *args, **kwargs):
#     if not instance.customer_id and instance.email:
#         customer = stripe.Customer.create(
#             email=instance.email
#         )
#         print(customer)
#         instance.customer_id = customer.id

# pre_save.connect(billing_profile_created_receiver,sender = BillingProfile)

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver,sender=User)