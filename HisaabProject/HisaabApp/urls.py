from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^account/logout/$', logout,{'next_page':'/'}, name='logout',),
    url(r'^moneyrequest/$', views.moneytransferrequest, name='moneyrequest'),
    url(r'^utilityrequest/$', views.utilitybillrequest, name='utilityrequest'),
    url(r'^access_denied/$', views.access_denied, name='access_denied'),
]
