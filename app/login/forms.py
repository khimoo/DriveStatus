from django.contrib.auth.forms import AuthenticationForm
from django.forms import HiddenInput
from django.http import HttpResponse

from .models import CustomUser


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        main_user = CustomUser.objects.filter(is_main=True).first()
        if main_user:
            self.fields["username"].initial = main_user.username
            self.fields["username"].widget = HiddenInput()
        else:
            HttpResponse("メインユーザーが存在しません")
