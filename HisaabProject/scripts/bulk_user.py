import csv
from HisaabApp.models import User, NgUser, Facility
with open( "data/users.csv" ) as f:
	reader = csv.reader(f)
	reader.next()

	for row in reader:
		print row     
	    user, created = User.objects.get_or_create(
	    	first_name=row[0],
	        last_name=row[1],                
	        email=row[2],                
	        username=row[3],            
	        )           
	# Add facilities   
	facility_names = ["Dharamsala Facility", "Gurgaon - Girls Facility", "Sarita Vihar - Boys Facility", "Gurgaon - Boys facility", "Chikballapur Facility"]            
	for facility_name in facility_names:
		Facility.objects.get_or_create(
			name = facility_name,
	        student_expenses_limit = 1750,      
	        #cash_in_hand = 0                
	        )            
	        facility_subname = row[4]            
	        facility = Facility.objects.filter(name__icontains=facility_subname)[0]            
	        print user.id, facility.id           
	        _, created = NgUser.objects.get_or_create(
	        	user = User.objects.get(id=user.id),
	            facility = facility                
	            # has_account_id = models.BooleanField(default=False)            
	            )