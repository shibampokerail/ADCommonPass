#!/usr/bin/env python3

import os
import sys
try:
	import pyperclip # it is usually installed in kali linux (just to be safe)
except:
	os.system("pip install pyperclip")
	import pyperclip


def getArgs(supress_warnings=True):
    valid_command = True
    if os.path.isfile("gui_adCommonPass.py"):
        if len(sys.argv) < 2:
            os.system("./gui_adCommonPass.py")
            exit()
    else:
        if not supress_warnings:
            print("GUI mode not available. Please enter correct parameters.")
            exit()

    ntds_path = ""
    system_path = ""
    gui = False
    generate_all_hash = False
    generate_common_hash = False
    generate_report_hash =  False
    files_count = 0
    search_username =""

    for i in sys.argv:
        a = str(i)
        if a.startswith("-ntds="):
            ntds_path = (a.split("=")[1])
            print("ntds:", ntds_path)
            files_count = -1
        elif a.startswith("-sys="):
            system_path = (a.split("=")[1])
            print("sys:", system_path)
            files_count += 1
        elif a.startswith("-searchusr="):
            search_username = (a.split("=")[1])
            print("username:", search_username)
            
        elif a.startswith("-gui"):
            gui=True
        elif a.startswith("-a"):
            generate_all_hash = True
        elif a.startswith("-c"):
            generate_common_hash = True
        elif a.startswith("-r"):
            generate_report_hash = True
        else:
            if sys.argv.index(i)!=0:
            	invalidCommand(i)

    if files_count == 1:
        invalidCommand("enter path to your ntds file using:   -ntds=<your path>")
    if files_count == -1:
        invalidCommand("enter path to your ntds file using:   -sys=<your path>")

    return {"ntds_path":ntds_path, "system_path":system_path, "gui":gui, "a":generate_all_hash, "c":generate_common_hash, "r":generate_report_hash, "username":search_username}


def invalidCommand(cmd):
    print("Invalid Command:", cmd)
    exit()

def search_user(username, filepath):
    search_sequence = username  
    file_path = filepath   

    with open(file_path, "r") as file:
        for line in file:
            if search_sequence in line:
                return line
                
        return f"No user with username {username} was found"
                
    


def checkForRequiredFiles():
    # Checks for files required before running the script.
    # Also provides excecute permission to the python files.

    no_of_present_files = 0
    total_files_required = 2

    if not (os.path.isfile("secretsdump.py")):
        print("secretsdump.py not found.")
    else:
        os.system("chmod +x secretsdump.py")
        no_of_present_files += 1

    if not (os.path.isfile("checkHash.py")):
        print("checkHash.py not found.")
    else:
        os.system("chmod +x checkHash.py")
        no_of_present_files += 1

    print(f"{no_of_present_files}/{total_files_required} required files validated!")

    if (no_of_present_files != total_files_required):
        exit()
        # looked really messy
        raise ValueError(f"{total_files_required - no_of_present_files} files missing!")

def generateReport(common_hashes_txt):
	pass
	

temp_hash_storage_folder = "password_hashes"

if __name__ == "__main__":
    checkForRequiredFiles()
    files_path = getArgs()
    modes_count = ""
    
    if files_path['gui'] == True:
    	os.system("echo running in gui mode....")
    
    # creating a temp hash storage folder if it does not exist
    if not (os.path.exists(temp_hash_storage_folder) and os.path.isdir(temp_hash_storage_folder)):
        os.system(f"mkdir {temp_hash_storage_folder}")

    print("Extracting hashes from ndts.dit.....")

    os.system(f"secretsdump.py -ntds '{files_path['ntds_path']}' -system '{files_path['system_path']}' LOCAL -outputfile {temp_hash_storage_folder}/hashes.txt")
    os.system(f"./checkHash.py {temp_hash_storage_folder}/hashes.txt.ntds")
    os.system(f"./checkHash.py {temp_hash_storage_folder}/hashes.txt.ntds > {temp_hash_storage_folder}/grouped_shared_password_hashes.txt")
    
    if files_path['username']!="":
    	result = search_user(files_path['username'],f'{temp_hash_storage_folder}/hashes.txt.ntds')
    	if ":" in result:
    		pyperclip.copy(result)
    		os.system(f"./gui_adCommonPass.py -pop='{result} \n It has been copied to the clipboard.'")
    	else:
    		os.system(f"./gui_adCommonPass.py -pop='{result}!'")
    	
    	
    if not files_path['r']:
    	pass
    else:
    	os.system(f"./generateReport.py")
    	os.system(f"echo common password hashes report created")
    	modes_count+="r"
    
    if not files_path['a']:
    	os.system(f"rm {temp_hash_storage_folder}/hashes.txt.ntds")
    	os.system(f"rm {temp_hash_storage_folder}/hashes.txt.ntds.cleartext")
    	os.system(f"rm {temp_hash_storage_folder}/hashes.txt.ntds.kerberos")
    else:
    	os.system(f"echo all password hashes with usernames created at {temp_hash_storage_folder}")
    	modes_count+="a"
 
    if not files_path['c']:
    	os.system(f"rm {temp_hash_storage_folder}/grouped_shared_password_hashes.txt")
    else:
    	os.system(f"echo groups of shared password hashes with usernames created at {temp_hash_storage_folder}")
    	modes_count+="c"
    	
    if files_path['gui']:
    	if ('r' in modes_count) or ("c" in modes_count) or ("a" in modes_count):
    		os.system(f"./gui_adCommonPass.py -pop='Success! Your output files are located in the {temp_hash_storage_folder} or report folder.'")
    	else:
    		os.system(f"./gui_adCommonPass.py -pop='Complete!'")
    else:
    	os.system(f"echo Your output files are located in the {temp_hash_storage_folder} folder.")
