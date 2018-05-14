import csv
from datetime import datetime,date
from HisaabApp.models import *

with open('data/girls_expense.csv' ) as f:
        reader = csv.reader(f)
        reader.next()

        last_added_name = ""

        for row in reader:
            # print row[1]
            date=row[0]
            date=datetime.datetime.strptime(date, "%Y-%m-%d")
            amount=row[2]
            # print row
            if amount == '':
                amount = None
            try:
                amount = int(amount)
                # print type(amount)
            except:
                pass
            user = row[4].split(",")[0]
            if user:
                user = user.split()[0]
                last_added_name = user
            else:
                user = last_added_name

            facility = Facility.objects.filter(name__icontains="Gurgaon - Girls")[0]

                      # Find corresponding user from the user name
            print user
            userObj = User.objects.filter(username__icontains=user[:5]).first()
            if not userObj:
                User.objects.filter(first_name__icontains=user).first()

            if not userObj:
                print row
                print "YEH KAHA AAAAAAAA GAYE HUMMMMMMMM!!!!!!!!!"

            ngUserObj = NgUser.objects.get(user=userObj.id)

            category, created = Category.objects.get_or_create(
                          name=row[1][:30]
                      )

            _, created = CashEntry.objects.get_or_create(

                      fellow = ngUserObj,
                      created_date=date,
                      expense_amount=amount,
                      category=category,
                      description=row[3],
                      facility=facility,
                      is_facility_expense=1
                      )
