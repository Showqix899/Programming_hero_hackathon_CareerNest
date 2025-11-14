# careerbot_realtime/middleware.py
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user_from_token(token_key):
    # Import inside the function to avoid AppRegistryNotReady
    from django.contrib.auth.models import AnonymousUser
    from django.contrib.auth import get_user_model
    from rest_framework.authtoken.models import Token  # or your JWT logic

    User = get_user_model()
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Lazy import here too
        from django.contrib.auth.models import AnonymousUser

        query_params = parse_qs(scope["query_string"].decode())
        token = query_params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(inner)
