from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import NgUser,Facility
from .forms import MoneyTransferForm, BillPaymentForm


def is_fellow(user):
    return user.nguser.user_type == "FELLOW"

@login_required
def home(request):
    # if request.user.nguser.user_type=="ADMIN":
    #     #getting the request from database
    #
    #     return render(request,'admin.html')
    return render(request, 'fellow.html')

def access_denied(request):
    return render(request,'access_denied.html', )

# @user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def moneytransferrequest(request):
    if request.method =='POST':
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.is_money_request=True
            form.facility= form.cleaned_data.get('facility')
            form.save()
            redirect('home')
    else:
        form = MoneyTransferForm()
        print form
    return render(request,'moneytransfer.html',{'form':form})

# @user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def utilitybillrequest(request):
    if request.method =='POST':
        form = BillPaymentForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.is_utility_request=True
            form.save()
            redirect('home')
    else:
        form = BillPaymentForm()
        print form
    return render(request,'billpayment.html',{'form':form})
