from django.conf.urls import url
from django.contrib.auth.views import logout
from . import views
urlpatterns = [
    url(r'^$', views.home),
    url(r'^account/logout/$', logout,{'next_page':'/'}, name='logout',),
]
