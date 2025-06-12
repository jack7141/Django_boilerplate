from abc import abstractmethod
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.response import Response

from django.utils import timezone

from api_server.api.versioned.v1.users.social.serializers.token_serializer import AccessTokenIssueSerializer, \
    AccessTokenSetNoProfileSerializer
from api_server.oauth.models import LoginHistory
from api_server.users.models import User

class SocialOAuthViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = None
    serializer_class = None
    permission_classes = [permissions.AllowAny]

    @abstractmethod
    def social_id_by_platform(self, social_id):
        return

    @staticmethod
    def require_join_response(user_id):
        token_serializer = AccessTokenIssueSerializer(data={'user_id': user_id})
        token_serializer.is_valid(raise_exception=True)
        res_serializer = AccessTokenSetNoProfileSerializer(data=token_serializer.data)
        res_serializer.is_valid(raise_exception=True)
        return Response(res_serializer.data, status=status.HTTP_412_PRECONDITION_FAILED)

    def success_login_response(self, user):
        user.last_login = timezone.now()
        user.save()
        LoginHistory.objects.create(user=user, ip=get_client_ip(self.request))
        s = AccessTokenIssueSerializer(data={'user_id': user.id})
        s.is_valid(raise_exception=True)
        return Response(s.to_res_dict(), status=status.HTTP_201_CREATED)

    def success_login_and_require_join_response(self, social_id):
        user = User.objects.create_user(username=self.social_id_by_platform(social_id))
        self.queryset.create(user=user, social_id=social_id)
        return self.require_join_response(user.id)
