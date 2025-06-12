from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, mixins
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK
from rest_framework import status

from api_server.api.versioned.v1.users.social.serializers.google_serializer import GoogleVerificationSerializer
from api_server.api.versioned.v1.users.social.serializers.join_serializer import JoinSerializer
from api_server.api.versioned.v1.users.social.serializers.kakao_serializer import KaKaoVerificationSerializer
from api_server.api.versioned.v1.users.social.serializers.token_serializer import AccessTokenIssueSerializer
from api_server.api.versioned.v1.users.social.viewsets import SocialOAuthViewSet
from api_server.common.exceptions import InvalidSocialToken, AlreadyJoined
from api_server.common.viewset import MappingViewSetMixin
from api_server.oauth.models import AuthWithGoogle

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport.requests import Request

from api_server.users.models import UserProfile, User


class UserAuthViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = UserProfile.objects.all()
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='회원 가입',
        operation_description='소셜 로그인 후 LingPick 서비스에서 필요한 일부 양식을 입력 하여 회원 가입 시 호출. '
                              '회원 가입이 되어있지 않으면 소셜 로그인으로 서비스 이용이 불가',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AuthViewSet(MappingViewSetMixin, SocialOAuthViewSet):
    """"""
    queryset = AuthWithGoogle.objects.all()
    # 플랫폼별 prefix 매핑
    platform_prefix_map = {
        "create_google": "google",
        "create_kakao": "kakao",
    }
    serializer_action_map = {
        "create_google": GoogleVerificationSerializer,
        "create_kakao": KaKaoVerificationSerializer,
    }

    def create_google(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_token = serializer.validated_data['id_token']
        google_credentials = verify_oauth2_token(id_token, Request(), settings.GOOGLE_OAUTH_AUDIENCE)
        google_id = google_credentials.get('sub')
        obj = self.get_queryset().filter(social_id=google_id).first()
        try:
            if obj:
                if obj.user.has_profile:
                    return self.success_login_response(obj.user)
                else:
                    return self.require_join_response(obj.user_id)
            else:
                return self.success_login_and_require_join_response(google_id)
        except Exception as _:
            raise InvalidSocialToken

    def create_kakao(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']
        import requests
        res = requests.post(
            url='https://kapi.kakao.com/v2/user/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        kakao_id = res.json().get('id', None)
        if not kakao_id:
            raise InvalidSocialToken

        obj = self.get_queryset().filter(social_id=kakao_id).first()
        try:
            if obj:
                if obj.user.has_profile:
                    return self.success_login_response(obj.user)
                else:
                    return self.require_join_response(obj.user_id)
            else:
                return self.success_login_and_require_join_response(kakao_id)
        except Exception as _:
            raise InvalidSocialToken



class UserJoinViewSet(UserAuthViewSet):
    serializer_class = JoinSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='회원 가입',
        operation_description='소셜 로그인 후 서비스에서 필요한 일부 양식을 입력 하여 회원 가입 시 호출하여 회원의 profile 데이터를 채움. '
                              '회원 가입이 되어있지 않으면 소셜 로그인으로 서비스 이용이 불가',
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.has_profile:
            raise AlreadyJoined

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data.get('user_id')
        if User.objects.filter(user_id=user_id).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer.save()

        s = AccessTokenIssueSerializer(data={'user_id': user.id})
        s.is_valid(raise_exception=True)
        return Response(s.data, status=status.HTTP_201_CREATED)