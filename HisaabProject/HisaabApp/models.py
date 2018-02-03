from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def fellowscreenshot(instance , filename):
    return 'billpayment/{0}/{1}'.format(instance.user.id, filename)

class Facility(models.Model):
    name = models.CharField(max_length=50)
    student_expenses_limit = models.IntegerField()

class NgUser(models.Model):
    user = models.OneToOneField(User,unique=True, null=False)
    created_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_fellow = models.BooleanField(default=False)
    facility= models.ForeignKey(Facility,null=True)
# 
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         NgUser.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.nguser.save()

class RequestDetail(models.Model):
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField()
    is_queued = models.BooleanField(default=True)
    approve_or_rejected_by = models.ForeignKey(NgUser, limit_choices_to={'is_admin':True})
    reject_text = models.TextField(null=True)

class MoneyTransferRequest(models.Model):
    account_number = models.CharField(max_length=20)
    confirm_account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=20)
    transfer_to = models.ForeignKey(Facility)
    request_details = models.OneToOneField(RequestDetail,related_name='request_details')


class UtilityBillRequest(models.Model):
    BILL = ((1,'Internet'),(2,'Electricity'),(3,'WaterBill'),(4, 'Houserent'))
    type_of_bill = models.CharField(max_length=50, choices=BILL)
    bill_image = models.ImageField(upload_to='billpayment/%Y/%m/%d')
    requested_by = models.ForeignKey(Facility)
    request_details = models.OneToOneField(RequestDetail,related_name='request_detail')

class CashEntry(models.Model):
    CATEGORY =((1,'Travel Expense'),(2,'Groceries'))
    created_date = models.DateField(auto_now_add=True)
    fellow = models.ForeignKey(NgUser, related_name='cash_entry', related_query_name = 'cash_entry')
    facility=models.ForeignKey(Facility, null = True)
    expense_amount = models.IntegerField(null=True)
    payment_amount = models.IntegerField(null=True)
    category = models.CharField(max_length=25, choices= CATEGORY, null = True)
    is_personal_expense = models.BooleanField(default=False)
    is_facility_expense = models.BooleanField(default=False)
    is_pay_forward = models.BooleanField(default=False)
    is_payment_to_ng = models.BooleanField(default=False)
    bank_screenshot = models.ImageField(upload_to="bank_screenshot/%Y/%m/%d", null=True)
    fellow_payment_screenshot = models.ImageField(upload_to=fellowscreenshot, null=True)
    bill_image = models.ImageField(upload_to="billimage/%Y/%m/%d",null = True)
    description = models.TextField(null= True)
