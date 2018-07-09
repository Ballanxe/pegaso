from .base import *
from decouple import config


GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY', default='')

BLOCKCYPHER_TOKEN = config('BLOCKCYPHER_TOKEN', default='')

WALLET_PUBKEY = config('WALLET_PUBKEY', default='')

FERNET_KEY='abDz1nd63glph4MTPROXI5dQjsLKz58GvV0091ePM3U='

WALLET_PRIVKEY = config('WALLET_PRIVKEY', default='')