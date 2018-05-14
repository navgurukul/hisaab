#from HisaabApp.models import *
import csv
#import pprint

with open('airtable.csv', 'rb') as csvfile:
	re = csv.DictReader(csvfile)
	dict_list = []
	for row in re:
		dict_list.append(row)
		airtable_data = dict_list.append(row)
		#pprint.pprint(dict_list)
		#print(row['Source'], row['Expense Made By'])
		expence_made = row['Expense Made By']
		#print(expence_made)
		expence_date = row['Expense Date']
		#print(expence_date)
		source = row['Source']
		#print(source)
		category = row['Category']
		#print(category)
		Description = row['Description']
		#print(Description)
		campus = row['Campus']
		#print(campus)
for line in airtable_data:
	nguser = NgUser.object.create(user=line[1], facility=line[8])
	nguser.save()


