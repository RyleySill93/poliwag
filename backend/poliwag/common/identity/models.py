from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy
from poliwag.common.models import BaseModel


class User(AbstractUser, BaseModel):
    username = None
    password = None
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    phone = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
