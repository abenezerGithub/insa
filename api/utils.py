import jwt
import datetime
from django.conf import settings
    
def generatetoken(user):

    token = jwt.encode({
        'uid': user.uid,
        'email': user.email,
        'iat':datetime.datetime.now(),
        'exp': datetime.datetime.now() + datetime.timedelta(days=1)
    }, settings.SECRET_KEY, algorithm='HS256')
    return token