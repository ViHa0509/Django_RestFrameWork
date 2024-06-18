from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    joined_date = models.DateField(default=datetime.now, blank=True)
    phone = models.CharField(max_length=12)
    biography = models.TextField(blank=True)

    def __str__(self):
        return "{}\n{}".format(self.username, self.email)

CustomUser._meta.get_field('groups').remote_field.related_name='customer_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'customuser_user_permissions'