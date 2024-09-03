import requests
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Status(models.Model):
    is_using = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.is_using}"


class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # 予約が被っているかどうか
        overlapping_reservations = Reservation.objects.filter(
            start_time__lt=self.end_time,  # 終了時間が他の予約の開始時間より前
            end_time__gt=self.start_time,  # 開始時間が他の予約の終了時間より後
        ).exclude(
            pk=self.pk
        )  # 自分自身のレコードは除外する

        if overlapping_reservations.exists():
            raise ValidationError(
                "この時間帯はすでに予約されています。他の時間を選択してください。"
            )

    def save(self, *args, **kwargs):
        self.clean()  # 保存前にバリデーションを実行する
        super().save(*args, **kwargs)


# ガソリンをいれてくれた人の名前と金額を記録するモデル


class Gasoline(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.price}円"


class InsuranceContributer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    total_paid = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class InsurancePayment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(InsuranceContributer, on_delete=models.CASCADE)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.price}円"

    def save(self, *args, **kwargs):
        if self.pk is None:
            # 新規追加の場合は合計に加算
            self.name.total_paid += self.price
        else:
            # 既存のレコード更新時の処理
            old_payment = InsurancePayment.objects.get(pk=self.pk)
            self.name.total_paid -= old_payment.price
            self.name.total_paid += self.price
        self.name.save()  # InsuranceContributerの合計を更新
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # 削除時に合計から減算
        self.name.total_paid -= self.price
        self.name.save()
        super().delete(*args, **kwargs)


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            discord_info = DiscordIntegration.objects.first()
            if discord_info.is_discord_notification_enabled:
                if discord_info.is_announcement_notification_enabled:
                    url = f"https://discordapp.com/api/channels/{discord_info.discord_channel_id}/messages"
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bot {discord_info.discord_bot_token}",
                    }
                    data = {
                        "content": f"掲示板が更新されました\n{self.title}\n{self.content}"
                    }
                    requests.post(url, headers=headers, json=data)
        except:
            pass


class DiscordIntegration(models.Model):
    id = models.AutoField(primary_key=True)
    discord_bot_token = models.CharField(max_length=100)
    discord_channel_id = models.CharField(max_length=100)
    is_discord_notification_enabled = models.BooleanField(default=False)
    is_status_notification_enabled = models.BooleanField(default=False)
    is_reservation_notification_enabled = models.BooleanField(default=False)
    is_gasoline_notification_enabled = models.BooleanField(default=False)
    is_announcement_notification_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
