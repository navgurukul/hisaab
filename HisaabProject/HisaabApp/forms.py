from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import *
from django import forms


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'student_expenses_limit')



class RegisterForm(forms.Form):
    ''' Form to get the Facility of the students and UPI id on Signup'''
    facility = forms.ModelChoiceField(queryset = Facility.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))




class MoneyTransferForm(forms.ModelForm):
    upi_id = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder': 'UPI id of the Fellow'}),required=False)
    facility = forms.ModelChoiceField(queryset= Facility.objects.all() ,widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm','placeholder': 'How much money do you need?'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-sm','placeholder': 'Why is the money needed?'}))
    nguser_with_upi = forms.ModelChoiceField(queryset = NgUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm','placeholder':'In which account do you need the money?'}), required=False)
    nguser_without_upi = forms.ModelChoiceField(queryset = NgUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm', 'placeholder': "Account that doesn't have UPI id"}),required=False)

    class Meta:

        model = MoneyRequest
        fields = ('amount', 'description','facility','upi_id','nguser_with_upi', 'nguser_without_upi')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        facility__id = NgUser.objects.get(user = self.request.user).facility.id
        super(MoneyTransferForm, self).__init__(*args, **kwargs)
        self.fields['facility'].queryset = Facility.objects.all()
        self.fields['nguser_with_upi'].queryset = NgUser.objects.all().filter(facility__id= facility__id ,upi_id__isnull = False)
        self.fields['nguser_without_upi'].queryset = NgUser.objects.all().filter(facility__id= facility__id,upi_id__isnull = True)

    def save(self, commit=True, *args, **kwargs):
        instance = super(MoneyTransferForm, self).save(commit=False)
        upi_id = self.cleaned_data.get('upi_id')
        nguser_without_upi = self.cleaned_data.get('nguser_without_upi',None)
        nguser_with_upi = self.cleaned_data.get('nguser_with_upi',None)
        if nguser_without_upi and upi_id:
            nguser.upi_id = upi_id
            nguser.save()
            instance.nguser = nguser_without_upi
        else:
            instance.nguser = nguser_with_upi

        instance.is_money_request = True
        if commit:
            instance.save()

        return instance

    def clean(self):
        cleaned_data = super(MoneyTransferForm, self).clean()
        nguser_with_upi = cleaned_data.get('nguser_with_upi')
        nguser_without_upi = cleaned_data.get('nguser_without_upi')
        upi_id = cleaned_data.get('upi_id')
        if (nguser_without_upi or upi_id) and nguser_with_upi:
            raise ValidationError('Select either one of the options in Account Detail!')
        elif nguser_without_upi and not upi_id:
            raise ValidationError('UPI id is required!')


class RecordPaymentForm(forms.ModelForm):
    facility = forms.ModelChoiceField(queryset= Facility.objects.all() ,widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-sm','placeholder': 'Why is the money needed?'}))
    payment_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm','placeholder': 'How much money do you need?'}))
    # bank_screenshot = forms.ImageField(widget=forms.ClearableFileInput(attrs = {'class':'btn btn-default','placeholder': 'Upload the bank transaction screenshot!'}))
    class Meta:
        model = CashEntry
        fields = ['facility', 'bank_screenshot', 'payment_amount', 'description']



class UtilityBillRequestForm(forms.ModelForm):
    BILL = (('INTERNET','Internet'),('ELECTRICITY','Electricity'),('WATER','WaterBill'),('HOUSERENT', 'Houserent'))
    type_of_bill = forms.ChoiceField(choices = BILL)
    class Meta:
        model = MoneyRequest
        fields = ('amount','type_of_bill','description','bill_image')

class AddExpenseForm(forms.ModelForm):
    EXPENSETYPE = (("FELLOW",'Navgurukul'),('PERSONAL','Personal'))
    CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
    facility = forms.ModelChoiceField(queryset = Facility.objects.all(), widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    fellow = forms.ModelChoiceField(queryset = NgUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    expense_type = forms.ChoiceField(choices = EXPENSETYPE, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    category = forms.ChoiceField(choices =CATEGORY, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    expense_amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control form-control-sm','placeholder': 'How much money do you need?'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control form-control-sm','placeholder': 'Why is the money needed?'}))
    class Meta:
        model = CashEntry
        fields = ('fellow','expense_type','facility', 'expense_amount', 'created_date', 'category','bill_image','description')

# class FacilityReportForm(forms.ModelForm):
#     class Meta:
#         model = CashEntry
#         fields = ('fellow','expense_amount','category','created_date','description')



# class FellowReportForm(forms.Form):
#     CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
#     start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
#     end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
#     expense_type =forms.MultipleChoiceField(widget= forms.CheckboxSelectMultiple(),choices=CATEGORY)

#
