from django.conf import settings
from api_server.api.versioned.v1.users.social.serializers import GoogleVerificationSerializer, KaKaoVerificationSerializer

from api_server.api.versioned.v1.users.social.viewsets import SocialOAuthViewSet
from api_server.common.exceptions import InvalidSocialToken, AlreadyJoined
from api_server.common.viewset import MappingViewSetMixin, QuerysetMapMixin
from api_server.oauth.models import AuthWithGoogle, AuthWithKakao, AuthWithNaver, AuthWithApple

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport.requests import Request

import requests

class AuthViewSet(MappingViewSetMixin, QuerysetMapMixin, SocialOAuthViewSet):
    """"""
    # queryset = AuthWithGoogle.objects.all()
    queryset_map = {
        "create_google": AuthWithGoogle.objects.all(),
        "create_kakao": AuthWithKakao.objects.all(),
        "create_naver": AuthWithNaver.objects.all(),
        "create_apple": AuthWithApple.objects.all(),
    }

    serializer_action_map = {
        "create_google": GoogleVerificationSerializer,
        "create_kakao": KaKaoVerificationSerializer,
    }
    # 플랫폼별 prefix 매핑
    platform_prefix_map = {
        "create_google": "google",
        "create_kakao": "kakao",
    }

    def create_google(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token = serializer.validated_data['id_token']
        google_credentials = verify_oauth2_token(id_token, Request(), settings.GOOGLE_OAUTH_AUDIENCE)
        google_id = google_credentials.get('sub')
        return self.handle_social_user(google_id)

    def create_kakao(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']
        res = requests.post(url='https://kapi.kakao.com/v2/user/me', headers={'Authorization': f'Bearer {access_token}'})
        kakao_id = res.json().get('id', None)
        if not kakao_id:
            raise InvalidSocialToken
        return self.handle_social_user(kakao_id)
