import os
#os.chdir("D:\Airtel-Chad-USSD-MO-CDR's-6months")
root = "D:\Airtel-Chad-USSD-MO-CDR's-6months"
for root, dirs, files in os.walk(root):
	for FILENAME in files:
		#make sure file is a log file and is called ProcessHistory
		if not FILENAME.endswith('.gz'):
			fd = open(root+"\\"+FILENAME, 'r')
			#print(FILENAME)
			#open it with read only privilages
			for line in fd:
				print line