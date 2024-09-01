from django.contrib.auth.views import LoginView

from .forms import CustomLoginForm

# 基本共用の一つのユーザーをみんなで使う


class LoginView(LoginView):
    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True
