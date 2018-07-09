import requests


from django.shortcuts import render,reverse

from django.views.generic import CreateView, ListView, TemplateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _ 
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blockcypher import get_address_overview, simple_spend, get_address_full
from cryptography.fernet import Fernet

from .forms import SendBitcoinsCreateForm
from .models import Wallet, SendBitcoins
from core.utils import get_desencrypted_priv, get_satoshis, get_bitcoins, get_full_transactions
# Create your views here.


class SendBitcoinsCreateView(LoginRequiredMixin,CreateView):

	template_name = 'send_bitcoins_view.html'
	form_class = SendBitcoinsCreateForm

	def form_valid(self, form):

		temp = form.cleaned_data['amount']

		amount = get_satoshis(temp)
		to_wallet = form.cleaned_data['to_wallet']
		description = form.cleaned_data['description']
		context = self.get_context_data()
		wallet = context['wallet']
		priv = get_desencrypted_priv(wallet.private)
		# get_desencrypted_priv(wallet.private)

		# try:


		tx = simple_spend(
			from_privkey=priv, 
			to_address=to_wallet, 
			to_satoshis=int(amount), 
			coin_symbol=settings.COIN,
			api_key=settings.BLOCKCYPHER_TOKEN
		)

		if tx: 
			
			instance = form.save(commit=False)
			address_info = get_address_overview(wallet.receiving_address, coin_symbol=settings.COIN)
			instance.wallet = wallet
			instance.amount = get_bitcoins(amount)
			instance.to_wallet = to_wallet
			instance.description = description
			instance.tx_ref = tx
			instance.save()

			wallet.balance = get_bitcoins(float(address_info['balance']))
			wallet.save()

			messages.success(self.request, _(f'Congrats'))


		# except Exception as e:

		# 	if e == 'Build Unsigned TX Error':

		# 		messages.error(self.request, _("Transaccion invalida."))

		# 	messages.error(self.request, _("Algo extraño ha sucedido. Por favor chequea los datos"))
			


		return HttpResponseRedirect(reverse('wallets:send'))



	def get_context_data(self, *args, **kwargs):

		context = super(SendBitcoinsCreateView, self).get_context_data(*args, **kwargs)
		context['wallet'] = Wallet.objects.get(profile=self.request.user.profile)
		wallet = context['wallet']

		# try:

		

		address_info = get_address_overview(wallet.receiving_address, coin_symbol=settings.COIN)



		# Obtengo el balance de la respuesta de Blockcypher luego de comision de 

		wallet.balance=get_bitcoins(float(address_info['balance']))

		wallet.save()

		# Muestra la clave privad desencriptada 
		# context['priv'] = get_desencrypted_priv(wallet.private)

		# except:

		# 	messages.success(self.request, _(f'Could not get the balance'))

		return context 




class TransactionsListView(LoginRequiredMixin,TemplateView):

	template_name = 'transactions_list_view.html'

	def get_context_data(self, *args, **kwargs):

		context = super(TransactionsListView, self).get_context_data(*args, **kwargs)

		context['wallet'] = Wallet.objects.get(profile=self.request.user.profile)
		wallet = context['wallet']

		address_full = get_address_full(address=wallet.receiving_address, txn_limit=50, coin_symbol=settings.COIN)

		transactions = address_full['txs']

		context['transactions'] = get_full_transactions(transactions,addrs=wallet.receiving_address) 
		context['unconfirmed'] = get_bitcoins(address_full['unconfirmed_balance'])
		context['final_n_tx'] = address_full['final_n_tx']
		context['unconfirmed_n'] = address_full['unconfirmed_n_tx']

		paginator = Paginator(context['transactions'], 10)

		page = self.request.GET.get('page')
		context['transactions'] = paginator.get_page(page)


		return context


	


class ReceiveBitcoinsTemplateView(LoginRequiredMixin,TemplateView):

	template_name = 'receive_bitcoins_view.html'

	def get_context_data(self, *args, **kwargs):

		context = super(ReceiveBitcoinsTemplateView, self).get_context_data(*args, **kwargs)
		context['wallet'] = Wallet.objects.get(profile=self.request.user.profile)
		wallet = context['wallet']


		return context 
