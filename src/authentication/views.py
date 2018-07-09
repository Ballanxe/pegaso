import requests
import datetime

from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import authenticate, login
from django.views.generic import FormView, TemplateView, View, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages, auth
from django.utils.encoding import force_text


from authtools.views import (
	LoginView as AuthLoginView, 
	LogoutView as AuthLogoutView, 
	PasswordResetView as AuthPasswordResetView,
	PasswordResetConfirmView as AuthPasswordResetConfirmView,
	PasswordResetCompleteView as AuthPasswordResetCompleteView
)

from .tokens import account_activation_token
from .forms import RegisterForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, UserUpdateForm
from .models import User

# Create your views here.



class RegisterUserBigView(FormView):

	form_class = RegisterForm
	template_name = 'registration_view.html'
	# success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
	# initial = {
	# 	'usernaname': "Hola, como te llamas",
	# 	'email': "Hola email buenas tardes"
	# }


	def get_context_data(self, *args, **kwargs):
		form = self.form_class(self.request.POST)

		return super(RegisterUserBigView, self).get_context_data()


	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		recaptcha_response = self.request.POST.get('g-recaptcha-response')
		data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result = r.json()
		''' End reCAPTCHA validation '''

		#Recaptcha validationg 

		if result['success']:

			user = form.save()
			email = self.request.POST['email']
			password = self.request.POST['password1']
			user = authenticate(username=email, password=password)
			auth.login(self.request, user)

			# Sending Verification Email

			current_site = get_current_site(self.request)
			subject = 'Activate Account'
			message = render_to_string('account_activation_email.html', {
			    'user': user,
			    'domain': current_site.domain,
			    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			    'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			messages.info(self.request, _('Te enviamos un email para que verifiques tu direccion de correo'))

			next_url = self.request.POST.get('next','/')

			if next_url:
				return HttpResponseRedirect(next_url)
			else:
				return HttpResponseRedirect(reverse('home'))

		else:
			messages.error(self.request, 'Invalid reCAPTCHA. Please try again.')

		return HttpResponseRedirect(reverse('home'))
			


		

class LoginView(AuthLoginView):

	form_class = AuthenticationForm
	authentication_form = None
	template_name = 'login_view.html'
	allow_authenticated = True


	def form_invalid(self, form):
	    form = self.form_class(self.request.POST)
	    # response = 
	    # This method is called when valid form data has been POSTed.
	    # It should return an HttpResponse.
	    # print(form)
	    return super(LoginView, self).form_invalid(form)

	def get_context_data(self, *args, **kwargs):
		form = self.form_class(self.request.POST)


		return super(LoginView, self).get_context_data()


	def form_valid(self, form):
		# This method is called when valid form data has been POSTed.
		# It should return an HttpResponse.
		recaptcha_response = self.request.POST.get('g-recaptcha-response')
		data = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
		}
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
		result = r.json()
		''' End reCAPTCHA validation '''

		#Recaptcha validationg 

		if result['success']:

			return super(LoginView, self).form_valid(form)
		else:
			messages.error(self.request, _('Invalid reCAPTCHA. Please try again.'))
			return HttpResponseRedirect(reverse('auth:login'))

		return super(RegisterUserBigView, self).form_valid(form)



class LogoutView(AuthLogoutView):
	pass




class PasswordResetView(AuthPasswordResetView):

	template_name = 'password_reset_view.html'
	success_url = reverse_lazy('auth:password_reset_done')
	form_class = PasswordResetForm
	email_template_name = 'password_reset_email.html'

class PasswordResetDoneView(TemplateView):

	template_name = 'password_reset_done_view.html'


class PasswordResetConfirmView(AuthPasswordResetConfirmView):

	template_name = 'password_reset_confirm_view.html'
	form_class = SetPasswordForm
	success_url = reverse_lazy('auth:password_reset_complete')
	post_reset_login = False
	post_reset_login_backend = None


class PasswordResetCompleteView(AuthPasswordResetCompleteView):

	template_name = 'password_reset_complete_view.html'



class ActivateAccountView(View):


    def get(self, request, uidb64, token):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):

            user.email_verification = datetime.datetime.now()
            user.save()

            login(request, user)
            messages.error(self.request, _('Tu cuenta ha sido activada'))
            return HttpResponseRedirect(reverse('home'))

        else:
            # invalid link
            return render(request, 'registration/invalid.html')

class UserUpdateView(UpdateView):

	template_name = 'user_update_view.html'
	form_class = UserUpdateForm

	def form_valid(self, form):

		form.save()

		messages.success(self.request, _(f'Su perfil ha sido actualizado'))

		return HttpResponseRedirect(reverse('profiles:detail', kwargs={'username':self.request.user.username }))

	def get_context_data(self, *args, **kwargs):

		context = super(UserUpdateView, self).get_context_data(*args, **kwargs)

		return context 


	def get_object(self):

		pk = self.kwargs.get("pk")

		if pk is None:

			raise Http404
			
		return get_object_or_404(User, pk=pk)
