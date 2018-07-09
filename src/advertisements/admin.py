from django.contrib import admin

# Register your models here.
from .models import (
	Advertisement,
	Currencies,
	PaymentMethods
)


admin.site.register(Advertisement)
admin.site.register(Currencies)
admin.site.register(PaymentMethods)


