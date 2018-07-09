"""pegaso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from wallets.views import (
    SendBitcoinsCreateView,
    TransactionsListView,
    ReceiveBitcoinsTemplateView,

) 

from profiles.views import (

    ProfileDetailView,
    ProfileUpdatelView,
)

from advertisements.views import (

    AdvertisementCreateView,
    SellAdvertisementListView,
    BuyAdvertisementListView,
    AdvertisementDetailView,
    AdvertisementPrivateListView,
    AdvertisementUpdateView, 
    AdvertisementHomeView,

)



advertisements_patterns = [
    
    path('ad/create', AdvertisementCreateView.as_view(), name='create'),
    path('ad/buy', BuyAdvertisementListView.as_view(), name='buy'),
    path('ad/sell', SellAdvertisementListView.as_view(), name='sell'),
    re_path(r'^ads/(?P<pk>\d+)/$', AdvertisementDetailView.as_view(), name='detail'),
    re_path(r'^ads/edit/(?P<pk>\d+)/$', AdvertisementUpdateView.as_view(), name='update'),
    path('ads/', AdvertisementPrivateListView.as_view(), name='my_list'),


]



wallets_patterns = [

    path('accounts/wallet', SendBitcoinsCreateView.as_view(), name='send'),
    path('accounts/transactions', TransactionsListView.as_view(), name='transactions'),
    path('accounts/wallet-receive', ReceiveBitcoinsTemplateView.as_view(), name='receive'),
    # path('accounts/wallet-transactions', TransactionsListView.as_view(), name='transactions'),

]

profile_patterns = [

    re_path(r'^accounts/profile/(?P<username>[\w.@+-]+)/$', ProfileDetailView.as_view(), name='detail'),
    re_path(r'^accounts/update/(?P<username>[\w.@+-]+)/$', ProfileUpdatelView.as_view(), name='update'),

]


urlpatterns = [
    # path('', search, name='home'),
    path('', AdvertisementHomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('', include(('authentication.urls','authentication'), namespace='auth')),
    path('', include((profile_patterns,'profiles'), namespace='profiles')),
    path('', include((wallets_patterns,'wallets'), namespace='wallets')),
    path('', include((advertisements_patterns,'advertisements'), namespace='ads'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)