from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import NgUser,Facility,CashEntry,MoneyRequest
from .forms import *
from django.shortcuts import get_list_or_404, get_object_or_404
import pdb

def is_fellow(user):
    return user.nguser.user_type == "FELLOW"
def is_admin(user):
    return user.nguser.user_type == "ADMIN"


@login_required
def home(request):
    if not is_fellow(request.user):
        return render(request, 'admin.html')
    return render(request, 'fellow.html')


@user_passes_test(is_admin, login_url='/access_denied/')
@login_required
def add_facility(request):

    print('adding facility')


def access_denied(request):
    return render(request,'access_denied.html')


@user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def moneytransferrequest(request):
    if request.method =='POST':
        print "yes"
        form = MoneyTransferForm(request.POST, request=request)
        if form.is_valid():
            print form
            form.save()
            redirect('home')
    else:
        form = MoneyTransferForm(request=request)
    return render(request,'moneytransfer.html',{'form':form})

@user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def utilitybillrequest(request):
    if request.method =='POST':
        form = UtilityBillRequestForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.is_utility_request=True
            form.save()
            return redirect('home')
    else:
        form = UtilityBillRequestForm()
        print form
    return render(request,'billpayment.html',{'form':form})

def addexpense(request):
    if request.method =='POST':
        form = AddExpenseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            # pdb.set_trace()
            if form.cleaned_data.get('expense_type').encode('utf8') == 'PERSONAL':
                form.is_personal_expense = True
            else:
                form.is_facility_expense = True
            form.facility = form.cleaned_data.get('facility')
            form.save()
            return redirect('home')
    else:
        form = AddExpenseForm()
    return render(request, 'addexpense.html',{'form':form})

@login_required
def facilityreport(request):
    data = CashEntry.objects.all()
    template = 'report.html'
    return render(request, template, {'entries' : data})

@login_required
def fellowreport(request):
    pass
