from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.projects.models import Theme, DocumentType, Document
from apps.api import serializers as api_serializers


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'name', 'slug')


class ProfileSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'gender', 'uf', 'country', 'birthdate', 'avatar',
                  'profile_type', 'themes')


class UserSerializer(serializers.ModelSerializer):
    profile = api_serializers.ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'last_login', 'date_joined', 'profile')

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        request = self.context.get('request', None)
        if request:
            api_key = request.GET.get('api_key', None)
            if api_key != settings.SECRET_KEY:
                ret.pop('email')
        else:
            ret.pop('email')
        return ret


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'title', 'initials')


class DocumentSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    document_type = DocumentTypeSerializer()
    themes = ThemeSerializer(many=True)

    class Meta:
        model = Document
        fields = ('id', 'title', 'slug', 'description', 'document_type',
                  'number', 'year', 'themes', 'owner')
