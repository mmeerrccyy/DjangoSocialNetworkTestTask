from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication

class LastRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        auth_header = request.headers.get('AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            auth = JWTAuthentication()
            user = auth.authenticate(request)[0]
            user.last_request = timezone.now()
            user.save()
            # Attach the user to the request
            request.user = user

        # Code to be executed for each request/response after
        # the view is called.
        response = self.get_response(request)

        return response
