from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# def imageuploadlink(instance , filename):
#     return 'billpayment/{0}/{1}'.format(instance.type_of_bill, filename)#WTF
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


class BillPaymentRequest(models.Model):
    BILL = ((1,'Internet'),(2,'Electricity'),(3,'WaterBill'),(4, 'Houserent'))
    type_of_bill = models.CharField(max_length=50, choices=BILL)
    bill_image = models.ImageField(upload_to='billpayment/%Y/%m/%d')
    request_details = models.OneToOneField(RequestDetail,related_name='request_detail')
#models for add expences
class AddExpense(models.Model):
    CATEGORY =((1,'Travel Expense'),(2,'Groceries'))
    is_facility_level = models.BooleanField()
    facility = models.ForeignKey(Facility)
    description = models.TextField()
    amount = models.CharField(max_length=5)
    created_date = models.DateField(auto_now_add=True)
<<<<<<< HEAD
    expense_by = models.ForeignKey(NgUser, related_name='expenses')
=======
    expense_by = models.ForeignKey(NgUser,related_name="expenses")
>>>>>>> a8ce0af4265764a97158d42aa50a17f7984c8402
    category = models.CharField(max_length=30,choices = CATEGORY)
    expense_photo = models.ImageField(upload_to='expenses/%Y/%m/%d')

class RecordPayment(models.Model):
    amount = models.CharField(max_length=5)
    paid_to = models.ForeignKey(NgUser,limit_choices_to={'is_admin':False},null=True,related_name='payment_recieved')
    facility = models.ForeignKey(Facility)
<<<<<<< HEAD
    paid_by = models.ForeignKey(NgUser,limit_choices_to={'is_admin':True},related_name='payments_forward')
=======
    paid_by = models.ForeignKey(NgUser,limit_choices_to={'is_admin':True},related_name='payment_sent')
>>>>>>> a8ce0af4265764a97158d42aa50a17f7984c8402
    created_date = models.DateField(auto_now_add=True)
    bank_screenshot = models.ImageField(upload_to='bank_screenshot/%Y/%m/%d')
    transfer_request = models.ForeignKey(MoneyTransferRequest,null=True)
    bill_request = models.ForeignKey(UtilityBillRequest, null=True)
