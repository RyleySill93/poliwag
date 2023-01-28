from django.db import models

from poliwag.common.models import BaseModel


class Document(BaseModel):
    id = models.UUIDField(primary_key=True)
    file_name = models.CharField(max_length=1000)
    s3_key = models.CharField(max_length=1000)
    namespace = models.CharField(max_length=1000)
    is_public = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey(
        "identity.User",
        related_name="documents",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
