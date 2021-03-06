from django.db import models
from billing.models import BillingProfile

# Create your models here.
ADDRESS_TYPE = (
    ('billing','Billing'),
    ('shipping','Shipping')
)

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL)
    address_type = models.CharField(max_length=120,choices=ADDRESS_TYPE)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120,null=True,blank=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120,default="Nepal")
    state = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=120)


    def __str__(self):
        return str(self.billing_profile)

    def get_address(self):
        country=self.country
        state = self.state
        city=self.city
        postal = self.postal_code
        line1=self.address_line_1
        line2 = self.address_line_2 or ""
        return f"{country}\n{state}\n{city}, {postal}\n{line1}\n{line2}"
    
