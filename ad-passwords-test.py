#!/usr/bin/env python3


import os

def checkForRequiredFiles():
	#Checks for files required before running the script.
	#Also provides excecute permission to the python files.
	
	
	no_of_present_files = 0
	total_files_required = 4
	
	
	
	if not (os.path.isfile(os.path.join('ntds', 'ntds.dit')) or os.path.isfile(os.path.join('ntds', 'NTDS.dit'))):
		print("ntds.dit not found in the ntds folder! Please put your ntds.dit file in the ntds folder or if it already exists there, rename it to ntds.dit")
	else:
		no_of_present_files+=1
		
	if not (os.path.isfile(os.path.join('ntds', 'system')) or os.path.isfile(os.path.join('ntds', 'SYSTEM'))):
		print("system file not found in the ntds folder! Please put your system file in the ntds folder or if it already exists there, rename it to system")
	else:
		no_of_present_files+=1
		
	if not (os.path.isfile("secretsdump.py")):
		print("secretsdump.py not found.")
	else:
		os.system("chmod +x secretsdump.py")
		no_of_present_files+=1
		
	if not (os.path.isfile("checkHash.py")):
		print("checkHash.py not found.")
	else:
		os.system("chmod +x checkHash.py")
		no_of_present_files+=1
	
	print(f"{no_of_present_files}/{total_files_required} files found!")
	
	if (no_of_present_files!=total_files_required): 
		exit()
		#looked really messy
		raise ValueError(f"{total_files_required - no_of_present_files} files missing!")
	
temp_hash_storage_folder = "temp_hashes"

if __name__ == "__main__":
  	checkForRequiredFiles()
  	
  	#creating a temp hash storage folder if it does not exist
  	if not (os.path.exists(temp_hash_storage_folder) and os.path.isdir(temp_hash_storage_folder)):
  		os.system(f"mkdir {temp_hash_storage_folder}")
  	
  	print("Extracting hashes from ndts.dit.....")
	
  	os.system(f"secretsdump.py -ntds ntds/ntds.dit -system ntds/system LOCAL -outputfile {temp_hash_storage_folder}/hashes.txt")
  	os.system(f"./checkHash.py {temp_hash_storage_folder}/hashes.txt.ntds")
