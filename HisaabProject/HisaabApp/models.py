from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def fellowScreenshot(instance , filename):
    return 'fellowpayment/{0}/{1}'.format(instance.user.id, filename)
def bankScreenshot(instance , filename):
    return 'bankScreenshot/{0}/{1}'.format(instance.user.id, filename)
def billImage(instance , filename):
    return 'billimage/{0}/{1}'.format(instance.fellow.id, filename)

class Facility(models.Model):
    name = models.CharField(max_length=50)
    student_expenses_limit = models.IntegerField()

    def __str__(self):
        return self.name

class NgUser(models.Model):
    ROLES = (('ADMIN','admin'),('FELLOW','fellow'))
    user_type= models.CharField(choices=ROLES,max_length=6,default='FELLOW',blank=False)
    user = models.OneToOneField(User,unique=True, related_query_name = 'nguser', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    upi_id = models.CharField(max_length=40, blank= True, null=True)
    facility= models.ForeignKey(Facility,blank=True, null=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name




class MoneyRequest(models.Model):
    BILL = (('INTERNET','Internet'),('ELECTRICITY','Electricity'),('WATER','WaterBill'),('HOUSERENT', 'Houserent'))
    is_money_request= models.BooleanField(default=False)
    is_utility_request= models.BooleanField(default=False)
    nguser = models.ForeignKey(NgUser,null=True,blank=True)
    facility = models.ForeignKey(Facility,null=True,blank=True)
    type_of_bill = models.CharField(max_length=50, choices=BILL, blank=True, null =True)
    bill_image = models.ImageField(upload_to='billpayment/%Y/%m/%d', blank=True, null = True)
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField(default=False)
    is_queued = models.BooleanField(default=True)
    approve_or_rejected_by = models.ForeignKey(NgUser, related_name='approve_or_rejected_by',null=True)

    def __str__(self):
        return '{0}'.format(self.created_date)

class CashEntry(models.Model):
    CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
    created_date = models.DateField()
    fellow = models.ForeignKey(NgUser, related_name='cash_entry', related_query_name = 'cash_entry')
    facility=models.ForeignKey(Facility, blank=True, null = True)
    expense_amount = models.IntegerField(blank=True, null=True)
    payment_amount = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=25, choices= CATEGORY, blank=True, null = True)
    is_personal_expense = models.BooleanField(default=False)
    is_facility_expense = models.BooleanField(default=False)
    is_pay_forward = models.BooleanField(default=False)
    is_payment_to_ng = models.BooleanField(default=False)
    bank_screenshot = models.ImageField(upload_to=bankScreenshot, blank=True, null=True)
    fellow_payment_screenshot = models.ImageField(upload_to=fellowScreenshot, blank=True, null=True)
    bill_image = models.ImageField(upload_to=billImage,blank=True, null = True)
    description = models.TextField(blank=True, null= True)

    def __str__(self):
        return '{0}'.format(self.fellow.user)
