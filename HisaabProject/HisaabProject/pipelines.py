from HisaabApp.models import * 
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

@partial
def add_facility(strategy,	backend, user,request, *args, **kwargs):
	# print request.session
	if backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		uid = kwargs['uid']
		super_admin_list=['a@navgurukul.org', 'r@navgurukul.org','amar17@navgurukul.org',]
		strategy.session_set('is_new', new_user)
		has_facility = strategy.session_get('facility', None)
		if new_user and not has_facility and not uid in super_admin_list:
			return redirect('register')

	return

@partial
def save_profile(strategy, backend, user, request, *args, **kwargs):
	facility = strategy.session_get('facility', None)
	if user and backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		uid = kwargs['uid']
		super_admin_list=['a@navgurukul.org', 'r@navgurukul.org','amar17@navgurukul.org',]
		if new_user and uid in super_admin_list:
			nguser = NgUser(user = user, user_type='SUPER_ADMIN')
			nguser.save()
			return {'nguser':nguser}
		elif new_user and facility:
			nguser = NgUser(user = user)
			nguser.facility = Facility.objects.get(id= facility)
			nguser.save()
			return {'nguser':nguser}

USER_FIELDS = ['username', 'email']

def create_user(strategy, details, backend, user=None, *args, **kwargs):
	uid = kwargs['uid']

	# if not uid.endswith('@navgurukul.org'):
	# 	print('return')
	# 	return False
	if user:
		return {'is_new': False}

	fields = dict((name, kwargs.get(name, details.get(name))) for name in backend.setting('USER_FIELDS', USER_FIELDS))
	if not fields:
		return

	return {
		'is_new': True,
		'user': strategy.create_user(**fields)
	}
