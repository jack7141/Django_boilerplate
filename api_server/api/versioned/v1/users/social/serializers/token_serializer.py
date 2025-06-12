import datetime

from django.utils import timezone
from oauthlib.common import generate_token
from rest_framework import serializers

from api_server.users.models import User

from oauth2_provider.models import AccessToken, RefreshToken
from django.shortcuts import get_object_or_404
from django.conf import settings

class AccessTokenIssueSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(allow_null=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True, allow_null=True,)
    expires_in = serializers.IntegerField(read_only=True)
    token_type = serializers.CharField(read_only=True)
    scope = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = get_object_or_404(User, id=attrs.get('user_id', None))
        expires = settings.ACEESS_TOKEN_EXPIRES - 2
        access_token = AccessToken.objects.create(
            user=user, token=generate_token(),
            expires=timezone.now() + datetime.timedelta(seconds=expires), scope='read write'
        )
        refresh_token = RefreshToken.objects.create(
            user=user, token=generate_token(), access_token=access_token
        )
        print(f'access token id : {access_token.id}')
        AccessToken.objects.filter(user=user).exclude(id=access_token.id).delete()

        attrs['access_token'] = access_token.token
        attrs['refresh_token'] = refresh_token.token
        attrs['expires_in'] = expires

        attrs['token_type'] = 'Bearer'
        attrs['scope'] = access_token.scope
        return attrs

    def to_res_dict(self):
        res_data = {
            'access_token': self.data.get('access_token'),
            'refresh_token': self.data.get('refresh_token'),
            'expires_in': self.data.get('expires_in'),
            'token_type': 'Bearer',
            'scope': 'read write',
            'user_id': self.data.get('user_id'),
        }
        return res_data



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
