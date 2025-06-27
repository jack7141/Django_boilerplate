from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer
from oauth2_provider.models import RefreshToken, AccessToken
from api_server.api.versioned.v1.users.serializers import UserSerializer

from api_server.api.versioned.v1.users.social.serializers import AccessTokenIssueSerializer, \
    AccessTokenRefreshSerializer
from api_server.common.exceptions import AlreadyJoined, RefreshTokenHasExpired
from api_server.common.viewset import MappingViewSetMixin
from api_server.users.models import User

from django.shortcuts import get_object_or_404
from django.conf import settings

import requests
from django.utils import timezone
from datetime import timedelta


class UserViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    """
    사용자 정보 ViewSet
    
    인증된 사용자의 정보를 조회합니다.
    """
    queryset = User.objects.select_related('profile')
    permission_classes = [IsAuthenticated, ]
    permission_classes_map = {
        "refresh_token": [AllowAny, ],
    }
    serializer_class = UserSerializer
    serializer_action_map = {
        "logout": Serializer,
        "refresh_token": AccessTokenRefreshSerializer,
    }

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


    def me(self, request, *args, **kwargs):
        """현재 로그인한 사용자 정보 반환"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def logout(self, request, *args, **kwargs):
        auth = request.auth
        auth.revoke()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def refresh_token(self, request, *args, **kwargs):
        url = f'{settings.BASE_URL}/oa/token/'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']

        prev_token = get_object_or_404(RefreshToken, token=refresh_token)
        prev_access = prev_token.access_token

        data = {
            'client_id': settings.APPLICATION_WEB_AUTH_CLIENT_ID,
            'client_secret': settings.APPLICATION_WEB_AUTH_CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }

        user = prev_access.user
        res = requests.post(url=url, data=data, timeout=5)
        res.raise_for_status()
        json = res.json()

        prev_token.revoke()
        new_token = AccessToken.objects.get(token=json.get('access_token'))

        # conf 대신 상수 사용 (예: 24시간)
        ACCESS_TOKEN_EXPIRES = 24 * 3600  # 24시간을 초 단위로
        new_token.expires = timezone.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRES)
        new_token.save()

        json['user_id'] = user.id
        json['expires_in'] = ACCESS_TOKEN_EXPIRES
        return Response(json, status=status.HTTP_200_OK)
