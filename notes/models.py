from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Note(models.Model):
    title = models.CharField(
        verbose_name='заголовок',
        max_length=50,
        blank=False,
    )
    note = models.TextField(
        verbose_name='примечание',
        blank=True,
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
