import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('username', 'email', 'is_superuser', 'is_staff',
                   'is_active', 'password')


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        exclude = ('profile_type',)
        convert_choices_to_enum = False


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    profiles = graphene.List(UserProfileType)
    user = graphene.Field(UserType,
                          id=graphene.Int(),
                          firstName=graphene.String())

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(is_active=True)

    def resolve_profiles(self, info, **kwargs):
        return UserProfile.objects.filter(user__is_active=True)

    def resolve_user(self, info, **kwargs):
          id = kwargs.get('id')
          name = kwargs.get('firstName')

          if id is not None:
              return User.objects.get(pk=id)

          if name is not None:
              return User.objects.get(first_name=name)

          return None
