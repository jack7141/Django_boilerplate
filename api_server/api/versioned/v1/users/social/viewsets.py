from abc import abstractmethod
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from django.utils import timezone

from api_server.api.versioned.v1.users.social.serializers.token_serializer import AccessTokenIssueSerializer, \
    AccessTokenSetNoProfileSerializer
from api_server.common.exceptions import InvalidSocialToken
from api_server.common.utils import get_client_ip
from api_server.oauth.models import LoginHistory
from api_server.users.models import User

class SocialOAuthViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = None
    serializer_class = None
    permission_classes = [permissions.AllowAny]
    
    # 플랫폼별 prefix 매핑
    platform_prefix_map = {}

    def get_platform_prefix(self, action_name):
        """액션 이름을 기반으로 플랫폼 prefix를 반환"""
        return self.platform_prefix_map.get(action_name, 'unknown')

    def social_id_by_platform(self, social_id, action_name=None):
        """플랫폼별로 social_id에 prefix를 추가"""
        if action_name:
            prefix = self.get_platform_prefix(action_name)
            return f'{prefix}-{social_id}'
        return str(social_id)

    def require_join_response(self, user_id):
        token_serializer = AccessTokenIssueSerializer(data={'user_id': user_id})
        token_serializer.is_valid(raise_exception=True)
        res_serializer = AccessTokenSetNoProfileSerializer(data=token_serializer.data)
        res_serializer.is_valid(raise_exception=True)
        print(res_serializer.data)
        return Response(res_serializer.data, status=status.HTTP_412_PRECONDITION_FAILED)

    def success_login_response(self, user):
        user.last_login = timezone.now()
        user.save()
        LoginHistory.objects.create(user=user, ip=get_client_ip(self.request))
        s = AccessTokenIssueSerializer(data={'user_id': user.id})
        s.is_valid(raise_exception=True)
        return Response(s.data, status=status.HTTP_201_CREATED)

    def success_login_and_require_join_response(self, social_id):
        username = self.social_id_by_platform(social_id, self.action)
        user = User.objects.create_user(username=username)
        self.get_queryset().create(user=user, social_id=social_id)
        return self.require_join_response(user.id)

    def handle_social_user(self, social_id):
        """소셜 ID로 사용자 로그인 처리 (공통 로직)"""
        obj = self.get_queryset().filter(social_id=social_id).first()
        try:
            if obj:
                if obj.user.has_profile:
                    return self.success_login_response(obj.user)
                else:
                    return self.require_join_response(obj.user_id)
            else:
                return self.success_login_and_require_join_response(social_id)
        except Exception as _:
            raise InvalidSocialToken