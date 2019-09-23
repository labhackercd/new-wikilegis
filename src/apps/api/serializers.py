from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile, ThematicGroup
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
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'last_login', 'date_joined', 'profile', 'is_active',
                  'is_staff', 'is_superuser')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request', None)
        if request:
            api_key = request.GET.get('api_key', None)
            if api_key != settings.SECRET_KEY:
                ret.pop('email')
                ret.pop('is_active', None)
                ret.pop('is_staff', None)
                ret.pop('is_superuser', None)
        else:
            ret.pop('email')
            ret.pop('is_active', None)
            ret.pop('is_staff', None)
            ret.pop('is_superuser', None)
        return ret

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.is_active = validated_data.get('is_active',
                                                instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_superuser = validated_data.get('is_superuser',
                                                   instance.is_superuser)
        if not hasattr(instance, 'profile'):
            profile = UserProfile()
            profile.user = instance
        else:
            profile = instance.profile
        profile.avatar = validated_data.get('avatar', profile.avatar)
        profile.gender = validated_data.get('gender', profile.gender)
        profile.uf = validated_data.get('uf', profile.uf)
        profile.country = validated_data.get('country', profile.country)
        profile.birthdate = validated_data.get('birthdate', profile.birthdate)
        profile.save()
        instance.save()
        return instance


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ('id', 'title', 'initials')


class DocumentSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    document_type = DocumentTypeSerializer()
    themes = ThemeSerializer(many=True)
    pub_excerpts = serializers.SerializerMethodField('get_pub_excerpts')

    class Meta:
        model = Document
        fields = ('id', 'title', 'slug', 'description', 'document_type',
                  'number', 'year', 'themes', 'owner', 'pub_excerpts')

    def get_pub_excerpts(self, obj):
        pub_group = obj.invited_groups.filter(
            public_participation=True,
            group_status='in_progress').last()
        pub_excerpts = obj.excerpts.filter(
            version=pub_group.version)
        serializer = ExcerptSerializer(
            instance=pub_excerpts,
            many=True,
            context=self.context)

        return serializer.data


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

    excerpt_type = serializers.StringRelatedField()

    class Meta:
        model = Excerpt
        fields = ('id', 'document', 'parent', 'order', 'excerpt_type',
                  'number', 'content', 'suggestions')


class InvitedGroupSerializer(serializers.HyperlinkedModelSerializer):
    document = DocumentSerializer()
    suggestions_count = serializers.SerializerMethodField()

    class Meta:
        model = InvitedGroup
        fields = ('id', 'created', 'modified', 'closing_date', 'document',
                  'public_participation', 'suggestions_count')

    def get_suggestions_count(self, obj):
        return obj.suggestions.count()


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


class ThematicGroupSerializer(serializers.HyperlinkedModelSerializer):
    participants = UserSerializer(many=True)

    class Meta:
        model = ThematicGroup
        fields = ('id', 'name', 'participants')
