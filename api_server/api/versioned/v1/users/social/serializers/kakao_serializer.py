from rest_framework import serializers

class KaKaoVerificationSerializer(serializers.Serializer):
    access_token = serializers.CharField(label='KaKao Access ID Token', help_text='카카오 연동 로그인시 발급 받은 `access-token`')