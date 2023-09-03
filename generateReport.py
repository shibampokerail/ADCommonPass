#!/usr/bin/env python3

import os
import datetime
import csv

os.system(f"./checkHash.py password_hashes/hashes.txt.ntds > password_hashes/grouped_shared_password_hashes.txt")

c = ""
commons = []
sharers = []
all_data = []

with open("password_hashes/grouped_shared_password_hashes.txt", 'r') as hashes_txt:
    groups = 1
   
    while True:
        c = hashes_txt.readline()
        
        if not c:
            break
        all_data.append(c)            
        c = c.split(" ")
        username = c[0]

        if username.strip() != "":
           # print(c[0])
            sharers.append(c[0])
            
        else:
            groups += 1
           # print()
            commons.append(sharers)
            sharers = []

    #print(groups)
    #print(commons)
    #print(sharers)

admin_accounts = []
admin_with_other = []

superuser_accounts = []
superuser_with_other = []

BRCN_accounts = []
HLG_accounts = []
JWCC_accounts = []

other_depts = ['BRCN','HLG','JWCC','RAD','WIU','LAB','SCC']
report= {'admin':[],
	 'superuser':[],
	 'BRCN':[],'HLG':[],'JWCC':[],'RAD':[],'WIU':[],'LAB':[],'SCC':[]}
service_accs =['KIOSK','enexity',"ENEXITY","DISPLAY","WLBPSESuite","Office","EDUCTRAIN","PERAWATCH","room","EDScribe","telneur","conference","Conference","Auditorium","VD"]
common_password_hashes = {}
all_password_hashes = {}

for i in commons:
	for j in i:
		if len(i)>3:
			for service_account in service_accs:
							
							for data in all_data:
								if (j in data) and (service_account in j):	
									
									try:
										all_password_hashes.update({data.split(" ")[-1][:-1]:i})
									except:
										pass
						
		if "-admin" in j:
			admin_name = j.split("\\")[1]
			name = j.split("-")[0]
			name_count = 0
			other = [j]
			for k in i:
			    if name == k:
			       admin_accounts.append(j)
			       report['admin'].append(j)
			       
			    else:
			       if k not in other:
			       	other.append(k)
			
			if other not in admin_with_other and len(other)>1:
					admin_with_other.append(other)
			       
		if "-superuser" in j:
			super_name = j.split("\\")[1]
			name = j.split("-")[0]
			name_count = 0
			other = [j]
			for k in i:
			    if name == k:
			       superuser_accounts.append(j) 
			       report['superuser'].append(j)
			    else:
			       if k not in other:
			       	other.append(k)
			if other not in superuser_with_other and len(other)>1:
					superuser_with_other.append(other)
		
		for x in other_depts:
			if x in j:
				#print(i)
				BRCN_name = j.split("\\")[1]
				name = BRCN_name.split(x)[0]
				#print(BRCN_name)
				name_count = 0
				other = [j]
				for k in i:
			    		z = k.split("\\")[1]
			    		#print(name,z)
			    		if (name[:-2] in z) and (x not in z) and ("KIOSK" not in z.upper()) and ("DISPLAY" not in z.upper()):
			       			report[x].append(j) 
			    		else:
			       			if k not in other:
			       				other.append(k)
		
for i in commons:
	for j in i:
		if len(i)>3:
			for service_account in service_accs:
							
							for data in all_data:
								if (j in data) and (service_account not in j):	
									
									try:
										common_password_hashes.update({data.split(" ")[-1][:-1]:i})
									except:
										pass	      
			
		
			
			    


all_keys = all_password_hashes.keys()
common_passkeys = common_password_hashes.keys()

for key in all_keys:
	if key in common_password_hashes:
		del common_password_hashes[key]

#print(common_password_hashes)
#print()
#print(report)

try:
	max_length = max(len(lst) for lst in common_password_hashes.values())
except:
	print("No common passwords!")
	exit()

current_datetime = datetime.datetime.now()

folder_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

os.system(f"mkdir {folder_name}_report")


for key in common_password_hashes:
    common_password_hashes[key] += [None] * (max_length - len(common_password_hashes[key]))

csv_file_path = f"{folder_name}_report/common_passwords.csv"

with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header
    writer.writerow(common_password_hashes.keys())
    
    # Write the data rows
    for row in zip(*common_password_hashes.values()):
        writer.writerow(row)
    

max_length = max(len(lst) for lst in report.values())

for key in report:
    report[key] += [None] * (max_length - len(report[key]))

csv_file_path = f"{folder_name}_report/admin_pass_shared_with_personal.csv"

with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(report.keys())
    
    for row in zip(*report.values()):
        writer.writerow(row)







 	   
 		
 	
