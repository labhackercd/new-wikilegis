from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.projects.models import Theme, DocumentType, Document, Excerpt
from apps.participations.models import InvitedGroup, Suggestion, OpinionVote


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('id', 'name', 'slug', 'color')


class ProfileSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'gender', 'uf', 'country', 'birthdate', 'avatar',
                  'profile_type', 'themes')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'last_login', 'date_joined', 'profile')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
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
    excerpts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='excerpt-detail'
    )

    class Meta:
        model = Document
        fields = ('id', 'title', 'slug', 'description', 'document_type',
                  'number', 'year', 'themes', 'owner', 'excerpts')


class ExcerptSerializer(serializers.ModelSerializer):
    document = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='document-detail'
    )
    parent = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='excerpt-detail'
    )
    suggestions = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='suggestion-detail'
    )

    class Meta:
        model = Excerpt
        fields = ('id', 'document', 'parent', 'order', 'excerpt_type',
                  'number', 'content', 'suggestions')


class InvitedGroupSerializer(serializers.HyperlinkedModelSerializer):
    document = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='document-detail'
    )

    class Meta:
        model = InvitedGroup
        fields = ('id', 'created', 'modified', 'closing_date', 'document',
                  'public_participation')


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):
    excerpt = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='excerpt-detail'
    )
    author = UserSerializer()
    votes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='opinionvote-detail'
    )

    class Meta:
        model = Suggestion
        fields = ('id', 'created', 'modified', 'excerpt', 'start_index',
                  'end_index', 'content', 'author', 'votes')


class OpinionVoteSerializer(serializers.HyperlinkedModelSerializer):
    suggestion = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='suggestion-detail'
    )
    owner = UserSerializer()

    class Meta:
        model = OpinionVote
        fields = ('id', 'created', 'modified', 'suggestion', 'opinion_vote',
                  'owner')
