"""poliwag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from poliwag.common.views import APIStatusUrlView

from poliwag.common.authentication import views as auth_views
from poliwag.core.user import views as user_views


urlpatterns = [
    ### User
    path(
        "users/",
        include(
            [
                path(
                    "me/", user_views.GetCurrentUserView.as_view(), name="current-user"
                ),
            ]
        ),
    ),
    ### Authentication
    path(
        "auth/",
        include(        
            [
                path(
                    "email/generate/",
                    auth_views.GenerateEmailAuthView.as_view(),
                    name="gen-auth-email",
                ),
                path(
                    "email/<slug:uidb64>/<slug:token>/",
                    auth_views.AuthenticateEmailView.as_view(),
                    name="auth-email",
                ),
                path(
                    "phone/generate/",
                    auth_views.GeneratePhoneAuthView.as_view(),
                    name="gen-auth-phone",
                ),
                path(
                    "phone/",
                    auth_views.AuthenticatePhoneView.as_view(),
                    name="auth-phone",
                ),
                path(
                    "refresh/",
                    auth_views.TokenRefreshView.as_view(),
                    name="auth-refresh"
                )
            ]
        )
    ),
    # Health Check
    path("status/", APIStatusUrlView.as_view())
]
