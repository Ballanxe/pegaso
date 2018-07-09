from django import forms 

from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):

	# email 				= forms.EmailField()
	# category				= forms.CharField(required=False, validators=[validate_category])

	class Meta:

		model = Profile
		fields = [

			'language',
			'phone',


		]


		widgets = {

			'phone': PhoneNumberPrefixWidget()

		}