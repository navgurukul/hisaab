#Routes for the HisaabApp

#Importing the files
from django.conf.urls import url
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    #routes for every user_type
    url(r'^$', views.home,name='home'),
    url(r'^access_denied/$', views.access_denied, name='access_denied'),
    url(r'^addexpense/$', views.addexpense,  name='addexpense'),
    url(r'^fellowreport/(?P<pk>\w+)$', views.fellowreport,  name='fellowreport'),
    url(r'^facilityreport/(?P<pk>\d+)$', views.facilityreport, name= 'facilityreport'),
    url(r'^register/$', views.register,  name='register'),
    url(r'^account/logout/$', logout,{'next_page':'/'}, name='logout',),

    #routes for the Ng Fellow
    url(r'^moneyrequest/$', views.moneytransferrequest, name='moneyrequest'),
    url(r'^utilityrequest/$', views.utilitybillrequest, name='utilityrequest'),
   
    #Routes for the both Admin and Super Admin
    url(r'^recordpayment/$', views.recordpayment,  name='recordpayment'),
    url(r'^viewpendingrequests/$', views.viewpendingrequests,  name='viewpendingrequests'),
    url(r'^searchfellow/$', views.searchfellow,  name='searchfellow'),
    url(r'^viewpendingrequest/(?P<pk>\d+)$', views.viewpendingrequest,  name='viewpendingrequest'),
    url(r'^detailrequest/(?P<pk>\d+)$', views.detailrequest,  name='detailrequest'),
    
    #Routes for the Super Admin
    url(r'^addfacility$', views.add_facility, name='addfacility',),
    url(r'^makeadmin/$', views.make_admin,  name='make_admin'),
]
# To save the static files in the media folder
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
