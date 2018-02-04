from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import NgUser,Facility
from .forms import UserForm,FacilityForm

@login_required
def home(request):
    return render(request, 'home.html')
