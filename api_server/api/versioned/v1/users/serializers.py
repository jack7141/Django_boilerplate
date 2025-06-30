from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, serializers

from api_server.common.utils import get_client_ip
from api_server.images.models import Images
from api_server.oauth.models import LoginHistory
from api_server.users.models import User, UserProfile

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ('content_type', 'object_id', 'created', 'modified')

class UserProfileSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    class Meta:
        model = UserProfile
        fields = ('user', 'nickname', 'gender', 'birthday', 'mbti', 'introduce', 'images')
        extra_kwargs = {
            'user': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)
    created = serializers.DateTimeField(source='date_joined', read_only=True)
    provider = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'profile', 'provider', 'created', 'user_id']


    def is_valid(self, raise_exception=False):
        if super().is_valid(raise_exception=raise_exception):
            user_id = self.validated_data['user_id']
            if user_id is None:
                raise serializers.ValidationError({'user_id': ['This field is required.']})

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context['request'].user
            profile_data = validated_data.pop('profile', {})
            images_data = profile_data.pop('images', [])
            user.last_login = timezone.now()
            user.save()
            LoginHistory.objects.create(user=user, ip=get_client_ip(self.context['request']), )
            profile = UserProfile.objects.create(user=user, **profile_data)
            profile.save()
            if images_data:
                for image_data in images_data:
                    profile.images.create(**image_data)
            return user