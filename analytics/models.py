from django.conf import settings
from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save

from .signals import object_viewed_signal
from .utils import get_client_ip

from accounts.signal import user_logged_in


FORCE_SESSION_TO_ONE = getattr(settings,'FORCE_SESSION_TO_ONE',False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings,'FORCE_INACTIVE_USER_ENDSESSION',False)
# Create your models here.
User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)    # User instance
    ip_address = models.CharField(max_length=255, blank=True, null=True)                # Ip Address
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)             # Model Name : Product, Order, User, Cart, Address
    object_id = models.PositiveIntegerField()                                           # id of Models
    content_object = GenericForeignKey('content_type','object_id')                      # Model Instance
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "%s viewed on %s" %(self.content_object,self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)    # User instance
    ip_address = models.CharField(max_length=255, blank=True, null=True)                # Ip Address
    session_key = models.CharField(max_length=255, blank=True, null=True)                   # Model Instance
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active = False
            self.ended = True
            self.save()
        except:
            pass
        return self.ended




def post_save_session_receiver(sender,created,instance, *args, **kwargs):
    if created:
        qs = UserSession.objects.filter(user = instance.user,ended = False, active=True).exclude(id=instance)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver,sender = UserSession)


def post_save_user_changed_receiver(sender, instance, created, request, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user = instance.user, ended=False, active=True)
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)


#  Creating UserSession whenever user_logged_in signal is hitted 
def user_logged_in_receiver(sender,instance, request,*args, **kwargs):
    print(instance)
    user = instance
    session_key = request.session.session_key
    ip_address =get_client_ip(request)
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

user_logged_in.connect(user_logged_in_receiver)   




#  Creates ObjectViewed instance/object whenever object_viewed_signal is hitted which resides over ObjectViewedMixin class in mixin.py
def object_viewed_receiver( sender, instance, request, *args, **kwargs):
    # print(request)
    # print(instance)
    # print(sender)
    # print(request.user)
    c_type = ContentType.objects.get_for_model(sender)
    new_view_object = ObjectViewed.objects.create(
        user = request.user,
        ip_address = get_client_ip(request),
        object_id = instance.id,
        content_type = c_type,
    )


object_viewed_signal.connect(object_viewed_receiver)