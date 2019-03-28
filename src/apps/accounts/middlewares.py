from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from apps.accounts.models import UserProfile
import json

User = get_user_model()


class WikilegisRemoteUser(RemoteUserMiddleware):
    header = "HTTP_AUTH_USER"

    # Override process request to pass the request to authentication method
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            return

        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated:
            cleaned_username = self.clean_username(username, request)
            if request.user.get_username() == cleaned_username:
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=username, request=request)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            user_data = json.loads(request.META['HTTP_REMOTE_USER_DATA'])
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.username = username
            if not hasattr(user, 'profile'):
                profile = UserProfile()
                profile.user = user
            else:
                profile = user.profile
            profile.avatar = user_data['avatar']
            profile.gender = user_data['gender']
            profile.uf = user_data['uf']
            profile.country = user_data['country']
            profile.birthdate = user_data['birthdate']
            profile.save()
            user.save()

            request.user = user
            auth.login(request, user)
