from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from api_server.api.versioned.v1.users.serializers import UserSerializer
from api_server.users.models import User

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    사용자 정보 ViewSet
    
    인증된 사용자의 정보를 조회합니다.
    """
    queryset = User.objects.select_related('profile')
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer

    def me(self, request, *args, **kwargs):
        """현재 로그인한 사용자 정보 반환"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def logout(self, request, *args, **kwargs):
        auth = request.auth
        auth.revoke()
        return Response(status=status.HTTP_204_NO_CONTENT)