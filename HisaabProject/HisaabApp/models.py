from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime

def fellowScreenshot(instance , filename):
    return 'fellowpayment/{0}/{1}'.format(instance.fellow.user.id, filename)
def bankScreenshot(instance , filename):
    return 'bankScreenshot/{0}/{1}'.format(instance.fellow.user.id, filename)
def billImage(instance , filename):
    return 'billimage/{0}/{1}'.format(instance.fellow.user.id, filename)

class Facility(models.Model):
    name = models.CharField(max_length=50)
    student_expenses_limit = models.IntegerField()
    cash_in_hand = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class NgUser(models.Model):
    ROLES = (('ADMIN','admin'),('FELLOW','fellow'))
    user_type= models.CharField(choices=ROLES,max_length=6,default='FELLOW',blank=False)
    user = models.OneToOneField(User,unique=True, related_query_name = 'nguser', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    upi_id = models.CharField(max_length=40, blank= True, null=True)
    facility= models.ForeignKey(Facility,blank=True, null=True, )

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    def total_time_in_ng(self):
        print timezone.now(), self.created_date
        return (datetime.date.today() - self.created_date).days

    def total_weekly_expenses(self):
        fellow_balance = (self.total_time_in_ng()/7) * self.facility.student_expenses_limit
        personal_expense = CashEntry.objects.filter(fellow__id=self.id,is_personal_expense=True) 
        personal_amount = 0
        for expense in personal_expense:
            personal_amount  += expense.expense_amount  
        fellow_balance = fellow_balance + personal_amount
        return fellow_balance

    def last_week_facility_expenses(self):
        today = datetime.date.today()   
        weekend_date = today - datetime.timedelta(today.weekday()+1)
        last_week_date = weekend_date - datetime.timedelta(7)
        last_week_expense=CashEntry.objects.filter(created_date__range=(last_week_date,weekend_date),is_facility_expense=True, facility = self.facility)
        last_week_amount = 0
        for expense in last_week_expense:
            last_week_amount += expense.expense_amount
        return last_week_amount

    def last_month_facility_expense(self):
        today = datetime.date.today()   
        last_month_enddate = today.replace(day=1)-datetime.timedelta(1)
        last_month_startdate = last_month_enddate.replace(day=1)    
        last_month_expense=CashEntry.objects.filter(created_date__range=(last_month_startdate,last_month_enddate),is_facility_expense=True, facility = self.facility)
        last_month_amount = 0
        for expense in last_month_expense:
            last_month_amount += expense.expense_amount
        return last_month_amount

    def is_fellow(self):
        return self.user_type == 'FELLOW'

    def is_admin(self):
        return self.user_type == 'ADMIN'


    def in_weekly_limit(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        total_limit = total_fellow * self.facility.student_expenses_limit
        if total_limit - self.last_week_facility_expenses > 0:
            return True
        return False 

    def week_limit_exceed_by(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        total_limit = total_fellow * self.facility.student_expenses_limit
        return total_limit - self.last_week_facility_expenses

    def in_monthly_limit(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        today = datetime.date.today()   
        last_month_enddate = today.replace(day=1)-datetime.timedelta(1)
        last_month_startdate = last_month_enddate.replace(day=1)  

        total_limit = (total_fellow * self.facility.student_expenses_limit)/7 *(last_month_startdate - last_month_enddate).days
        if int(total_limit) - self.last_month_facility_expenses > 0:
            return True
        return False 
    def month_limit_exceed_by(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        today = datetime.date.today()   
        last_month_enddate = today.replace(day=1)-datetime.timedelta(1)
        last_month_startdate = last_month_enddate.replace(day=1)  
        total_limit = (total_fellow * self.facility.student_expenses_limit)/7 *(last_month_startdate - last_month_enddate).days
        return int(total_limit) - self.last_month_facility_expenses

class MoneyRequest(models.Model):
    BILL = (('INTERNET','Internet'),('ELECTRICITY','Electricity'),('WATER','WaterBill'),('HOUSERENT', 'Houserent'))
    is_money_request= models.BooleanField(default=False)
    is_utility_request= models.BooleanField(default=False)
    money_requested_by = models.ForeignKey(NgUser,null=True, related_name = "money_requested_by", blank=True)
    money_received_by = models.ForeignKey(NgUser, related_name = "money_received_by",null=True,blank=True)
    facility = models.ForeignKey(Facility,null=True,blank=True)
    type_of_bill = models.CharField(max_length=50, choices=BILL, blank=True, null =True)
    bill_image = models.ImageField(upload_to='billpayment/%Y/%m/%d', blank=True, null = True)
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    is_approve = models.BooleanField(default=False)
    is_queued = models.BooleanField(default=True)
    reason_for_reject = models.TextField(null=True,blank=True)
    approve_or_rejected_by = models.ForeignKey(NgUser, related_name='approve_or_rejected_by',null=True)

    def __str__(self):
        return '{0}'.format(self.created_date)

class CashEntry(models.Model):
    CATEGORY =(('TRAVEL','Travel Expense'),('GROCERIES','Groceries'),('VEGETABLES','Vegetables'), ('HOUSEHOLD','HouseholdItems'),('EGG','Egg'),('MILK','Milk & Bread'),('TECH EXPENCE','Tech Expenses'),('OTHER','Other'))
    created_date = models.DateField(default = timezone.now)
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
