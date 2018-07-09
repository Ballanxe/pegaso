from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from blockcypher import create_wallet_from_address

from profiles.models import Profile
from wallets.models import Wallet

from .models import User 
from core.utils import get_payment_adress_for_user

@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):

	# Notice that we're checking for `created` here. We only want to do this
	# the first time the `User` instance is created. If the save that caused
	# this signal to be run was an update action, we know the user already
	# has a profile.

	if instance and created:
		instance.profile = Profile.objects.create(user=instance)

		new_wallet = get_payment_adress_for_user(instance)

		wallet = create_wallet_from_address(wallet_name=instance.username, address=new_wallet['address'], api_key=settings.BLOCKCYPHER_TOKEN, coin_symbol=settings.COIN)

		instance.wallet = Wallet.objects.create(
			profile=instance.profile,
			receiving_address=new_wallet['address'],
			private = new_wallet['priv'],
			reg_private=new_wallet['reg_priv']

		)


