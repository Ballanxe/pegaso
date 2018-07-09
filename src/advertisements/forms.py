from django import forms 

from .models import Advertisement



class AdvertisementCreateForm(forms.ModelForm):

	# email 				= forms.EmailField()
	# category				= forms.CharField(required=False, validators=[validate_category])

	class Meta:
		model = Advertisement
		fields = [

			'types',
			'currency',
			'location', 
			'price',
			'payment_method',
			'min_limit',
			'max_limit',
			'terms',
			'payment_data',


		]

		widgets = {
			'types': forms.RadioSelect(),
		}


		
class AdvertisementUpdateForm(forms.ModelForm):

	class Meta:

		model = Advertisement
		fields = [

			'currency',
			'location', 
			'price',
			'payment_method',
			'min_limit',
			'max_limit',
			'terms',
			'payment_data',


		]

		widgets = {
			'types': forms.RadioSelect(),
		}


