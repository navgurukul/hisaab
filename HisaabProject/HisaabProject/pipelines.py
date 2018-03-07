from HisaabApp.models import * 
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

@partial
def add_facility(strategy, 	backend, user,request, *args, **kwargs):
	# print request.session
	if backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		strategy.session_set('is_new', new_user)

		has_facility = strategy.session_get('facility', None)
		if new_user and not has_facility:
			return redirect('register')

	return 

@partial
def save_profile(strategy, backend, user, request, *args, **kwargs):
	facility = strategy.session_get('facility', None)
	if backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		print user
		if new_user and facility: 
			nguser = NgUser(user = user)
			nguser.facility = Facility.objects.get(id= facility)
			nguser.save()	
			return {'nguser':nguser}
	