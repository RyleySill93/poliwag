from django.urls import path

from . import views


urlpatterns = [
    path("create-presigned-post/", views.CreatePresignedUrlView.as_view()),
]
