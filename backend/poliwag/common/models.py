from django.db import models
from poliwag.common.nanoid import NanoId


class BaseQuerySet(models.QuerySet):
    ...


class BaseManager(models.Manager):
    ...


class BaseModel(models.Model):
    objects = BaseManager()

    id = models.CharField(
        primary_key=True, max_length=NanoId._CHAR_SIZE, default=NanoId.gen
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
