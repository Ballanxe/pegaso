from django.shortcuts import render, get_object_or_404, reverse

from django.http import Http404, HttpResponseRedirect

from django.views.generic import DetailView, UpdateView
from django.contrib import messages 

from django.utils.translation import ugettext_lazy as _

from .models import Profile

from .forms import ProfileUpdateForm

# Create your views here.


class ProfileDetailView(DetailView):

	template_name = 'profile_detail_view.html'

	def get_context_data(self, *args, **kwargs):

		context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)

		obj = self.get_object()

		user = self.request.user

		if obj.user.pk == user.pk:

			context = super(ProfileDetailView, self).get_context_data()

			context['updateable'] = True

		return context 

	def get_object(self):

		username = self.kwargs.get("username")

		if username is None:

			raise Http404

		return get_object_or_404(Profile, user__username=username)


class ProfileUpdatelView(UpdateView):

	template_name = 'profile_update_view.html'
	form_class = ProfileUpdateForm

	def form_valid(self, form):

		form.save()

		messages.success(self.request, _(f'Su perfil ha sido actualizado'))

		return HttpResponseRedirect(reverse('profiles:detail', kwargs={'username':self.request.user.username }))

	def get_context_data(self, *args, **kwargs):

		context = super(ProfileUpdatelView, self).get_context_data(*args, **kwargs)

		return context 


	def get_object(self):

		username = self.kwargs.get("username")

		if username is None:

			raise Http404
			
		return get_object_or_404(Profile, user__username=username)


