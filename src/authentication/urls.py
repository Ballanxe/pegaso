from django.conf.urls import url

from authtools import views

from .views import (
	RegisterUserBigView, 
	LoginView, 
	LogoutView, 
	PasswordResetView, 
	PasswordResetConfirmView, 
	PasswordResetDoneView,
	PasswordResetCompleteView,
	ActivateAccountView,
	UserUpdateView,
)


urlpatterns = [

	url(
		r'^register/$',
		RegisterUserBigView.as_view(),
		name='register'
	),

	url(
		r'^login/$',
		LoginView.as_view(),
		name='login'
	),

	url(
		r'^update/(?P<pk>\d+)/$',
		UserUpdateView.as_view(),
		name='update'
	),

	url(
		r'^logout/$'
		, LogoutView.as_view(),
		name='logout'
	),
	url(
		r'^password-reset/$',
		PasswordResetView.as_view(),
		name='password_reset'
	),
	url(
		r'^password-reset/done/$',
		PasswordResetDoneView.as_view(),
		name='password_reset_done'
	),
	url(
		r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		PasswordResetConfirmView.as_view(),
		name='password_reset_confirm'
	),
	url(
		r'^reset/done/$',
		PasswordResetCompleteView.as_view(),
		name='password_reset_complete'
	),
	url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivateAccountView.as_view(), name='activate'),

###### This are for dashboard options conf.

# url(
# 	r'^password_change/$',
# 	PasswordChangeView.as_view(),
# 	name='password_change'
# ),
# url(
# r'^password_change/done/$',
# views.PasswordChangeDoneView.as_view(),
# name='password_change_done'
# ),



]