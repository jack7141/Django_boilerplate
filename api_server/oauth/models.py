from django.conf import settings
from django.db import models, transaction
from django.db.models import GenericIPAddressField
from encrypted_fields.fields import SearchField, EncryptedCharField
from model_utils.models import UUIDModel, TimeStampedModel

from api_server.users.models import User


class EncryptedIpAddressField(EncryptedCharField, GenericIPAddressField):
    pass

class AbstractSocialAuth(models.Model):
    social_id = models.CharField(max_length=127, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True


class AuthWithKakao(AbstractSocialAuth):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_kakao')

    def __str__(self):
        return f'카카오 연동 ({self.social_id})'

    class Meta:
        db_table = 'users_auth_with_kakao'


class AuthWithNaver(AbstractSocialAuth):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_naver')

    class Meta:
        db_table = 'users_auth_with_naver'
        verbose_name = '네이버 인증 내역'
        verbose_name_plural = verbose_name


class AuthWithGoogle(AbstractSocialAuth):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_google')
    class Meta:
        db_table = 'users_auth_with_google'
        verbose_name = '구글 인증 내역'
        verbose_name_plural = verbose_name
        pass

class AuthWithApple(AbstractSocialAuth):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='auth_apple')

    class Meta:
        db_table = 'users_auth_with_apple'
        verbose_name = 'Apple 인증 내역'
        verbose_name_plural = verbose_name


class LoginHistory(UUIDModel, TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='login_histories')
    _ip = EncryptedIpAddressField(null=False, blank=False)
    ip = SearchField(verbose_name='접속 IP', encrypted_field_name='_ip', hash_key=settings.ENC_FIELD_KEY_1)

    class Meta:
        db_table = 'users_login_history'
        verbose_name = '로그인 내역'
        verbose_name_plural = verbose_name
        ordering = ['-created']
