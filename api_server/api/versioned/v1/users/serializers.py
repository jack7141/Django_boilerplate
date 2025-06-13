from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, serializers

from api_server.common.utils import get_client_ip
from api_server.oauth.models import LoginHistory
from api_server.users.models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)
    provider = serializers.CharField(read_only=True)
    user_id = serializers.CharField()
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'profile', 'provider', 'created_at', 'user_id']


    def is_valid(self, raise_exception=False):
        if super().is_valid(raise_exception=raise_exception):
            user_id = self.validated_data['user_id']
            if user_id is None:
                raise serializers.ValidationError({'user_id': ['This field is required.']})

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context['request'].user
            profile_data = validated_data.pop('profile', {})
            user.last_login = timezone.now()
            user.save()
            LoginHistory.objects.create(user=user, ip=get_client_ip(self.context['request']), )
            UserProfile.objects.create(user=user, **profile_data)
            return user