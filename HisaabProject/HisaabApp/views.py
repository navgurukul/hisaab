from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from .models import NgUser,Facility
from .forms import UserForm,FacilityForm

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        facility_form = Facility(request.POST, instance=request.user.facility)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            facility_form.save()
            return redirect('/')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        facility_form = FacilityForm(instance=request.user.facility)
    return render(request, 'updae_profile.html', {
        'user_form': user_form,
        'facility_form': facility_form
    })
