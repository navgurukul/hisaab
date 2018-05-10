import csv
from HisaabApp.models import *

with open('data/sarita_vihar.csv' ) as f:
        reader = csv.reader(f)
        reader.next()

        last_added_name = ""

        # sample row
        # Milk & Bread-21,Shivam Monga,1 April 2017,-21,NavGurukul PayTM,Milk & Bread,bought by milk 21,4/1/2017 7:08am,SV,Navgurukul

        for row in reader:
            user = row[1].split(",")[0]
            if user:
                user = user.split()[0]
                last_added_name = user
            else:
                user = last_added_name

            facility = Facility.objects.filter(name__icontains="sarita")[0]

            # Find corresponding user from the user name
            print user
            userObj = User.objects.filter(username__icontains=user[:5]).first()
            if not userObj:
                User.objects.filter(first_name__icontains=user).first()
            if not userObj:
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
        		created_date=row[2],
        		expense_amount=row[3],
        		category=category,
        		description=row[6],
        		facility=facility,
        		is_facility_expense=1
            )
