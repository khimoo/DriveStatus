from django.views.generic import TemplateView

# 基本共用の一つのユーザーをみんなで使う
class LoginView(TemplateView):
    template_name = 'login.html'
