from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import NgUser,Facility
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username',)
# class NgUserForm(forms.ModelForm):
#     class Meta:
#         model = NgUser
#         fields

class FacilityForm(forms.ModelForm):
    class Meta:
        model=Facility
        fields = ('name', 'student_expenses_limit')
