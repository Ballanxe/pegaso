
from django import forms
from django.utils.translation import pgettext, ugettext, ugettext_lazy as _

from django.contrib.auth.forms import (
    # ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget,
    # PasswordResetForm as OldPasswordResetForm,
    # UserChangeForm as DjangoUserChangeForm,
    AuthenticationForm as DjangoAuthenticationForm,
    SetPasswordForm as DjangoSetPasswordForm
)
from django.contrib.auth.forms import PasswordResetForm as AuthPasswordResetForm
from authtools.forms import CaseInsensitiveUsernameFieldCreationForm



from core.utils import get_client_ip
from .models import User



class RegisterForm(CaseInsensitiveUsernameFieldCreationForm):
	pass

	# def save(self, commit=True):
	# 	# Save the provided password in hashed format
	# 	user = super(RegisterForm, self).save(commit=False)
	# 	user.activated = False

	# 	if commit:
	# 		affiliate.save()
	# 		affiliate.send_activation_email()
	# 	return affiliate
	


class AuthenticationForm(DjangoAuthenticationForm):

	username = forms.CharField(label=_('Email o nombre de usuario'))

	class Meta:
		widgets = {
			'email': forms.TextInput(attrs={'placeholder': _('Insert you email')}),
			'password': forms.TextInput(attrs={'placeholder': _('Insert your password')}),
		}


	def __init__(self, request=None, *args, **kwargs):
		super(AuthenticationForm, self).__init__(request, *args, **kwargs)
		username_field = User._meta.get_field(User.USERNAME_FIELD)
		self.fields['username'].widget = username_field.formfield().widget


class PasswordResetForm(AuthPasswordResetForm):
	pass
 


class SetPasswordForm(DjangoSetPasswordForm):
	pass


class UserUpdateForm(forms.ModelForm):

	class Meta:

		model = User
		fields = [

			'first_name',
			'last_name',

		]
