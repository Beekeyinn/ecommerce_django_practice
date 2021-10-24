from random import randint
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save,post_save
from django.db.models import Q

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.urls import reverse

from datetime import timedelta
from django.utils import timezone

from django.core.mail import send_mail
from django.template.loader import get_template

from ecommerce.utils import rand_string_generator, unique_key_generator
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, fullname=None, password=None,is_active=True, is_staff = False,is_admin=False):
        if not email:
            raise ValueError("User must have Email Address.")

        if not password:
            raise ValueError("User must have password.")
        
        # if not fullname:
        #     raise ValueError("Fullname is Required.")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) 
        user_obj.fullname = fullname
        user_obj.is_active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using = self._db)
        return user_obj
    
    def create_superuser(self, email, fullname=None, password=None):
        user = self.create_user(
            email,
            fullname,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    def create_staffuser(self, email, fullname=None, password=None):
        user = self.create_user(
            email,
            fullname,
            password=password,
            is_staff=True,
        )
        return user


class User(AbstractBaseUser):
    email   = models.EmailField(unique=True, max_length=255)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    is_active  = models.BooleanField(default=True)
    staff   = models.BooleanField(default=False)
    admin   = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    

    def get_fullname(self):
        if self.fullname:
            return self.fullname
        return self.email
    
    def get_shortname(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EmailActivationQueryset(models.QuerySet):
    def confirmable(self):
        DEFAULT_ACTIVATION_DAYS = 7
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated = False,
            forced_expired = False
        ).filter(
            timestamp__gt=start_range,
            timestamp__lt=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQueryset(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                Q(email = email) | 
                Q(user__email = email)
              ).filter(
                activated=False
                )




class EmailActivation(models.Model):
    user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    key  = models.CharField(max_length=120,blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_path = getattr(settings,'BASE_URL',"127.0.0.1:8000")
                key_path = reverse('Accounts:email_activate',kwargs={'key':self.key})
                path = f"{base_path}{key_path}"
                context = {
                    'path':path,
                    'email':self.email
                }

                txt_ = get_template('registration/emails/verify.txt').render(context)
                html_ = get_template('registration/emails/verify.html').render(context)
                subject = "1-Click Email Verification"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = (self.email,)
                send_mail_b = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently = False
                )

                return send_mail_b
        return False

def pre_save_email_activation(instance, sender, *args, **kwargs) :
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation,sender=EmailActivation)

def post_save_user_create_receiver(sender,instance,created,*args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance,email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver,sender=User)