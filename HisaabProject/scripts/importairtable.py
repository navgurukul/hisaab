import csv
from HisaabApp.models import *

with open('student.csv' ) as f:
        reader = csv.reader(f)
        for row in reader:
            _, created = CashEntry.objects.get_or_create(
		fellow=row[1],
		created_date=row[2],
		expense_amount=row[3],
		category=row[5],
		description=row[6],
		facility=row[7],
		is_facility_expense=row[8])
