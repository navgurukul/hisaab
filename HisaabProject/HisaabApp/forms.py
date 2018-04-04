#Importing the files
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import *
from django import forms


#Form to create a new facility by Super Admin
class AddFacilityForm(forms.ModelForm):

    #fields to be displayed and the model to be used
    class Meta:
        model = Facility
        fields = ('name', 'student_expenses_limit')

#form to add new category
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

#to check the image fileis valid or not aftering accepting
class PaymentRecordForm(forms.Form):
    bank_screenshot = forms.ImageField()

#form to Update the detail of the facility
class UpdateFacilityForm(forms.Form):
    facility = forms.ModelChoiceField(queryset= Facility.objects.all())
    student_expenses_limit = forms.IntegerField()



#Form to get the Facility of the user when the user signup for the first time
class RegisterForm(forms.Form):
    facility = forms.ModelChoiceField(queryset = Facility.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))


#Form to Handle the data whenever someone make a request to the user from TransferRequestPage 
class MoneyTransferForm(forms.ModelForm):
    upi_id = forms.CharField(max_length=40,required=False)
    money_requested_by = forms.ModelChoiceField(queryset= NgUser.objects.all())
    amount = forms.IntegerField()
    description = forms.CharField()
    nguser_with_upi = forms.ModelChoiceField(queryset = NgUser.objects.all(), required=False)
    nguser_without_upi = forms.ModelChoiceField(queryset = NgUser.objects.all(),required=False)

    #fields to be displayed and the model to be used
    class Meta:
        model = MoneyRequest
        fields = ('amount', 'description','money_requested_by','upi_id','nguser_with_upi', 'nguser_without_upi')


    #Initializing the instance with default customization in the ModelChoiceFields
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        #Getting the id of the user
        facility__id = NgUser.objects.get(user = self.request.user).facility.id

        #calling the parent class __init__() method
        super(MoneyTransferForm, self).__init__(*args, **kwargs)
        
        #creating the queryset for ModelChoiceFields as per requirement
        self.fields['money_requested_by'].queryset = NgUser.objects.all().filter(facility__id = facility__id, user_type='FELLOW')
        self.fields['nguser_with_upi'].queryset = NgUser.objects.all().filter(facility__id= facility__id ,user_type='FELLOW',upi_id__isnull = False)
        self.fields['nguser_without_upi'].queryset = NgUser.objects.all().filter(facility__id= facility__id,user_type='FELLOW',upi_id__isnull = True)


    #Saving the form to the database whenever save() method is called
    def save(self, commit=True, *args, **kwargs):

        #calling the parent class save() method
        instance = super(MoneyTransferForm, self).save(commit=False)

        #getting the value after validation has been done
        upi_id = self.cleaned_data.get('upi_id')
        nguser_without_upi = self.cleaned_data.get('nguser_without_upi',None)
        nguser_with_upi = self.cleaned_data.get('nguser_with_upi',None)
        
        # Checking if a new user is created with the required fields and
        # saving the UPI id to the user model field
        if nguser_without_upi and upi_id:
            nguser_without_upi.upi_id = upi_id
            nguser_without_upi.save()
            instance.money_received_by = nguser_without_upi

        #else pre-existing user have been selected
        else:
            instance.money_received_by = nguser_with_upi

        #saving the rest of the required fields for the TransferRequestPage
        instance.is_money_request = True
        instance.facility = instance.money_received_by.facility
        
        #Saving the instance to database 
        if commit:
            instance.save()
        return instance


    #Checking for the custom validation of the form 
    def clean(self):

        #calling the parent class clean() method
        cleaned_data = super(MoneyTransferForm, self).clean()
        nguser_with_upi = cleaned_data.get('nguser_with_upi')
        nguser_without_upi = cleaned_data.get('nguser_without_upi')
        upi_id = cleaned_data.get('upi_id')

        #Checking the either one of the field has the data or not
        if (nguser_without_upi or upi_id) and nguser_with_upi:
            raise ValidationError('Select either one of the options in Account Detail!')

        #Checking if the user is created with data in both the fields
        elif nguser_without_upi and not upi_id:
            raise ValidationError('UPI id is required!')


#Form to handle the data from the RecordPaymentPage 
class RecordPaymentForm(forms.ModelForm):
    facility = forms.ModelChoiceField(queryset= Facility.objects.all())
    description = forms.CharField()
    payment_amount = forms.IntegerField()

    #fields to be displayed and the model to be used
    class Meta:
        model = CashEntry
        fields = ['facility', 'bank_screenshot', 'payment_amount', 'description']


#Form to handle the BillPaymentPage
class UtilityBillRequestForm(forms.ModelForm):

    BILL = (('INTERNET','Internet'),('ELECTRICITY','Electricity'),('WATER','WaterBill'),('HOUSERENT', 'Houserent'))
    type_of_bill = forms.ChoiceField(choices = BILL)

    #fields to be displayed and the model to be used
    class Meta:
        model = MoneyRequest
        fields = ('amount','type_of_bill','description','bill_image')


#Form to handle the Add Expense Page 
class AddExpenseForm(forms.ModelForm):

    EXPENSETYPE = (("FACILITY",'Navgurukul'),('PERSONAL','Personal'))

    #categories for the expenses made
    # CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))

    facility = forms.ModelChoiceField(queryset = Facility.objects.all())
    fellow = forms.ModelChoiceField(queryset = NgUser.objects.all().filter(user_type='FELLOW'))
    expense_type = forms.ChoiceField(choices = EXPENSETYPE)
    category = forms.ModelChoiceField(queryset = Category.objects.all())
    expense_amount = forms.IntegerField()
    description = forms.CharField()


    #fields to be displayed and the model to be used
    class Meta:
        model = CashEntry
        fields = ('fellow','expense_type','facility', 'expense_amount', 'created_date', 'category','bill_image','description')

    #Initializing the instance with default customization in the ModelChoiceFields
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)

        #calling the parent class __init__() method
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        
        # including all the user if authenticated user is admin or super_admin
        if self.request.user.nguser.is_admin() or self.request.user.nguser.is_super_admin():
            self.fields['fellow'].queryset = NgUser.objects.all()

        # else selecting all the user of same facility
        else:
            facility__id = NgUser.objects.get(user = self.request.user).facility.id
            self.fields['fellow'].queryset = NgUser.objects.all().filter(facility__id= facility__id).filter(user_type='FELLOW')

