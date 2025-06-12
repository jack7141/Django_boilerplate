from rest_framework import serializers


class GoogleVerificationSerializer(serializers.Serializer):
    access_token = serializers.CharField(label='Google Access Token', help_text='구글 연동 로그인시 발급 받은 `Access-token`')
