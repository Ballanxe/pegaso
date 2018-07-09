from datetime import datetime, timedelta

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import (

	AbstractBaseUser, BaseUserManager, PermissionsMixin	

)
from django.db import models
from core.models import TimestampedModel


class UserManager(BaseUserManager):
	"""
	Django requires that custom users define their own Manager class. By
	inheriting from `BaseUserManager`, we get a lot of the same code used by
	Django to create a `User`. 

	All we have to do is override the `create_user` function which we will use
	to create `User` objects.
	"""

	def create_user(self, username, email, password=None):
		"""Create and return a `User` with an email, username and password."""

		if username is None:
			raise TypeError('Users must have a username.')

		if email is None:
			raise TypeError('Users must have an email adress')


		user = self.model(username=username, email=self.normalize_email(email))
		user.set_password(password)
		user.save()

		return user

	def create_superuser(self, username, email, password):
		"""
		Create and return a `User` with superuser (admin) permissions.
		"""


		if password is None:
			raise TypeError('Superusers must have a password')

		user = self.create_user(username, email, password)
		user.is_superuser = True
		user.is_staff = True
		user.save()


		return user 

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):


	username = models.CharField(db_index=True, max_length=255, unique=True,validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9_]+$',
            message=_('Se permiten sólo números letras y _'),
            code='invalid_username'
        )])
	first_name = models.CharField(_('First name'), max_length=50, null=True, default=None, blank=True )
	last_name = models.CharField(_('Last name'), max_length=50, null=True, default=None, blank=True, unique=True)
	email = models.EmailField(db_index=True, unique=True)
	is_active = models.BooleanField(default=True)
	email_verification = models.DateTimeField(null=True)
	is_staff = models.BooleanField(default=False)



	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	objects = UserManager()

	def __str__(self):

		return self.email

	@property
	def token(self):
		"""
		Allows us to get a user's token by calling `user.token` instead of
		`user.generate_jwt_token().

		The `@property` decorator above makes this possible. `token` is called
		a "dynamic property".
		"""

		return self._generate_jwt_token()


	def get_full_name(self):

		return self.first_name, self.last_name

	def get_short_name(self):

		return self.username

	def email_user(self, subject, message, from_email=None, **kwargs):
	    """Send an email to this user."""
	    send_mail(subject, message, from_email, [self.email], **kwargs)

