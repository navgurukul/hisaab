from django.conf.urls import url
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    url(r'^$', views.home,name='home'),
    url(r'^account/logout/$', logout,{'next_page':'/'}, name='logout',),
    url(r'^add_facility$', views.add_facility, name='add_facility',),
    url(r'^moneyrequest/$', views.moneytransferrequest, name='moneyrequest'),
    url(r'^utilityrequest/$', views.utilitybillrequest, name='utilityrequest'),
    url(r'^access_denied/$', views.access_denied, name='access_denied'),
    url(r'^addexpense/$', views.addexpense,  name='addexpense'),
    url(r'^fellowreport/(?P<pk>\w+)$', views.fellowreport,  name='fellowreport'),
    url(r'^facilityreport/(?P<pk>\d+)$', views.facilityreport, name= 'facilityreport'),
    url(r'^register/$', views.register,  name='register'),
    url(r'^recordpayment/$', views.recordpayment,  name='recordpayment'),
    url(r'^viewpendingrequests/$', views.viewpendingrequests,  name='viewpendingrequests'),
    url(r'^viewpendingrequest/(?P<pk>\d+)$', views.viewpendingrequest,  name='viewpendingrequest'),
    url(r'^addfacility/$', views.add_facility,  name='addfacility'),

]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
