import django_filters 

from .models import Advertisement
from .models import Currencies
from .models import PaymentMethods



class AdvertisementFilter(django_filters.FilterSet):

	types = django_filters.ChoiceFilter(choices=[x.value for x in Advertisement.TYPES])
	currency = django_filters.ModelChoiceFilter(queryset=Currencies.objects.all(), empty_label=None)
	payment_method = django_filters.ModelChoiceFilter(queryset=PaymentMethods.objects.all(), empty_label=None)
	max_limit = django_filters.NumberFilter(lookup_expr='gt', label='Cantidad')


	class Meta:

		model = Advertisement
		fields = ['types','currency', 'payment_method', 'max_limit' ]


	# @property
	# def qs(self):

	# 	parent = super(AdvertisementFilter, self).qs
		
	# 	return parent




	# @property
	# def qs(self):
	# 	parent = super(ArticleFilter, self).qs
	# 	author = getattr(self.request, 'user', None)

	# 	return 


	# def __init__(self, *args, **kwargs):
	# 	self.queryset = None

