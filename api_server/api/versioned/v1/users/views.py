from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer

from api_server.api.versioned.v1.users.serializers import UserSerializer

from api_server.api.versioned.v1.users.social.serializers import AccessTokenIssueSerializer
from api_server.common.exceptions import AlreadyJoined
from api_server.common.viewset import MappingViewSetMixin
from api_server.users.models import User

class UserViewSet(MappingViewSetMixin, viewsets.ModelViewSet):
    """
    사용자 정보 ViewSet
    
    인증된 사용자의 정보를 조회합니다.
    """
    queryset = User.objects.select_related('profile')
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    serializer_action_map = {
        "logout": Serializer
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