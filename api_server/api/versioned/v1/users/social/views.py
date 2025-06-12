from django.conf import settings

from rest_framework import viewsets
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from api_server.api.versioned.v1.users.social.serializers.google_serializer import GoogleVerificationSerializer
from api_server.api.versioned.v1.users.social.viewsets import SocialOAuthViewSet
from api_server.oauth.models import AuthWithGoogle

from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport.requests import Request


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    status: 상태 체크

    Kibana Heartbeat 상태 체크용 API 입니다.
    """
    permission_classes = [AllowAny, ]
    serializer_class = Serializer

    def status(self, request, *args, **kwargs):
        return Response(status=HTTP_200_OK)

class AuthViewSet(SocialOAuthViewSet):
    """"""
    queryset = AuthWithGoogle.objects.all()
    serializer_class = GoogleVerificationSerializer

    def social_id_by_platform(self, social_id):
        return f'google-{social_id}'

    def create_google(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = serializer.validated_data['access_token']
        google_credentials = verify_oauth2_token(access_token, Request(), settings.GOOGLE_OAUTH_AUDIENCE)
        google_id = google_credentials.get('sub')
        obj = self.get_queryset().filter(social_id=google_id).first()