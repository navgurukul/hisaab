from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import CashEntry,Facility,MoneyRequest
from django import forms


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ('name', 'student_expenses_limit')


class MoneyTransferForm(forms.ModelForm):
    facility = forms.ChoiceField(choices=[(facility.pk, facility) for facility in Facility.objects.all()])

    class Meta:
        model = MoneyRequest
        fields = ('amount', 'description', 'account_number', 'ifsc_code','account_holder_name','facility')


class BillPaymentForm(forms.ModelForm):
    BILL = ((1,'Internet'),(2,'Electricity'),(3,'WaterBill'),(4, 'Houserent'))
    facility = forms.ChoiceField(choices=[(facility.pk, facility) for facility in Facility.objects.all()])
    type_of_bill = forms.ChoiceField(choices=BILL)
    class Meta:
        model = MoneyRequest
        fields = ('amount', 'type_of_bill','description', 'bill_image')


class AddExpenseForm(forms.ModelForm):
    EXPENSETYPE = ((1,'Navgurukul'),(2,'Personal'))
    CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
    facility = forms.ChoiceField(choices=[(facility.name, facility) for facility in Facility.objects.all()])
    fellow = forms.ChoiceField(choices=[(user.pk, user) for user in User.objects.all()])
    expense_type = forms.ChoiceField(choices=EXPENSETYPE)
    category = forms.ChoiceField(choices=CATEGORY)
    class Meta:
        model = CashEntry
        fields = ('expense_type', 'expense_amount', 'created_date', 'category','bill_image','description')
