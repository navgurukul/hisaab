from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.contrib.auth.models import User
=======
>>>>>>> 77f3af94ef4aea6fa1e8fe9607fb2ccfb8b953a6
from .models import NgUser,Facility
from .forms import UserForm,FacilityForm

@login_required
def home(request):
    return render(request, 'home.html')
