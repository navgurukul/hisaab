
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms

from django.urls import reverse
from django.utils import timezone

from django.utils import timezone
from social_core.pipeline.utils import partial_load
from social_django.utils import load_strategy


def is_fellow(user):
    return user.nguser.user_type == "FELLOW"
def is_admin(user):
    return user.nguser.user_type == "ADMIN"

def access_denied(request):
    return render(request,'access_denied.html')


def register(request):
    if request.session.get('is_new', None):
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                request.session['facility'] =  form.cleaned_data.get('facility',None).id
                print "redirecting"
                return redirect(reverse('social:complete', args=("google-oauth2",)))
        else:
            form = RegisterForm()
        return render(request, 'register_form.html',{'form':form})
    else:
        return redirect('access_denied')

@login_required
def home(request):
    if is_admin(request.user):
        money_requests = MoneyRequest.objects.all().filter(is_queued=True)[:2]

        facilities = Facility.objects.all()
        return render(request, 'admin.html', {'facilities': facilities,'money_requests':money_requests  })

    return render(request, 'fellow.html')


@user_passes_test(is_admin, login_url='/access_denied/')
@login_required
def add_facility(request):
    print('adding facility')


@user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def moneytransferrequest(request):
    if request.method =='POST':
        form = MoneyTransferForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = MoneyTransferForm(request=request)
    return render(request,'moneytransfer.html',{'form':form})


@user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def utilitybillrequest(request):
    if request.method =='POST':
        form = UtilityBillRequestForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_utility_request=True
            instance.facility = request.user.nguser.facility
            instance.money_requested_by = request.user.nguser
            instance.save()
            return redirect('home')
    else:
        form = UtilityBillRequestForm()
        print form
    return render(request,'billpayments.html',{'form':form})


@user_passes_test(is_admin, login_url='/access_denied/')
@login_required
def recordpayment(request):
    if request.method ==  'POST':
        form = RecordPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.fellow = request.user.nguser
            instance.is_payment_to_ng = True
            instance.save()
            return redirect('home')
    else:
        form = RecordPaymentForm()
    return render(request, 'recordpayment.html', {'form': form})

@login_required
def addexpense(request):
    if request.method =='POST':
        form = AddExpenseForm(request.POST,request.FILES, request=request)
        if form.is_valid():
            instance = form.save(commit=False)
            if form.cleaned_data.get('expense_type').encode('utf8') == 'PERSONAL':
                instance.is_personal_expense = True
            else:
                instance.is_facility_expense = True
            
            instance.save()
        return redirect('home')
    else:
        form = AddExpenseForm(request=request)
    return render(request, 'addexpenses.html',{'form':form})

@login_required
def facilityreport(request, pk):
    facility = get_object_or_404(Facility,pk=pk)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        categories = request.POST.getlist('categories')
        if 'payment' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date,end_date),\
            is_payment_to_ng=True,facility__id=pk)
            payment = True
        elif 'expense' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date, end_date),\
            category__in=categories,is_facility_expense=True,facility__id=pk)
            payment = False
        return render(request, 'facilityreport.html', {'entries': data, 'facility':facility, 'payment': payment })
    payment = False
    data = CashEntry.objects.all().filter(facility__id=pk)
    return render(request, 'facilityreport.html',{'facility':facility,'entries': data,'payment':payment})

@login_required
def fellowreport(request, pk):
    fellow = get_object_or_404(NgUser,pk=pk)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        categories = request.POST.getlist('categories')
        if 'payment' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date,end_date),\
            is_pay_forward=True,fellow__id=pk)
            payment = True
        elif 'expense' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date, end_date),\
            category__in=categories,is_personal_expense=True,fellow__id=pk)
            payment = False
        return render(request, 'facilityreport.html', {'entries': data, 'fellow':fellow, 'payment': payment })
    payment = False
    return render(request, 'facilityreport.html',{'fellow':fellow,'payment':payment})


@user_passes_test(is_admin, login_url='/access_denied/')
@login_required
def viewpendingrequests(request):
    transfer_requests = MoneyRequest.objects.all().filter(is_queued=True)
    paginator = Paginator(transfer_requests, 3)
    page = request.GET.get('page', 1)
    try:
        money_requests = paginator.page(page)
    except PageNotAnInteger:
        money_requests = paginator.page(1)
    except EmptyPage:
        money_requests = paginator.page(paginator.num_pages)
    
    return render(request,'viewpendingrequests.html',{'money_requests':money_requests})


@user_passes_test(is_admin, login_url='/access_denied/')
@login_required
def viewpendingrequest(request, pk):    
    money_request = get_object_or_404(MoneyRequest, pk=pk)
    if request.method == 'POST':
        if 'accept' in request.POST:
            money_request.is_queued = False
            money_request.is_approve = True
            money_request.approve_or_rejected_by = request.user.nguser
            money_request.save()
        elif 'reject' in request.POST:
            money_request.is_queued = False
            money_request.approve_or_rejected_by = request.user.nguser
            reason_for_reject = request.POST.get('reason_for_reject', None)
            if not reason_for_reject:
                raise forms.ValidationError('Please Provide a reason')
            money_request.reason_for_reject = reason_for_reject
            money_request.save()
        return redirect('home')

    return render(request,'viewpendingrequest.html',{'money_request':money_request})
