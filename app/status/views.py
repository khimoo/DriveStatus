from django.views.generic import View, TemplateView
from django.shortcuts import redirect
import datetime
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages as message
from django.utils.timezone import make_aware

from .models import Status, Reservation


class CarStatusView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['is_using'] = Status.objects.first().is_using
        # 現在時刻がend_timeを過ぎている予約を削除
        Reservation.objects.filter(end_time__lt=datetime.datetime.now()).delete()
        context['reservations'] = Reservation.objects.all()
        return context


class StatusToggleView(View):
    def get(self, request, *args, **kwargs):
        status = Status.objects.first()
        status.is_using = not status.is_using
        status.save()
        return redirect('api:status')


class ReservationView(TemplateView):
    template_name = 'reservation.html'

    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        password = request.POST.get('password')
        start_date = request.POST.get('start_date')
        start_time = request.POST.get('start_time')
        duration = int(request.POST.get('duration', 0))  # Ensure duration is an integer

        # Combine start_date and start_time into a single datetime object
        start_datetime_str = f'{start_date}T{start_time}'
        start_time = make_aware(parse_datetime(start_datetime_str))

        # Calculate end_time based on start_time and duration
        end_time = start_time + datetime.timedelta(minutes=duration)

        try:
            # Create Reservation object
            reservation = Reservation(
                user=user,
                password=password,
                start_time=start_time,
                end_time=end_time
            )
            reservation.save()
            return redirect('api:status')
        except ValidationError as e:
            return render(request, self.template_name, {
                'error_message': e.message,  # Pass the error message to the template
                'user': user,
                'password': password,
                'start_date': start_date,
                'start_time': start_time.strftime('%H:%M'),
                'duration': duration,
            })


class DeleteReservationView(View):
    def post(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=kwargs['pk'])
        password = request.POST.get('password')

        if password == reservation.password:
            reservation.delete()
            message.success(request, '予約を削除しました。')
        else:
            message.error(request, 'パスワードが違います。')

        return redirect('api:status')
