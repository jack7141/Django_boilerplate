from rest_framework import serializers


class GoogleVerificationSerializer(serializers.Serializer):
    id_token = serializers.CharField(label='Google Access ID Token', help_text='구글 연동 로그인시 발급 받은 `ID-token`')
