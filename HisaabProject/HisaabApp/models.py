from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from HisaabProject.custom_storages import MediaStorage
import datetime


#********* path to save the images in media folder **************
def fellowScreenshot(instance , filename):
    return 'fellowpayment/{0}/{1}'.format(instance.fellow.user.id, filename)
def bankScreenshot(instance , filename):
    return 'bankScreenshot/{0}/{1}'.format(instance.fellow.user.id, filename)
def billImage(instance , filename):
    return 'billimage/{0}/{1}'.format(instance.fellow.user.id, filename)
#************************************************************************************

#Category for expenses can be added by admin
class Category(models.Model):
    name= models.CharField(max_length=30)

    def __str__(self):
        return self.name


# The Facility model is created for assign the name of facility and expense limit of particular facility.
class Facility(models.Model):
    name = models.CharField(max_length=50)
    student_expenses_limit = models.IntegerField()
    cash_in_hand = models.IntegerField(default=0)

    # Settings the name of instance
    def __str__(self):
        return self.name

# The NgUser models create  for add the user type , created date of user and there upi id .
class NgUser(models.Model):
    ROLES = (('ADMIN','admin'),('SUPER_ADMIN','super_admin'),('FELLOW','fellow'))
    user_type = models.CharField(choices=ROLES,max_length=11,default='FELLOW',blank=False)
    user = models.OneToOneField(User,unique=True, related_query_name = 'nguser', on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    facility = models.ForeignKey(Facility,blank=True, null=True) # think of this as current_facility
    has_account_id = models.BooleanField(default=False)
    # #for fellow
    # account_id = models.CharField(max_length=40, blank= True, null=True)

    #To display the name of the model instance.
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    # the function created for calculate the total time of fellows in Navgurukul.
    def total_time_in_ng(self):
        # print timezone.now(), self.created_date
        return (datetime.date.today() - self.created_date).days

    ###############################################################
    # Still need to add payforward entry calculation
    ###############################################################
    # the function for calculate the total weekly expense of fellow.
    def total_weekly_expenses(self):
        fellow_balance = (self.total_time_in_ng()/7) * self.facility.student_expenses_limit
        personal_expense = CashEntry.objects.filter(fellow__id=self.id,is_personal_expense=True)
        personal_amount = 0
        for expense in personal_expense:
            personal_amount  += expense.expense_amount
        fellow_balance = fellow_balance + personal_amount
        return fellow_balance

    # the function created for calculate the last weekly expense of facility for reminding the students.
    def last_week_facility_expenses(self):
        today = datetime.date.today()
        weekend_date = today - datetime.timedelta(today.weekday()+1)
        last_week_date = weekend_date - datetime.timedelta(7)
        last_week_expense=CashEntry.objects.filter(created_date__range=(last_week_date,weekend_date),is_personal_expense=True, facility = self.facility)
        last_week_amount = 0
        for expense in last_week_expense:
            last_week_amount += expense.expense_amount
        return last_week_amount

    # the function create for calculate the last month facility expense .
    def last_month_facility_expense(self):
        today = datetime.date.today()
        last_month_enddate = today.replace(day=1)-datetime.timedelta(1)
        last_month_startdate = last_month_enddate.replace(day=1)
        last_month_expense=CashEntry.objects.filter(created_date__range=(last_month_startdate,last_month_enddate),is_personal_expense=True, facility = self.facility)
        last_month_amount = 0
        for expense in last_month_expense:
            last_month_amount += expense.expense_amount
        return last_month_amount

    #******* flags for checking user user_type ********
    def is_fellow(self):
        return self.user_type == 'FELLOW'

    def is_admin(self):
        return self.user_type == 'ADMIN'

    def is_super_admin(self):
        return self.user_type == 'SUPER_ADMIN'
    # *************************************************



    #flag to check if student facility has exceed weekly facility expense limit.
    def in_weekly_limit(self):
        total_fellow = len(NgUser.objects.all().filter(facility = self.facility))
        total_limit = total_fellow * self.facility.student_expenses_limit
        if int(total_limit) - self.last_week_facility_expenses() > 0:
            return True
        return False

    #calculate expense exceed by per student in facility of last week
    def week_limit_exceed_by(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        total_limit = total_fellow * self.facility.student_expenses_limit
        return abs(int(total_limit - self.last_week_facility_expenses())/total_fellow)


    #flag to check if student facility has exceed monthly facility expense limit.
    def in_monthly_limit(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        today = datetime.date.today()
        last_month_enddate = today.replace(day=1)-datetime.timedelta(1)
        last_month_startdate = last_month_enddate.replace(day=1)

        total_limit = (total_fellow * self.facility.student_expenses_limit)/7 *((last_month_enddate - last_month_startdate).days+1)
        if int(total_limit) - self.last_month_facility_expense() > 0:
            return True
        return False

    #calculate expense exceed by per student in facility of last month
    def month_limit_exceed_by(self):
        total_fellow = len(NgUser.objects.filter(facility = self.facility))
        today = datetime.date.today()
        last_month_enddate = today.replace(day=1)-datetime.timedelta(1)
        last_month_startdate = last_month_enddate.replace(day=1)
        total_limit = (total_fellow * self.facility.student_expenses_limit)/7 *((last_month_enddate - last_month_startdate).days+1)
        return abs((self.last_month_facility_expense() - int(total_limit))/total_fellow)


# Model to handle all account details when request is made
class AccountDetail(models.Model):
    #Fields specifically for BillPaymentRequest
    account_number = models.CharField(max_length=40, default="")
    IFSC_code = models.CharField(max_length=40)
    account_holder_name = models.CharField(max_length=40)


#Model to handle all kind of Money and Bill requests data
class MoneyRequest(models.Model):
    #Fields specifically for BillPaymentRequest
    BILL = (('INTERNET','Internet'),('ELECTRICITY','Electricity'),('WATER','WaterBill'),('HOUSERENT', 'Houserent'))
    is_utility_request= models.BooleanField(default=False)
    type_of_bill = models.CharField(max_length=50, choices=BILL, blank=True, null =True)
    bill_image = models.FileField(upload_to='billpayment/%Y/%m/%d', blank=True, null = True)

    #Fields specifically for TransferRequest
    is_money_request= models.BooleanField(default=False)
    account_detail = models.OneToOneField(AccountDetail, blank=True, null =True)

    #Fields that are included in both TransferRequest and BillPaymentRequest
    facility = models.ForeignKey(Facility,null=True,blank=True)
    money_requested_by = models.ForeignKey(NgUser,null=True, related_name = "money_requested_by", blank=True)
    amount = models.IntegerField()
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_approve = models.BooleanField(default=False)
    is_queued = models.BooleanField(default=True)
    reason_for_reject = models.TextField(null=True,blank=True)
    approve_or_rejected_by = models.ForeignKey(NgUser, related_name='approve_or_rejected_by',null=True)

    def __str__(self):
        return '{0}'.format(self.created_date)

#Model to Handle all the cash Entry made in Ng
class CashEntry(models.Model):

    #Add Expense Fields
    category = models.ForeignKey(Category, default=1)
    expense_amount = models.IntegerField(blank=True, null=True)
    bill_image = models.FileField(upload_to=billImage,blank=True, null = True)
    is_personal_expense = models.BooleanField(default=False) # INN SAAREIN BOOLEANS KO REPLACE EK SIMPLE SA BOOLEAN BANANA HAI
    is_facility_expense = models.BooleanField(default=False)
    fellow = models.ForeignKey(NgUser, related_name='cash_entry', related_query_name = 'cash_entry')

    #Record Payment Fields
    is_payment_to_ng = models.BooleanField(default=False)
    bank_screenshot = models.FileField(upload_to=bankScreenshot, blank=True, null=True)
    payment_amount = models.IntegerField(blank=True, null=True)

    #to handle payforward
    is_pay_forward = models.BooleanField(default=False)
    fellow_payment_screenshot = models.FileField(upload_to=fellowScreenshot, blank=True, null=True)

    #Fields for AddExpense, RecordPayment
    created_date = models.DateField(default = timezone.now)
    facility=models.ForeignKey(Facility, blank=True, null = True)
    description = models.TextField(blank=True, null= True)
    cash_in_hand_currently = models.IntegerField(default= 0, blank = True, null= True) # TODO ISSE HATA DO

    def __str__(self):
        return '{0}'.format(self.fellow)
