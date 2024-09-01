from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # is_mainがTrueの場合、他のユーザーのis_mainをFalseにする
        if self.is_main:
            CustomUser.objects.filter(is_main=True).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
