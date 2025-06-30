from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.managers import SoftDeletableManager
from model_utils.models import UUIDModel, SoftDeletableModel

from api_server.users.choices import MBTI_TYPE, IMAGE_SCALE, GENDER_TYPE


class UserManager(SoftDeletableManager, BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(UUIDModel, AbstractUser, SoftDeletableModel):
    user_id = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='사용자 검색 등에 사용되는 고유 아이디',
                               help_text='입력된 아이디는 고유한 값을 가짐. (중복불가)<br/>''또한 변경 가능하지만, 최종으로 사용된 아이디는 회원 탈퇴가 있더라도 재사용 할 수는 없음',
                               )
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    password = models.CharField(_('password'), max_length=128, null=True, blank=True)
    email = None
    first_name = None
    last_name = None

    is_confirm = models.BooleanField(default=False, verbose_name='약관 동의 유무')
    email = models.EmailField(_('email address'))
    EMAIL_FIELD = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    provider = models.CharField(max_length=10, null=True, blank=True)

    objects = UserManager(_emit_deprecation_warnings=True)

    @property
    def has_profile(self):
        return hasattr(self, 'profile')

    class Meta:
        verbose_name = '사용자 목록'
        verbose_name_plural = verbose_name
        constraints = [
            UniqueConstraint(
                fields=['email'],
                condition=Q(is_removed=False),
                name='unique_email_if_not_removed'
            ),
            UniqueConstraint(
                fields=['username'],
                condition=Q(is_removed=False),
                name='unique_username_if_not_removed'
            )
        ]



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='사용자')
    nickname = models.CharField(max_length=60, null=True, blank=True, verbose_name='사용자 닉네임')
    profile_image_link = models.URLField(max_length=255, null=True, blank=True, verbose_name='프로필 이미지 링크')
    gender = models.CharField(max_length=1, verbose_name='성별', null=True, blank=True, choices=GENDER_TYPE)
    birthday = models.DateTimeField(verbose_name='생일', null=True, blank=True, help_text='사주 컨텐츠를 활용하기 위해 시간까지 활용')
    mbti = models.CharField(max_length=4, null=True, blank=True, verbose_name='MBTI', choices=MBTI_TYPE)
    introduce = models.TextField(verbose_name='프로필 소개', null=True, blank=True)



class UserImage(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='images', verbose_name='프로필')
    image_url = models.URLField(max_length=255, verbose_name='이미지 URL')
    scale = models.CharField(max_length=10, choices=IMAGE_SCALE, verbose_name='이미지 스케일')

    class Meta:
        verbose_name = '사용자 이미지'
        verbose_name_plural = verbose_name