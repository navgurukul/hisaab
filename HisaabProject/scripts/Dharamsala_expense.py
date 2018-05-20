import csv
from datetime import datetime
from HisaabApp.models import *
from django.shortcuts import render


with open('data/Dharamsala_expense.csv' ) as f:
        reader = csv.reader(f)
        reader.next()

        last_added_name = ""

        for row in reader:
            

            user = row[4].split(",")[0]
            if user == '':continue
            date=row[1]
            date=datetime.datetime.strptime(date, "%Y-%m-%d")
            amount= row[2]
            if amount == '':
                amount = None
            try:
                amount = int(amount)
                # print amount
            except:
                pass

            user = row[4].split(",")[0]

            if user:
                user = user.split()[0]
                last_added_name = user
            else:
                user = last_added_name

            facility = Facility.objects.filter(name__icontains="Dharamsala")[0]

            # Find corresponding user from the user name
            print row
            userObj = User.objects.filter(username__icontains=user[:5]).first()
            if not userObj:
                User.objects.filter(first_name__icontains=user).first()
            if not userObj:
                print row
                print "YEH KAHA AAAAAAAA GAYE HUMMMMMMMM!!!!!!!!!"

            ngUserObj = NgUser.objects.get(user=userObj.id)

            category, created = Category.objects.get_or_create(
                name=row[5][:30]
            )

            _, created = CashEntry.objects.get_or_create(
        		# expense_made_by=row[1],
        		# split_name=expense_made_by.split(','),
        		# fellow=split_name[0],
                fellow = ngUserObj,
        		created_date=date,
        		expense_amount=amount,
        		category=category,
        		description=row[0],
        		facility=facility,
        		is_facility_expense=1,
            )
