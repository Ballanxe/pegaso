from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from core.models import TimestampedModel


# Create your models here.


class Wallet(TimestampedModel):

	profile = models.OneToOneField('profiles.Profile', on_delete=models.CASCADE, related_name='wallet')
	receiving_address = models.CharField(max_length=255)
	# transaction_number = models.IntegerField()
	private = models.CharField(max_length=255,default='')
	reg_private = models.CharField(max_length=255,default='')
	balance = models.DecimalField(max_digits=16,decimal_places=8,default=0)
	sent_transactions_30 = models.ForeignKey('wallets.SendBitcoins', on_delete=models.CASCADE, related_name = 'sent_transactions', null=True)
	received_transactions_30 = models.ForeignKey('wallets.ReceiveBitcoins',on_delete=models.CASCADE, related_name = 'receive_transactions', null=True)

	def __str__(self):

		return '{} - {} Wallet'.format(self.receiving_address,self.profile.user.username)

	def get_balance(self):

		return "{} BTC".format(self.balance)




class SendBitcoins(TimestampedModel):

	wallet = models.ForeignKey('wallets.Wallet',on_delete=models.CASCADE,related_name = 'send_wallet' )
	tx_ref = models.CharField(max_length=255,null=True, default='')
	amount = models.DecimalField(_('BTC'),max_digits=16,decimal_places=8, null=False)
	to_wallet = models.CharField(max_length=255,null=True, default='')
	description = models.TextField(_('Description'),null=True)

	# def clean(self):

	# 	# Prevents user to transfer to local addresses

	# 	if  Wallet.objects.filter(receiving_address=self.to_wallet).exists():

	# 		raise ValidationError(_("No puedes transferir a carteras locales"), code='invalid')





class ReceiveBitcoins(TimestampedModel):

	from_wallet = models.CharField(max_length=255)
	amount = models.DecimalField(max_digits=8,decimal_places=8)



# class Transactions(models.Model):

# 	sender = OneToOneField('wallets.SendBitcoins'. c)
# 	receiver = 


