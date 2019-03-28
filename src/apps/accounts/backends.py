from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth import get_user_model
from apps.accounts.models import UserProfile
import json
UserModel = get_user_model()


class WikilegisAuthBackend(RemoteUserBackend):

    def authenticate(self, request, remote_user):
        if not remote_user:
            return
        user = None
        remote_user_data = json.loads(
            request.META.get('HTTP_REMOTE_USER_DATA')
        )
        user, created = UserModel.objects.get_or_create(
            email=remote_user_data['email']
        )
        user.username = remote_user
        user.first_name = remote_user_data['first_name']
        user.last_name = remote_user_data['last_name']
        if not hasattr(user, 'profile'):
            profile = UserProfile()
            profile.user = user
        else:
            profile = user.profile
        profile.avatar = remote_user_data['avatar']
        profile.gender = remote_user_data['gender']
        profile.uf = remote_user_data['uf']
        profile.country = remote_user_data['country']
        profile.birthdate = remote_user_data['birthdate']
        profile.save()
        user.save()

        return user
