from django.contrib import admin

from .models import (Gasoline, InsuranceContributer, InsurancePayment,
                     Reservation, Status)

admin.site.register(Status)
admin.site.register(Reservation)
admin.site.register(Gasoline)
admin.site.register(InsuranceContributer)
admin.site.register(InsurancePayment)
