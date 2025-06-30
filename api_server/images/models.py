from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from api_server.users.choices import IMAGE_SCALE
from model_utils.models import TimeStampedModel

class Images(TimeStampedModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image_url = models.URLField(max_length=255, verbose_name='이미지 URL')
    scale = models.CharField(max_length=10, choices=IMAGE_SCALE, verbose_name='이미지 스케일')
    class Meta:
        verbose_name = '이미지'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
