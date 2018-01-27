from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

def fellowscreenshot(instance , filename):
    return 'billpayment/{0}/{1}'.format(instance.user.id, filename)

class Facility(models.Model):
    name = models.CharField(max_length=50)
    student_expenses_limit = models.CharField(max_length=6)

class NgUser(models.Model):
    user = models.OneToOneField(User)
    created_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    facility= models.ForeignKey(Facility,null=True)

class RequestDetail(models.Model):
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField()
    approve_or_rejected_by = models.ForeignKey(NgUser, limit_choices_to={'is_admin':True})
    reject_text = models.TextField(null=True)

class MoneyTransferRequest(models.Model):
    account_number = models.CharField(max_length=20)
    confirm_account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=20)
    transfer_to = models.ForeignKey(NgUser,limit_choices_to={'is_admin':False})
    request_details = models.OneToOneField(RequestDetail,related_name='request_details')


class UtilityBillRequest(models.Model):
    BILL = ((1,'Internet'),(2,'Electricity'),(3,'WaterBill'),(4, 'Houserent'))
    type_of_bill = models.CharField(max_length=50, choices=BILL)
    bill_image = models.ImageField(upload_to='billpayment/%Y/%m/%d')
    request_details = models.OneToOneField(RequestDetail,related_name='request_detail')
#
# class AddExpense(models.Model):
#     CATEGORY =((1,'Travel Expense'),(2,'Groceries'))
#     is_facility_level = models.BooleanField()
#     facility = models.ForeignKey(Facility)
#     description = models.TextField()
#     amount = models.CharField(max_length=5)
#     created_date = models.DateField(auto_now_add=True)
#     expense_by = models.ForeignKey(NgUser,related_name="expenses")
#     category = models.CharField(max_length=30,choices = CATEGORY)
#     expense_photo = models.ImageField(upload_to='expenses/%Y/%m/%d')
#
# class RecordPayment(models.Model):
#     amount = models.CharField(max_length=5)
#     paid_to = models.ForeignKey(NgUser,limit_choices_to={'is_admin':False},null=True,related_name='payment_recieved')
#     facility = models.ForeignKey(Facility)
#     paid_by = models.ForeignKey(NgUser,limit_choices_to={'is_admin':True},related_name='payment_sent')
#     created_date = models.DateField(auto_now_add=True)
#     bank_screenshot = models.ImageField(upload_to='bank_screenshot/%Y/%m/%d')
#     transfer_request = models.ForeignKey(MoneyTransferRequest,null=True)
#     bill_request = models.ForeignKey(UtilityBillRequest, null=True)


class CashEntry(models.Model):
    CATEGORY =((1,'Travel Expense'),(2,'Groceries'))
    ENTRY_TYPE =((1,'Payment'),(2,'Expenses'))
    created_date = models.DateField(auto_now_add=True)
    fellow = models.ForeignKey(NgUser, related_name='cash_entry', related_query_name = 'cash_entry')
    entry_type= models.CharField(max_length=25, choices= ENTRY_TYPE)
    transaction_amount = models.IntegerField()
    category = models.CharField(max_length=25, choices= CATEGORY, null = True)
    is_expense_personal = models.BooleanField(default=False)
    is_facility_expense = models.BooleanField(default=False)
    is_pay_forward = models.BooleanField(default=False)
    is_payment_to_ng = models.BooleanField(default=False)
    bank_screenshot = models.ImageField(upload_to="bank_screenshot/%Y/%m/%d")
    fellow_payment_screenshot = models.ImageField(upload_to=fellowscreenshot)
    bill_image = models.ImageField(upload_to="billimage/%Y/%m/%d")
    description = models.TextField
