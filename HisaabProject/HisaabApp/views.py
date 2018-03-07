from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.urls import reverse


from social_core.pipeline.utils import partial_load
from social_django.utils import load_strategy



def is_fellow(user):
    return user.nguser.user_type == "FELLOW"

def is_admin(user):
    return user.nguser.user_type == "ADMIN"


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
    if request.method == 'POST':
        print "yahan ayaa ta"
        form = MoneyTransferForm(request.POST, request=request)
        if form.is_valid():
            print "yahn bhi"
            form.save()
            redirect('home')
    else:
        form = MoneyTransferForm(request=request)
    return render(request,'moneytransfer.html',{'form':form})




@user_passes_test(is_fellow, login_url='/access_denied/')
@login_required
def utilitybillrequest(request):
    if request.method =='POST':
        form = BillPaymentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.is_utility_request=True
            form.save()
            redirect('home')
    else:
        form = BillPaymentForm()
        print form
    return render(request,'billpayment.html',{'form':form})

def addexpense(request):
    if request.method =='POST':
        form = AddExpenseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=False)
            # pdb.set_trace()
            print form.cleaned_data.get('expense_type').encode('utf8')
            if form.cleaned_data.get('expense_type').encode('utf8') == 'PERSONAL':
                form.is_personal_expense = True
            else:
                form.is_facility_expense = True
            print form.cleaned_data.get('facility')
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