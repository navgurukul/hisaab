
 django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import CashEntry,NgUser,Facility,MoneyRequest
from django import forms


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'student_expenses_limit')


class MoneyTransferForm(forms.ModelForm):
    facility = forms.ModelChoiceField(queryset=Facility.objects.all())

    class Meta:
        model = MoneyRequest
        fields = ('amount', 'description', 'account_number', 'ifsc_code','account_holder_name','facility')


class BillPaymentForm(forms.ModelForm):
    BILL = ((1,'Internet'),(2,'Electricity'),(3,'WaterBill'),(4, 'Houserent'))
    facility = forms.ModelChoiceField(queryset=Facility.objects.all())
    type_of_bill = forms.ChoiceField(choices=BILL)
    class Meta:
        model = MoneyRequest
        fields = ('amount', 'type_of_bill','description', 'bill_image')


class AddExpenseForm(forms.ModelForm):
    EXPENSETYPE = (("FELLOW",'Navgurukul'),('PERSONAL','Personal'))
    CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
    facility = forms.ModelChoiceField(queryset = Facility.objects.all())
    fellow = forms.ModelChoiceField(queryset = NgUser.objects.all())
    expense_type = forms.ChoiceField(choices = EXPENSETYPE)
    category = forms.ChoiceField(choices =CATEGORY)
    class Meta:
        model = CashEntry
        fields = ('fellow','expense_type','facility', 'expense_amount', 'created_date', 'category','bill_image','description')


class FacilityReportForm(forms.ModelForm):
    class Meta:
        model = CashEntry
        fields = ('fellow','expense_amount','category','created_date','description')



class FellowReportForm(forms.Form):
    CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    expense_type =forms.MultipleChoiceField(widget= forms.CheckboxSelectMultiple(),choices=category)

    