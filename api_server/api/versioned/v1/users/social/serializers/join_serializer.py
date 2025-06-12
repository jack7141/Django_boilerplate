from django.db import transaction
from django.utils import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_server.common.utils import get_client_ip
from api_server.oauth.models import LoginHistory
from api_server.users.models import UserProfile, User



class JoinSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
    user_id = serializers.CharField(
        allow_null=False,
        label='외부에 노출되는 고유아이디',
        help_text='아이디는 검색등에 사용되는 사용자의 고유 아이디로 중복이 허용되지 않음, `alphanumeric` only',
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.all_objects.exclude(user_id=None))],
    )
    nickname = serializers.CharField()
    email = serializers.EmailField()
    birthday = serializers.DateField()
    def validate(self, attrs):
        user = self.context['request'].user
        self.user = user
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user_id = validated_data.pop('user_id', None)
            nickname = validated_data.pop('nickname', None)
            birthday = validated_data.pop('birthday', None)

            self.user.last_login = timezone.now()
            self.user.user_id = user_id

            LoginHistory.objects.create(user=self.user, ip=get_client_ip(self.context['request']),)
            profile = UserProfile.objects.create(user=self.user, nickname=nickname, birthday=birthday)
            self.user.save()
            return profile

    class Meta:
        examples = {
            'userId': 'helloworlduser'
        }
