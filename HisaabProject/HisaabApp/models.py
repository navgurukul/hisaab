from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def fellowscreenshot(instance , filename):
    return 'billpayment/{0}/{1}'.format(instance.user.id, filename)

class Facility(models.Model):
    name = models.CharField(max_length=50)
    student_expenses_limit = models.IntegerField()

    def __str__(self):
        return self.name

class NgUser(models.Model):
<<<<<<< HEAD
    ROLES = ((1,'admin'),(2,'fellow'))
    user = models.OneToOneField(User,unique=True, null=False)
    created_date = models.DateField(auto_now_add=True)
    user_type= models.CharField(choices=ROLES,max_length=20,blank=False)
    facility= models.ForeignKey(Facility,null=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         NgUser.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
=======
    user = models.OneToOneField(User,unique=True)
    created_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_fellow = models.BooleanField(default=False)
    facility= models.ForeignKey(Facility,blank=True, null=True)

    def __str__(self):
        return self.user.username
>>>>>>> 1c295bea59ddae672e31cf4b14ee2b4446fe03fd

class MoneyTransferRequest(models.Model):
    BILL = ((1,'Internet'),(2,'Electricity'),(3,'WaterBill'),(4, 'Houserent'))
    account_number = models.CharField(max_length=20, blank=True, null = True)
    ifsc_code = models.CharField(max_length=20, blank=True, null= True)
    is_money_request= models.BooleanField(default=False)
    is_utility_request= models.BooleanField(default=False)
    account_holder_name = models.CharField(max_length=20, blank=True, null=True)
    type_of_bill = models.CharField(max_length=50, choices=BILL, blank=True, null =True)
    bill_image = models.ImageField(upload_to='billpayment/%Y/%m/%d', blank=True, null = True)
    facility = models.ForeignKey(Facility)
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField()
    is_queued = models.BooleanField(default=True)
<<<<<<< HEAD
    approve_or_rejected_by = models.ForeignKey(NgUser, limit_choices_to={'user_type':2})
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
=======
    approve_or_rejected_by = models.ForeignKey(NgUser, limit_choices_to={'is_admin':True})
    reject_text = models.TextField(blank=True, null=True)
>>>>>>> 1c295bea59ddae672e31cf4b14ee2b4446fe03fd

class CashEntry(models.Model):
    CATEGORY =((1,'Travel Expense'),(2,'Groceries'))
    created_date = models.DateField(auto_now_add=True)
    fellow = models.ForeignKey(NgUser, related_name='cash_entry', related_query_name = 'cash_entry')
    facility=models.ForeignKey(Facility, blank=True, null = True)
    expense_amount = models.IntegerField(blank=True, null=True)
    payment_amount = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=25, choices= CATEGORY, blank=True, null = True)
    is_personal_expense = models.BooleanField(default=False)
    is_facility_expense = models.BooleanField(default=False)
    is_pay_forward = models.BooleanField(default=False)
    is_payment_to_ng = models.BooleanField(default=False)
    bank_screenshot = models.ImageField(upload_to="bank_screenshot/%Y/%m/%d", blank=True, null=True)
    fellow_payment_screenshot = models.ImageField(upload_to=fellowscreenshot, blank=True, null=True)
    bill_image = models.ImageField(upload_to="billimage/%Y/%m/%d",blank=True, null = True)
    description = models.TextField(blank=True, null= True)
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         NgUser.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
