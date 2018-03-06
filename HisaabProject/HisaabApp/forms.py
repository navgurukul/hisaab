
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import *
from django import forms


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'student_expenses_limit')


class MoneyTransferForm(forms.ModelForm):

    # facility_id = request.user.nguser.facility.id

    upi_id = forms.CharField(max_length=40,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'UPI id of the Fellow'}),required=False)

    facility = forms.ModelChoiceField(queryset= Facility.objects.all() ,widget=forms.Select(attrs={'class': 'form-control'}))
    
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder': 'How much money do you need?'}))
    
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'Why is the money needed?'}))
    
    nguser_with_upi = forms.ModelChoiceField(queryset = NgUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control','placeholder':'In which account do you need the money?'}))
    
    nguser_without_upi = forms.ModelChoiceField(queryset = NgUser.objects.all(),widget=forms.Select(attrs={'class': 'form-control', 'placeholder': "Account that doesn't have UPI id"}),required=False)
    
    class Meta:

        model = MoneyRequest
        fields = ('amount', 'description','facility','upi_id','nguser_with_upi', 'nguser_without_upi')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        facility__id = NgUser.objects.get(user = self.request.user).facility.id
        super(MoneyTransferForm, self).__init__(*args, **kwargs)
        self.fields['facility'].queryset = Facility.objects.all()
        self.fields['facility'].initial = {'facility': facility__id }
        self.fields['nguser_with_upi'].queryset = NgUser.objects.all().filter(facility__id= facility__id ,upi_id__isnull = False)
        self.fields['nguser_without_upi'].queryset = NgUser.objects.all().filter(facility__id= facility__id,upi_id__isnull = True)

    def save(self, commit=True, *args, **kwargs):
        instance = super(MoneyTransferForm, self).save(commit=False)
        upi_id = self.cleaned_data.get('upi_id')
        nguser_without_upi = NgUser.objects.get(id = self.cleaned_data.get('nguser_without_upi').id)
        nguser_with_upi = NgUser.objects.get(id = self.cleaned_data.get('nguser_with_upi').id)
        if nguser and upi_id:
            nguser.upi_id = upi_id
            nguser.save()
            instance.nguser = nguser_without_upi
        else:
            instance.nguser = nguser_with_upi
        instance.is_money_request = True
        if commit:
            instance.save()

        return instance






# class AddExpenseForm(forms.ModelForm):
#     EXPENSETYPE = (("FELLOW",'Navgurukul'),('PERSONAL','Personal'))
#     CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
#     facility = forms.ModelChoiceField(queryset = Facility.objects.all())
#     fellow = forms.ModelChoiceField(queryset = NgUser.objects.all())
#     expense_type = forms.ChoiceField(choices = EXPENSETYPE)
#     category = forms.ChoiceField(choices =CATEGORY)
#     class Meta:
#         model = CashEntry
#         fields = ('fellow','expense_type','facility', 'expense_amount', 'created_date', 'category','bill_image','description')


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