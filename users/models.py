import uuid

from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractUser


# Create your models here.


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        public_id = username + str(uuid.uuid4())
        user = self.model(username=username, email=email, public_id=public_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUserModel(AbstractUser):
    email = models.EmailField("Email", blank=False, null=False, unique=True)
    public_id = models.CharField("Public user ID", max_length=60, blank=False, null=False, unique=True)
    last_request = models.DateTimeField("Last Request", blank=True, null=True)

    objects = CustomUserManager()
