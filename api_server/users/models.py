from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.managers import SoftDeletableManager
from model_utils.models import UUIDModel, SoftDeletableModel


# Create your models here.

class UserManager(SoftDeletableManager, BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username,)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(UUIDModel, AbstractUser, SoftDeletableModel):
    user_id = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='사용자 검색 등에 사용되는 고유 아이디',
                               help_text='입력된 아이디는 고유한 값을 가짐. (중복불가)<br/>''또한 변경 가능하지만, 최종으로 사용된 아이디는 회원 탈퇴가 있더라도 재사용 할 수는 없음',
                               )
    password = models.CharField(_('password'), max_length=128, null=True, blank=True)
    email = None
    first_name = None
    last_name = None

    is_confirm = models.BooleanField(default=False, verbose_name='약관 동의 유무')

    EMAIL_FIELD = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager(_emit_deprecation_warnings=True)

    class Meta:
        verbose_name = '사용자 목록'
        verbose_name_plural = verbose_name