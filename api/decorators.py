import jwt
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from functools import wraps
from django.contrib.auth import get_user_model
import ReportInsa.settings as settings
# Dictionary mapping error codes to user-friendly messages
ERROR_MESSAGES = {
    'missing_token': 'Authentication token is missing. Please log in.',
    'invalid_token_format': 'Invalid authentication token format. Please log in again.',
    'token_expired': 'Your session has expired. Please log in again.',
    'invalid_token': 'Invalid authentication token. Please log in again.',
    'user_not_found': 'User not found. Please log in again.'
}

def jwt_auth_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        print(request.headers,request.body)
        bearer_token = request.headers.get('Authorization')
        if not bearer_token:
            raise AuthenticationFailed(ERROR_MESSAGES['missing_token'], code='missing_token')

        try:
            _, token = bearer_token.split()
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except ValueError as e:
            
            raise AuthenticationFailed(ERROR_MESSAGES['invalid_token_format'], code='invalid_token_format')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(ERROR_MESSAGES['token_expired'], code='token_expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed(ERROR_MESSAGES['invalid_token'], code='invalid_token')

        User = get_user_model()
        user = User.objects.filter(uid=payload.get('uid')).first()
        if not user:
            raise AuthenticationFailed(ERROR_MESSAGES['user_not_found'], code='user_not_found')

        request.user = user  # Attach user to request object for easy access in view
        return view_func(request, *args, **kwargs)

    return wrapped_view
