from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    level = models.IntegerField(verbose_name="user level")
    email = models.EmailField(null=True, blank=True)

    REQUIRED_FIELDS = [""]


class Referral(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who invites others
    referred_users = models.JSONField(default=list)  # List of referred user IDs


class UserPasswords(models.Model):
    user_id = models.BigIntegerField(unique=True)  # Using Telegram chat ID as unique identifier
    password = models.CharField(max_length=128)  # Password field

    def __str__(self):
        return f"User ID: {self.user_id}"
