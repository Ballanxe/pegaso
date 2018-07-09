from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages 

from enum import Enum


from core.models import TimestampedModel

# Create your models here.


class Advertisement(TimestampedModel):

	class TYPES(Enum):

		sell_online			= ('sell_online', _('Vender sus bitcoins online'))
		buy_online 			= ('buy_online', _('Comprar bitcoins online'))


		@classmethod
		def get_value(cls, member):
			return cls[member].value[0]

	owner = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name = 'owner', default='')
	currency = models.ForeignKey('advertisements.Currencies', on_delete=models.CASCADE, related_name = 'currencies', null=False)
	types = models.CharField(max_length=25,choices=[x.value for x in TYPES],default=TYPES.get_value('sell_online'))
	location = models.CharField(max_length=50, null=True, default="", blank=True)
	price = models.DecimalField(max_digits=16,decimal_places=8,default=0)
	payment_method = models.ForeignKey('advertisements.PaymentMethods', on_delete=models.CASCADE, related_name = 'payment_methods', null=False, default='')
	min_limit = models.DecimalField(max_digits=16,decimal_places=8,default=0)
	max_limit = models.DecimalField(max_digits=16,decimal_places=8,default=0)
	terms = models.TextField()
	payment_data = models.TextField()
	is_active = models.BooleanField(default=True)

	# objects = AdvertisementManager()

	def get_limits(self):

		return "{} - {}".format(self.min_limit, self.max_limit)

	def get_active(self):

		if not self.is_active:

			return _(f'Esta publicacion esta desactivada')

	def get_is_active(self):

		return self.is_active


	def get_button_tag(self):

		if self.types == 'buy_online':

			return _('Comprar')

		if self.types == 'sell_online':

			return _('Vender')



class Currencies(models.Model):

	country = models.CharField(max_length=255)
	iso = models.CharField(max_length=255)


	def __str__(self):
		return self.iso




class PaymentMethods(models.Model):

	name = models.CharField(max_length=255)


	def __str__(self):
		return self.name