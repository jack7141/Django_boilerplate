from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.managers import SoftDeletableManager
from model_utils.models import UUIDModel, SoftDeletableModel


GENDER_TYPE = Choices(
    ('M', 'MALE', '남자'),
    ('F', 'FEMALE', '여자'),
    ('U', 'OTHER', '미제공'),
)

IMAGE_SCALE = Choices(
    ('RAW', 'RAW', '원본'),  # 원본
    ('DETAIL', 'DETAIL', '상세'),  # 상세보기
    ('NORMAL', 'NORMAL', '일반'),  # 일반
    ('THUMBNAIL', 'THUMBNAIL', '미리보기'),  # 미리보기
)

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

    @property
    def has_profile(self):
        return hasattr(self, 'profile')

    class Meta:
        verbose_name = '사용자 목록'
        verbose_name_plural = verbose_name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='사용자')
    nickname = models.CharField(max_length=60, null=True, blank=True, verbose_name='사용자 닉네임')
    link = models.URLField(max_length=255, null=True, blank=True, verbose_name='개인 사이트 링크')
    email = models.EmailField(verbose_name='사용자 이메일', null=True, blank=True)
    gender = models.CharField(max_length=1, verbose_name='성별', null=True, blank=True, choices=GENDER_TYPE)
    birthday = models.DateField(verbose_name='생일', null=True, blank=True)
    introduce = models.TextField(verbose_name='프로필 소개', null=True, blank=True)

    @property
    def image_sets(self):
        images_by_scale = {}
        for img in self.images.all():
            if img.scale in images_by_scale:
                continue
            images_by_scale[img.scale] = img

        # 이미지를 가져오면서 대체 이미지 처리
        raw = images_by_scale.get(IMAGE_SCALE.RAW)
        detail = images_by_scale.get(IMAGE_SCALE.DETAIL) or raw
        normal = images_by_scale.get(IMAGE_SCALE.NORMAL) or detail
        thumbnail = images_by_scale.get(IMAGE_SCALE.THUMBNAIL) or normal

        return {
            'RAW': raw,
            'DETAIL': detail,
            'NORMAL': normal,
            'THUMBNAIL': thumbnail,
        }
