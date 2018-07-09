from django.contrib import admin

# Register your models here.

from .models import (
	Wallet,
	SendBitcoins,
	ReceiveBitcoins
)


admin.site.register(Wallet)
admin.site.register(SendBitcoins)
admin.site.register(ReceiveBitcoins)
