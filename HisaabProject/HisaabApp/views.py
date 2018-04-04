
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms

from django.urls import reverse
from django.utils import timezone
import json
from django.utils import timezone

from django.db.models import Q



#For checking the usertype
# For checking is the user is fellow(student in the navgurukul)
def is_fellow(user):
    return user.nguser.user_type == "FELLOW"

#For checking the is the user is admin(volenture in the navgurukul)    
def is_admin(user):
    return user.nguser.user_type == "ADMIN" or user.nguser.user_type == "SUPER_ADMIN"

#For checking is the user is Super_admin(Abhisek Gupta or Rishabh verma(CO-FOUNDERS OF NAVGURUKUL))    
def is_super_admin(user):
    return user.nguser.user_type == "SUPER_ADMIN"

# If the user tries to do the things for which he doesn't have the permission then this page will shown to the user
def access_denied(request):
    return render(request,'access_denied.html')


# Views for registering the facility of the user
def register(request):

    # Getting the is_new from google authentication session   
    if request.session.get('is_new', None):

        #Handling the post request data  
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            # Validating the form and storing the facility in session for further use
            if form.is_valid():
                request.session['facility'] =  form.cleaned_data.get('facility',None).id
                print "redirecting"
                return redirect(reverse('social:complete', args=("google-oauth2",)))
        
        #new empty form instance for register is created
        else:
            form = RegisterForm()
        return render(request, 'register_form.html',{'form':form})

    # Handling the url visit after facility has been added
    else:
        return redirect('access_denied')


#Rendering the home page to user.
@login_required
def home(request):

    #Checkin is the user is_admin
    if is_admin(request.user):

        #filtring the MoneyRequest(atleast three) and facility objects
        money_requests = MoneyRequest.objects.all().filter(is_queued=True)[:2]
        facilities = Facility.objects.all()

        return render(request, 'admin.html', {'facilities': facilities,'money_requests':money_requests  })

    #handling url visit after the filter    
    money_requests = MoneyRequest.objects.all().filter(is_queued=False, money_requested_by=request.user.nguser )
    return render(request, 'fellow.html',{'money_requests':money_requests})



@login_required
@user_passes_test(is_fellow, login_url='/access_denied/')
#For making money request by the students
def moneytransferrequest(request):

    # Handling the post request data and a form is made
    if request.method =='POST':
        form = MoneyTransferForm(request.POST, request=request)

        #validating and storing the form data
        if form.is_valid():
            form.save()
            return redirect('home')

    # new empty form instance for moneytransferrequest is created        
    else:
        form = MoneyTransferForm(request=request)
    return render(request,'moneytransfer.html',{'form':form})



@login_required
@user_passes_test(is_fellow, login_url='/access_denied/')
#For making the Bill request by the students
def utilitybillrequest(request):

    #Handling the post request data and a form is made
    if request.method =='POST':
        form = UtilityBillRequestForm(request.POST,request.FILES)

        # Vlidating the form 
        if form.is_valid():

            # creating model instances and saving it to the database
            instance = form.save(commit=False)
            instance.is_utility_request=True
            instance.facility = request.user.nguser.facility
            instance.money_requested_by = request.user.nguser
            instance.save()
            return redirect('home')

    #new empty form instance for utilitybillrequest is created       
    else:
        form = UtilityBillRequestForm()
        print form
    return render(request,'billpayments.html',{'form':form})



@user_passes_test(is_admin, login_url='/access_denied/')
@login_required

#Creating Records of the payment made to a Facility
def recordpayment(request):

    # Handling the post request data and a form is made
    if request.method ==  'POST':
        form = RecordPaymentForm(request.POST, request.FILES)

        # validating the form
        if form.is_valid():

            # making instances and getting objects from models and saving it
            instance = form.save(commit = False)
            ###################################################################
            # Should we save the admin who accepted as or the payment
            ###################################################################

            instance.fellow = request.user.nguser
            instance.is_payment_to_ng = True
            facility = instance.facility
            facility.cash_in_hand += int(form.cleaned_data.get('payment_amount'))
            instance.cash_in_hand_currently = facility.cash_in_hand
            facility.save()
            instance.save()
            return redirect('home')

    # new empty form instance for recordpayment is created          
    else:
        form = RecordPaymentForm()
    return render(request, 'recordpayment.html', {'form': form})

#For adding all the expenses made by a person.
@login_required
def addexpense(request):

    # Handling the post request data and a form is made
    if request.method =='POST':
        form = AddExpenseForm(request.POST,request.FILES, request=request)
        print"him"

        #validating the form 
        if form.is_valid():
            print"hi"
            #saving the instance
            instance = form.save(commit=False)

            # handling the data when expence type is personal
            if form.cleaned_data.get('expense_type') == 'PERSONAL':
                instance.is_personal_expense = True
                print "yeh"
            # handling the data when the expence type is not personal and save it    
            else:
                instance.is_facility_expense = True
            facility= form.cleaned_data.get('facility')
            facility.cash_in_hand -= int(form.cleaned_data.get('expense_amount'))
            instance.cash_in_hand_currently = facility.cash_in_hand
            facility.save()
            instance.save()
            return redirect('home')

    #Handling ajax request for sending the user of the same facility        
    elif request.method == 'GET' and request.is_ajax():
        facility = request.GET.get('facility', None)
        data = {'users': list(NgUser.objects.all().filter(facility__id= facility).values('user__username', 'id',))}
        return JsonResponse(data)

    # new empty form instance for adexpence is created    
    else:
        form = AddExpenseForm(request=request)
    return render(request, 'addexpenses.html',{'form':form})

#Getting the Detail Report about the expense and payment made to the Facility.
@login_required
def facilityreport(request, pk):

    facility = get_object_or_404(Facility,pk=pk)
    # Handling the post request data  
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        categories = request.POST.getlist('categories')
        print start_date,end_date,categories

        # payment fitering part handling for facility 
        if 'payment' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date,end_date),is_payment_to_ng=True,facility__id=pk)
            payment = True

        # expence filtering part handling for facility   
        elif 'expense' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date, end_date),category__in=categories,facility__id=pk).filter(Q(is_personal_expense=True)|Q(is_facility_expense=True))
            payment = False
        return render(request, 'facilityreport.html', {'entries': data, 'facility':facility, 'payment': payment })
    payment = False
    data = CashEntry.objects.all().filter(facility__id=pk).filter(Q(is_personal_expense=True)|Q(is_facility_expense=True))
    return render(request, 'facilityreport.html',{'facility':facility,'entries': data,'payment':payment})

#Getting the Detail report the student expense and payments.
@login_required
def fellowreport(request, pk):
    fellow = get_object_or_404(NgUser,pk=pk)
    #Handling the post request data
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        categories = request.POST.getlist('categories')
        #payment fitering part handling for fellow
        if 'payment' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date,end_date),\
            is_pay_forward=True,fellow__id=pk)
            payment = True
        #expence fitering part handling for fellow    
        elif 'expense' in request.POST:
            data = CashEntry.objects.all().filter(created_date__range=(start_date, end_date),category__in=categories,is_personal_expense=True,fellow__id=pk)
            payment = False
        return render(request, 'fellowreport.html', {'entries': data, 'fellow':fellow, 'payment': payment })
    payment = False
    data = CashEntry.objects.all().filter(fellow__id=pk,is_personal_expense=True)
    return render(request, 'fellowreport.html',{'fellow':fellow, 'payment':payment, 'entries': data,})

#Rending all the request that are pending
@login_required
@user_passes_test(is_admin, login_url='/access_denied/')
def viewpendingrequests(request):
    # showing all pending requests for admin and added paginator to it
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



#Detail Page for each requests for money or bill payment for admin.
@login_required
@user_passes_test(is_admin, login_url='/access_denied/')
def viewpendingrequest(request, pk):
    money_request = get_object_or_404(MoneyRequest, pk=pk)
    # handling if money is queued 
    if not money_request.is_queued:
        return redirect('home')
    # Handling the post request data
    if request.method == 'POST':
        # request handling if the the request is accepted 
        if 'accept' in request.POST:
            form = PaymentRecordForm(request.POST, request.FILES)
            if form.is_valid():
                # Updating the MoneyRequest data
                money_request.is_queued = False
                money_request.is_approve = True
                money_request.approve_or_rejected_by = request.user.nguser
                money_request.save()

                # Creating the cash entry data
                entry['facility'] = money_request.facility
                entry['bank_screenshot'] = forms.cleaned_data.get('bank_screenshot')
                entry['payment_amount'] = money_request.amount
                entry['description'] = money_request.description
                entry['fellow'] =  money_request.money_requested_by

                # facility cash_in_hand update
                facility = entry['facility']
                facility.cash_in_hand += int(entry['payment_amount'] )
                entry['cash_in_hand_currently'] = facility.cash_in_hand
                facility.save()

                ###################################################################
                # what to do about the bil_image in the MoneyRequest?
                ###################################################################
               
                # saving to database
                CashEntry.objects.create(facility = entry['facility'], bank_screenshot = entry['bank_screenshot'],payment_amount = entry['payment_amount'],description = entry['description'], fellow = entry['fellow'], is_personal_expense=True,cash_in_hand_currently = entry['cash_in_hand_currently'])
                return redirect('home')


        # request handling if the the request is rejected   
        elif 'reject' in request.POST:
            money_request.is_queued = False
            money_request.approve_or_rejected_by = request.user.nguser
            reason_for_reject = request.POST.get('reason_for_reject', None)

            # reson handling if the request is rejected
            if not reason_for_reject:
                raise forms.ValidationError('Please Provide a reason')
            money_request.reason_for_reject = reason_for_reject
            money_request.save()
            return redirect('home')

    # url handling after the request handling
    return render(request,'viewpendingrequest.html',{'money_request':money_request})



#Detail Page for each requests for money or bill payment for fellow.
@login_required
@user_passes_test(is_fellow, login_url='/access_denied/')
def detailrequest(request, pk):
    money_request = get_object_or_404(MoneyRequest, pk=pk)
    return render(request,'detailrequest.html',{'money_request':money_request})


#Views for serching any students report by admin
@login_required
@user_passes_test(is_admin, login_url='/access_denied/')
def searchfellow(request):
    #handling for serch student name by ajax
    if request.is_ajax() and request.method=='GET':
        query = request.GET.get('query')
        print"commit"
        data = {'users': list(NgUser.objects.all().filter(user_type="FELLOW", user__username__icontains= query).values('user__username', 'id', 'facility__name'))}

        return JsonResponse(data)
    #render the search page    
    return render(request, 'searchuser.html')

# views for giving a permission to super admin to create a admin
@login_required
@user_passes_test(is_super_admin, login_url='/access_denied/')
def make_admin(request):
    if request.method == 'GET' and request.is_ajax():

        #sending the data by getting the facility value
        facility = request.GET.get('facility')
        print facility
        data = {'users': list(NgUser.objects.all().filter(user_type="FELLOW",facility__id= facility).values('user__username', 'id',))}
        return JsonResponse(data)
    elif request.method == 'POST':
        #Add it to be an admin
        fellow_id = request.POST.get('fellow',None)
        fellow = get_object_or_404(NgUser, pk=fellow_id)
        fellow.user_type='ADMIN'
        fellow.save()
        return redirect('home')
    #render the Page
    facilities = Facility.objects.all()
    return render(request, 'makeadmin.html',{'facilities':facilities})



@user_passes_test(is_super_admin, login_url='/access_denied/')
#views for adding a new facility by super admin
def add_facility(request):
    #Handling the post request data and a form is made
    if request.method =='POST':
        form=AddFacilityForm(request.POST)
        #validating and storing the form for further use
        if form.is_valid():
            form.save()
            return redirect('home')
    #new empty form instance for add_facility is created        
    else:
        form = AddFacilityForm()
    return render(request,'addfacility.html',{'form':form})



@user_passes_test(is_super_admin, login_url='/access_denied/')
#views for adding a new add category by super admin
def add_category(request):
    #Handling the post request data and a form is made
    if request.method =='POST':
        form=AddCategoryForm(request.POST)
        #validating and storing the form for further use
        if form.is_valid():
            form.save()
            return redirect('home')
    #new empty form instance for add_cateogry form is created        
    else:
        form = AddCategoryForm()
    return render(request,'addcategory.html',{'form':form})



@user_passes_test(is_super_admin, login_url='/access_denied/')
#views for Updating facility detail by super admin
def update_facility(request):
    #Handling the post request data and a form is made
    if request.method =='POST':
        form=UpdateFacilityForm(request.POST)
        #validating and storing the form for further use
        if form.is_valid():
            facility = form.cleaned_data.get('facility')
            facility.student_expenses_limit = form.cleaned_data.get('student_expenses_limit')
            facility.save()
            return redirect('home')
    #new empty form instance for Updatingfacility is created        
    else:
        form = UpdateFacilityForm()
    return render(request,'updatefacility.html',{'form':form})

