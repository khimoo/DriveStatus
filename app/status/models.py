from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError


class Status(models.Model):
    is_using = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.is_using}"


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(default=timezone.now)

    def clean(self):
        # 予約が被っているかどうか
        overlapping_reservations = Reservation.objects.filter(
            start_time__lt=self.end_time,  # 終了時間が他の予約の開始時間より前
            end_time__gt=self.start_time  # 開始時間が他の予約の終了時間より後
        ).exclude(pk=self.pk)  # 自分自身のレコードは除外する

        if overlapping_reservations.exists():
            raise ValidationError('この時間帯はすでに予約されています。他の時間を選択してください。')

    def save(self, *args, **kwargs):
        self.clean()  # 保存前にバリデーションを実行する
        super().save(*args, **kwargs)
