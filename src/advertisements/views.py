from itertools import chain
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib import messages 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _

from django_filters.views import FilterView

from .filters import AdvertisementFilter
from .forms import AdvertisementCreateForm, AdvertisementUpdateForm
from .models import Advertisement
from .models import Currencies
from .models import PaymentMethods

# Create your views here.

class AdvertisementHomeView(FilterView):

	template_name = 'index.html'
	filterset_class = AdvertisementFilter
	count = 0


	def get_context_data(self, *args, **kwargs):

		request = self.request

		context = super(AdvertisementHomeView, self).get_context_data(*args, **kwargs)

		context['results'] = self.filterset_class(request.GET, queryset=Advertisement.objects.all())

		buy_qs = Advertisement.objects.filter(types='buy_online').all().order_by('created_at')

		sell_qs = Advertisement.objects.filter(types='sell_online').all().order_by('created_at')
		
		context['buy_objects'] = buy_qs
		context['sell_objects'] = sell_qs

		return context




class AdvertisementCreateView(LoginRequiredMixin,CreateView):

	template_name= 'ads_create_view.html'
	form_class= AdvertisementCreateForm

	def form_valid(self, form):

		instance = form.save(commit=False)

		instance.owner = self.request.user

		instance.save()

		messages.success(self.request, _(f'La publicación ha sido creada satisfactoriamente'))

		return HttpResponseRedirect(reverse('ads:my_list'))


class BuyAdvertisementListView(ListView):

	template_name= 'buy_ads_list_view.html'

	def get_queryset(self):

		return Advertisement.objects.filter(types='buy_online')


class SellAdvertisementListView(ListView):

	template_name= 'sell_ads_list_view.html'

	def get_queryset(self):

		return Advertisement.objects.filter(types='sell_online')


class AdvertisementDetailView(DetailView):

	template_name = 'ads_detail_view.html'

	def get_object(self):

		pk = self.kwargs.get("pk")

		if pk is None:

			raise Http404
			
		return get_object_or_404(Advertisement, pk=pk)


class AdvertisementPrivateListView(LoginRequiredMixin,ListView):

	template_name= 'private_ads_list_view.html'

	def get_queryset(self):

		return Advertisement.objects.filter(owner=self.request.user).order_by('-created_at')


class AdvertisementUpdateView(LoginRequiredMixin, UpdateView):

	template_name="ads_update_view.html"
	form_class = AdvertisementUpdateForm


	def form_valid(self, form):

		form.save()

		messages.success(self.request, _(f'La publicacion ha sido actualizada'))

		return HttpResponseRedirect(reverse('ads:my_list'))

	def get_context_data(self, *args, **kwargs):

		context = super(AdvertisementUpdateView, self).get_context_data(*args, **kwargs)

		return context 


	def get_object(self):

		pk = self.kwargs.get("pk")

		if pk is None:

			raise Http404
			
		return get_object_or_404(Advertisement, pk=pk)


