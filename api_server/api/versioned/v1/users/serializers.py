from rest_framework import viewsets, serializers
from api_server.users.models import User

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)
    nickname = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    provider = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(source='date_joined', read_only=True)
    birthday = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'nickname', 'email', 'provider', 'created_at', 'birthday']

    def get_nickname(self, obj):
        """사용자 이름 반환"""
        if hasattr(obj, 'profile') and obj.profile and obj.profile.nickname:
            return obj.profile.nickname
        return 'Google User'

    def get_email(self, obj):
        """사용자 이메일 반환"""
        if hasattr(obj, 'profile') and obj.profile and obj.profile.email:
            return obj.profile.email
        return ''

    def get_provider(self, obj):
        """소셜 로그인 제공자 반환"""
        if hasattr(obj, 'auth_google'):
            return 'google'
        elif hasattr(obj, 'auth_kakao'):
            return 'kakao'
        elif hasattr(obj, 'auth_naver'):
            return 'naver'
        elif hasattr(obj, 'auth_apple'):
            return 'apple'
        return 'google'  # 기본값

    def get_birthday(self, obj):
        """생일 반환"""
        if hasattr(obj, 'profile') and obj.profile and obj.profile.birthday:
            return obj.profile.birthday
        return None

