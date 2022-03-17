from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Note(models.Model):
    title = models.CharField(
        verbose_name='заголовок',
        max_length=50,
        blank=False,
    )
    note = RichTextUploadingField(
        verbose_name='заметка',
        blank=True,
        null=True,
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    created = models.DateField(
        default=timezone.now,
        verbose_name='дата создания',
    )

    def __str__(self):
        return f'{self.title}'
