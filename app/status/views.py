import json

from django.contrib import messages as message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import FormView, TemplateView, View

from .forms import ReservationForm
from .models import Gasoline, InsuranceContributer, Reservation, Status


class CarStatusView(LoginRequiredMixin, TemplateView):

    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_using"] = Status.objects.first().is_using
        # 現在時刻がend_timeを過ぎている予約を削除
        Reservation.objects.filter(end_time__lt=timezone.now()).delete()
        context["reservations"] = Reservation.objects.all()

        insurance_contributers = InsuranceContributer.objects.all()
        contributers_data = list(insurance_contributers.values("name", "total_paid"))
        context["insurance_contributers"] = json.dumps(contributers_data)

        # 現在がReservation.start_timeより後、Reservation.end_timeより前の時間ならcontext['is_reserved']をTrueにする
        for reservation in context["reservations"]:
            if reservation.start_time < timezone.now() < reservation.end_time:
                context["is_reserved"] = True
                break
        else:
            context["is_reserved"] = False
        return context


class StatusToggleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status = Status.objects.first()
        status.is_using = not status.is_using
        status.save()
        return redirect("status:home")


class ReservationView(LoginRequiredMixin, FormView):
    form_class = ReservationForm
    template_name = "reservation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reservations = Reservation.objects.all()
        events = []
        for reservation in reservations:
            local_start_time = timezone.localtime(reservation.start_time)
            local_end_time = timezone.localtime(reservation.end_time)
            events.append(
                {
                    "id": reservation.id,
                    "start_year": int(local_start_time.strftime("%Y")),
                    "start_month": int(local_start_time.strftime("%m")),
                    "start_day": int(local_start_time.strftime("%d")),
                    "start_hour": int(local_start_time.strftime("%H")),
                    "start_minute": int(local_start_time.strftime("%M")),
                    "end_year": int(local_end_time.strftime("%Y")),
                    "end_month": int(local_end_time.strftime("%m")),
                    "end_day": int(local_end_time.strftime("%d")),
                    "end_hour": int(local_end_time.strftime("%H")),
                    "end_minute": int(local_end_time.strftime("%M")),
                    "title": reservation.name,
                }
            )
        context["events"] = events
        return context

    def post(self, request, *args, **kwargs):
        form = ReservationForm(data=request.POST)
        if form.is_valid():
            # formの内容をReservationモデルに保存
            Reservation.objects.create(
                name=form.cleaned_data["name"],
                password=form.cleaned_data["password"],
                start_time=form.cleaned_data["start_date"],
                end_time=form.cleaned_data["end_date"],
            )
            return redirect("status:home")
        else:
            return render(request, self.template_name, {"form": form})


class DeleteReservationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=kwargs["pk"])
        password = request.POST.get("password")

        if password == reservation.password:
            reservation.delete()
            message.success(request, "予約を削除しました。")
        else:
            message.error(request, "パスワードが違います。")

        return redirect("status:home")


# ガソリンを入れたことを報告するビュー
class GasolineView(LoginRequiredMixin, TemplateView):
    template_name = "gasoline.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["gasolines"] = Gasoline.objects.all().order_by("-created_at")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = request.POST.get("user")
        price = request.POST.get("price")
        comment = request.POST.get("comment")
        gasoline = Gasoline(name=user, price=price, comment=comment)
        gasoline.save()
        return redirect("status:home")
