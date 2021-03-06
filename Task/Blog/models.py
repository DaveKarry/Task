from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.urls import reverse


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    subscribers = models.ManyToManyField("NewUser", blank=True)
    seen_posts = models.ManyToManyField("Post", blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("userblog", kwargs={
            'username': self.username
        })

    def get_subscribe_absolute_url(self):
        return reverse("subscribe", kwargs={
            'username': self.username
        })

    def get_unsubscribe_absolute_url(self):
        return reverse("unsubscribe", kwargs={
            'username': self.username
        })


class Post(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    author = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.author}'s ({self.title}) from _{self.posted_date}_"

    def get_absolute_url(self):
        return reverse("getpost", kwargs={
            'id': self.id
        })

    def get_seen_url(self):
        return reverse("seen", kwargs={
            'id': self.id
        })
