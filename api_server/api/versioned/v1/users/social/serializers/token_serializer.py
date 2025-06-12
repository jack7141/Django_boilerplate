import datetime

from django.utils import timezone
from oauthlib.common import generate_token
from rest_framework import serializers

from api_server.users.models import User

from oauth2_provider.models import AccessToken, RefreshToken, Application
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.conf import settings

class AccessTokenIssueSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(allow_null=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True, allow_null=True,)
    expires_in = serializers.IntegerField(read_only=True)
    token_type = serializers.CharField(read_only=True)
    scope = serializers.CharField(read_only=True)

    def get_application():
        """OAuth2 Application 조회"""
        try:
            return Application.objects.get(name='Django API Server')
        except Application.DoesNotExist:
            raise ValidationError("OAuth2 Application이 설정되지 않았습니다.")

    def validate(self, attrs):
        user = get_object_or_404(User, id=attrs.get('user_id', None))
        application = Application.objects.filter(name='Django API Server').first()
        expires = getattr(settings, 'ACCESS_TOKEN_EXPIRES', 3600) - 2
        access_token = AccessToken.objects.create(
            user=user, token=generate_token(),
            expires=timezone.now() + datetime.timedelta(seconds=expires), scope='read write', application=application,
        )
        refresh_token = RefreshToken.objects.create(
            user=user, token=generate_token(), access_token=access_token, application=application,
        )
        AccessToken.objects.filter(user=user).exclude(id=access_token.id).delete()

        return {
            'access_token': access_token.token,
            'refresh_token': refresh_token.token,
            'expires_in': expires,
            'token_type': 'Bearer',
            'scope': access_token.scope,
            'user_id': str(user.id),
        }

    def to_representation(self, instance):
        """응답 데이터 형태로 변환"""
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)



class AccessTokenSetNoProfileSerializer(serializers.Serializer):
    access_token = serializers.CharField(label='인증 토큰', help_text='Authorization Bearer token', required=False)
    expires_in = serializers.IntegerField(label='유효 시간', help_text='`AccessToken` 발급 후 유효한 시간', required=False)
    token_type = serializers.CharField(label='토큰 유형', required=False)
    scope = serializers.CharField(label='허용 범위', required=False)

    class Meta:
        examples = {
            'accessToken': 'e1sBuLhJJPy5z2JuK3qKgv67rTZN25',
            'expiresIn': 3600,
            'tokenType': 'Bearer',
            'scope': 'read write',
        }
