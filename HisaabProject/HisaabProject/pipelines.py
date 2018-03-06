from HisaabApp.models import NgUser 
from django.shortcuts import redirect

def save_profile(backend, user, response, *args, **kwargs):
	if backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		if new_user:
			nguser = NgUser(user_id=user.id)
			nguser.facility = Facility.objects.get(name = 'Dharamshala')
			nguser.save()
		