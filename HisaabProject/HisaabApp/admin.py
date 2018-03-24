from django.contrib import admin
from django.contrib.auth.models import User

from .models import*

# Register your models here.
admin.site.register(NgUser)
admin.site.register(Facility)
admin.site.register(CashEntry)
admin.site.register(MoneyRequest)
