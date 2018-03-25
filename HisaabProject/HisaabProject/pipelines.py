#Pipeline for Using while Social Authentication

#importing the files
from HisaabApp.models import * 
from django.shortcuts import redirect
from social_core.pipeline.partial import partial

#partial pipeline for adding a new facility
@partial
def add_facility(strategy,	backend, user,request, *args, **kwargs):

	#block for google-oauth2 signup
	if backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		uid = kwargs['uid']
		super_admin_list=['a@navgurukul.org', 'r@navgurukul.org','amar17@navgurukul.org',]
		
		#setting the is_new user in session
		strategy.session_set('is_new', new_user)

		#checking the pipeline was called once before to add_facility
		has_facility = strategy.session_get('facility', None)

		#Redirecting the Fellow and Admin to Register Facility Page
		if new_user and not has_facility and not uid in super_admin_list:
			return redirect('register')
	return

#partial pipeline for creatng NgUser instance for the user
@partial
def save_profile(strategy, backend, user, request, *args, **kwargs):
	facility = strategy.session_get('facility', None)

	#Saving Profile if the signin is from google-oauth2
	if user and backend.name == 'google-oauth2':
		new_user = kwargs['is_new']
		uid = kwargs['uid']
		super_admin_list=['a@navgurukul.org', 'r@navgurukul.org','amar17@navgurukul.org',]

		#Saving instance to database for Super Admin
		if new_user and uid in super_admin_list:
			nguser = NgUser(user = user, user_type='SUPER_ADMIN')
			nguser.save()
			return {'nguser':nguser}

		#saving instance to database for fellow's
		elif new_user and facility:
			nguser = NgUser(user = user)
			nguser.facility = Facility.objects.get(id= facility)
			nguser.save()
			return {'nguser':nguser}

