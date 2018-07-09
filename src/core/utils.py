from bitmerchant.wallet import Wallet
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from blockcypher import create_wallet_from_address
from bitmerchant.network import BlockCypherTestNet 
from cryptography.fernet import Fernet



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        remoteip = x_forwarded_for.split(',')[0]
    else:
        remoteip = request.META.get('REMOTE_ADDR')
    return remoteip



def get_payment_adress_for_user(user):

	user_id = user.id

	

	# assert isinstance(user_id, (int,long))

	wallet = Wallet.deserialize(settings.WALLET_PRIVKEY, network=BlockCypherTestNet)
	wallet_for_user = wallet.get_child(user.id, is_prime=True)

	my_wallet = {
		'address':wallet_for_user.to_address(),
		'priv':get_encripted_priv(wallet_for_user),
		# 'reg_priv': wallet_for_user.serialize_b58(private=True)
		'reg_priv': wallet_for_user.get_private_key_hex().decode('UTF-8')
	}

	return my_wallet




def get_encripted_priv(wallet): 

	a = wallet 
	
	priv = a.get_private_key_hex()


	key = settings.FERNET_KEY
	f = Fernet(key.encode('UTF-8'))
	token = f.encrypt(priv)

	return token.decode('UTF-8')

def get_desencrypted_priv(priv):

	priv = priv.encode('UTF-8')

	key = settings.FERNET_KEY
	f = Fernet(key.encode('UTF-8'))

	enc = f.decrypt(priv)

	return enc.decode('UTF-8')
	

def get_satoshis(inp):

	out = float(inp) * (10**8)

	return out 


def get_bitcoins(inp):

	out = float(inp) / (10**8)

	return "{0:.8f}".format(out)


def get_full_transactions(inp, addrs=None):

    transactions = []

    for i in range(len(inp)):

        tran = inp[i]

        fees = tran.get('fees', None)

        confirmed = tran.get('confirmed', None)

        inputs = tran.get('inputs', None)

        outputs = tran.get('outputs', None)

        value = outputs[0].get('value', None)

        receiver_output_list = outputs[0].get('addresses', None)

        receiver = receiver_output_list[0]

        if addrs and receiver == addrs:

        	is_receiver = True
        else:
        	is_receiver = False 

        sender_output_list = outputs[1].get('addresses', None)

        sender = sender_output_list[0]

        lista = inputs[0].get('addresses', None)

        address = lista[0]

        tran['sender'] = sender

        tran['receiver'] = receiver 

        tran['value'] = get_bitcoins(value)

        tran['fees'] = get_bitcoins(fees)

        tran['is_receiver'] = is_receiver

        tran['confirmed'] = confirmed if confirmed else _('Sin confirmar')

        transactions.append(tran)

    return transactions


