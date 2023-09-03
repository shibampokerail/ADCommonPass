#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog
import os
import sys

					
					
def show_popup(msg):
	popup = tk.Tk()
	
	popup.title("AdAudit - Blessing Health System")

	label = tk.Label(popup, text=msg)
	label.pack(padx=20, pady=10)

	close_button = tk.Button(popup, text="Close", command=popup.destroy)
	close_button.pack(pady=10)
	popup.mainloop()	

def getArgs(supress_warnings=True):
	if len(sys.argv) < 2:
		return
	else:
		for i in sys.argv:
			command = str(i)
			mode = command.split("=")[0]
			if mode =="-pop":
				if len(command.split("="))==2:	
					show_popup(command.split("=")[1])
	exit()

getArgs()							

def select_file(button):
    file_path = filedialog.askopenfilename()
    if button == 1:
        file1_label.config(text=f"NTDS.dit path: {file_path}")
        global file1_path
        file1_path = file_path
    elif button == 2:
        file2_label.config(text=f"SYSTEM path: {file_path}")
        global file2_path
        file2_path = file_path

def run_ad_audit():
   # print(list(checkbox_vars.keys())[0])
    external_commands = ""
    if checkbox_vars[list(checkbox_vars.keys())[0]].get()==1:  
    	external_commands += " -a"
    if checkbox_vars[list(checkbox_vars.keys())[1]].get()==1:  
    	external_commands += " -c"
    if checkbox_vars[list(checkbox_vars.keys())[2]].get()==1:  
    	external_commands += " -r"
    if enable_checkbox_var.get() == 1:
    	if text_entry.get()=="":
    		os.system("./gui_adCommonPass.py -pop='Username field cannot be empty.'")
    		return
    	external_commands += ' -searchusr=' + text_entry.get()
    
    
    print(external_commands)
    
    if file1_path and file2_path:
      #	os.system(f"./gui_adCommonPass.py -pop='{external_commands}'")
        os.system(f"./ad-passwords-test.py -ntds='{file1_path}' -sys='{file2_path}' -gui {external_commands}")
    else:
        os.system("./gui_adCommonPass.py -pop='Please select both files.'")

def toggle_textbox_state():
    if enable_checkbox_var.get() == 1:
        text_entry.config(state="normal")
    else:
        text_entry.config(state="disabled")
root = tk.Tk()
file1_path = None
file2_path = None

root.title("AD Audit - Blessing Health System")
root.geometry("500x370")

file1_label = tk.Label(root, text="NTDS.dit path:")
file2_label = tk.Label(root, text="SYSTEM path:")

select_file1_button = tk.Button(root, text="Select Ntds.dit", command=lambda: select_file(1))
select_file2_button = tk.Button(root, text="Select system file", command=lambda: select_file(2))

checkbox_vars = {}  # Dictionary to store checkbox variables

options = ["create a text file with all usernames and password hashes", "create a text file grouping all common password hashes together", "create csv reports of accounts sharing passwords"]

print_button = tk.Button(root, text="Start Process!", command=run_ad_audit)

file1_label.pack(pady=10,padx=10,anchor='w')
select_file1_button.pack(padx=10,anchor='w')
file2_label.pack(pady=10,padx=10,anchor='w')
select_file2_button.pack(padx=10,anchor='w')

for option in options:
    checkbox_vars[option] = tk.IntVar()  # IntVar to hold checkbox state
    checkbox = tk.Checkbutton(root, text=option, variable=checkbox_vars[option])
    checkbox.pack(pady=5,anchor='w')

enable_checkbox_var = tk.IntVar()
enable_checkbox = tk.Checkbutton(root, text="Search for a specific user's password hash:", variable=enable_checkbox_var, command=toggle_textbox_state)
enable_checkbox.pack(pady=5,anchor='w')

username = tk.Label(root, text="Username:")
username.pack(padx=10,anchor='w')
text_entry = tk.Entry(root, state="disabled")
text_entry.pack(padx=10,anchor='w')

print_button.pack(padx=10,pady=10,anchor='e')

root.mainloop()
