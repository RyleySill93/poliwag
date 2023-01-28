from django.db import models


class AppEvent(models.Model):
    id = models.UUIDField(primary_key=True)
    event_type = models.CharField(max_length=500)
    user_id = models.CharField(max_length=17, null=True, blank=True)
    payload = models.JSONField()
    payload_class = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["event_type"], name="idx_gl_event_event_type"),
        ]
