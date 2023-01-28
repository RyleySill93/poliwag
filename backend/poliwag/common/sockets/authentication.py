import logging
from http import cookies
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


logger = logging.getLogger(__name__)


class SimpleJWTAuthMiddlewareAsync:
    """
    JWT Middleware that matches our api authentication and sets authenticated
    users in the scope
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope["headers"])
        # @TODO Probably should never leave this middleware if user is not authenticated
        if b"cookie" in headers:
            try:
                jwt = self._get_jwt_value(self.scope)
                validated_token = JWTAuthentication().get_validated_token(jwt)
                self.scope["user"] = await self._get_user(validated_token)
            except InvalidToken:
                logger.info("Unauthenticated user attempt to connect to socket!")
                self.scope["user"] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)

    def _get_jwt_value(self, scope):
        try:
            cookie = next(
                x for x in scope["headers"] if x[0].decode("utf-8") == "cookie"
            )[1].decode("utf-8")
            return cookies.SimpleCookie(cookie)["jwt"].value
        except BaseException:
            return None

    @database_sync_to_async
    def _get_user(self, validated_token):
        return JWTAuthentication().get_user(validated_token=validated_token)


class SimpleJWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return SimpleJWTAuthMiddlewareAsync(scope, self)


def SimpleJWTAuthMiddlewareStack(inner):
    return SimpleJWTAuthMiddleware(AuthMiddlewareStack(inner))
