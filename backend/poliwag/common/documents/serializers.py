from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = (
            "id",
            "file_name",
            "s3_key",
            "namespace",
            "uploaded_by_id",
            "is_public",
        )
