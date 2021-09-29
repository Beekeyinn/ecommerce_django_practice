from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

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
        user_obj.active = is_active
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
    active  = models.BooleanField(default=True)
    staff   = models.BooleanField(default=False)
    admin   = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.fullname:
            return self.fullname
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
    def is_active(self):
        return self.active

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


    