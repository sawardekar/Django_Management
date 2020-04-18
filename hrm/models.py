from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
# Create your models here.

GENDER_STATUS = (
    ('Male','Male'),
    ('Female','Female')
)


class Employee(models.Model):
    photo = models.ImageField(upload_to='document',blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True, unique=True)
    address = models.CharField(max_length=500, blank=True, null=True, unique=True)
    email = models.CharField(max_length=500, blank=True, null=True, unique=True)
    gender = models.TextField(choices=GENDER_STATUS, default='', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    mobile = models.BigIntegerField(unique=True, blank=True, null=True)
    status = models.NullBooleanField(default=True)
    credit = models.FloatField(blank=True, null=True,default=0.0)
    created_at = models.DateTimeField(blank=True, null=True, default=now)
    birth_date = models.DateField(blank=True, null=True)
    type = models.ForeignKey('EmployeeType', models.DO_NOTHING, blank=True, null=True)
    product = models.ManyToManyField('Product', blank=True, null=True)
    meta_data = JSONField(blank=True, null=True)
    production_user = ArrayField(models.CharField(max_length=500, blank=True, null=True), null=True, blank=True)

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.photo:
            return mark_safe('<img src="https://%s/media/%s" width="50" height="50" />' % (settings.AWS_S3_CUSTOM_DOMAIN, self.photo))
        else:
            return mark_safe('<img src="https://%s/media/document/default.jpg" width="50" height="50" />' % (settings.AWS_S3_CUSTOM_DOMAIN))

    image_tag.short_description = 'Image'


class EmployeeType(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    if instance.email:
        if instance.last_login:
            send_mail('Security Alert', 'Hello Sir,'
                                        '\n Your personal info has modified.'
                                        '\n please check it other wise contact to administration , Click on '
                                        f'{settings.BASE_URL}/admin'
                                        '\n do not reply',
                      settings.EMAIL_HOST_USER, [instance.email])
        else:
            send_mail('User Creation', 'Hello Sir,'
                                       '\n Welcome to xyz company.'
                                       '\n Please login offical portal, Click on '
                                       f'{settings.BASE_URL}/admin'
                                       '\n do not reply',
                      settings.EMAIL_HOST_USER, [instance.email])