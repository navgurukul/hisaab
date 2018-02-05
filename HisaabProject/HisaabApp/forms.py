from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from HisaabApp.models import NgUser,Facility,MoneyRequest
from django import forms

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email','username',)
# # class NgUserForm(forms.ModelForm):
# #     class Meta:
# #         model = NgUser
# #         fields
#
# class FacilityForm(forms.ModelForm):
#     class Meta:
#         model=Facility
#         fields = ('name', 'student_expenses_limit')

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
        fields=('amount','description','bill_image','facility','type_of_bill')
