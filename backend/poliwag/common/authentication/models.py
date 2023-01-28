from django.db import models
from poliwag.common.models import BaseModel


class AuthPhoneChallenge(BaseModel):
    user = models.ForeignKey(
        "identity.User",
        related_name="auth_phone_challenges",
        on_delete=models.CASCADE,
    )
    code = models.IntegerField()
    num_attempts = models.SmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=["user"],
                name="active_pchal_per_user",
                condition=models.Q(is_active=True)
            ),
        )
