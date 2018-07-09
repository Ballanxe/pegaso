from django.apps import AppConfig

class AuthenticationAppConfig(AppConfig):

	name = 'authentication'
	label = 'authentication'
	verbose_name = 'Authentication'

	def ready(self):

		#This method is commonly used to register signals 

		import authentication.signals


default_app_config = 'authentication.AuthenticationAppConfig'