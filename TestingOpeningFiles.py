import os, hashlib
import pymongo
from pymongo import MongoClient
#import modules needed especially the pymongo modules
#which is a python integration for Mongo
root = "D:\Airtel-Chad-USSD-MO-CDR's-6months"
#the location of where the files were stored
USSDRequestHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","IMSI","SesID","USSD"]
USSDResponseHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","SesID","USSD","Status","Error"]
enter_to_database = ["Trans","Date","Time","CDRID","MSISDN","SesID","USSD","Status","Error"]
#define the attributes for each type of message
#and define the attributes that are wanted in the db
for root, dirs, files in os.walk(root):
	for FILENAME in files:
		#walk the directory and subdirectory and get every file
		listofdocuments = []
		client = MongoClient()
		db = client.FYP_Airtel_Storage
		collection = db.FYP_Data
		#open a connection to mongo db 
		if not FILENAME.endswith('.gz'):
			fd = open(root+"\\"+FILENAME, 'r')
			#open the files with read only privilages
			#and loop through each line
			for line in fd:
				count = 0
				document_content = {}
				if int(line.split(",")[2]) == 1:
					#this is finding the transaction id which states whether or not the 
					#message is USSD request or a response
					#Different arrays have to be used for the two and hence why the if statement is there
					for i in line.split(","):
						if USSDRequestHeaders[count] in enter_to_database:
							#make sure the sttribute is wanted in the db
							if '\n' in i:
								i=i.strip('\n')
								#ensure that no extra characters are saved
							if USSDRequestHeaders[count] == "MSISDN":
								#for privacy and ethical reasons the numbers in the db must be hashed
								i=hashlib.md5(i.encode()).hexdigest() 
							document_content[USSDRequestHeaders[count]] = i
							#create a dictionary for each transaction
							#NOTE: one for each response AND request
						count+=1
						#this is used to make sure the attribute assigned in the dictionary is pointing at the right
						#value from the files
				else:
					for i in line.split(","):
						#The same principle applies for USSD response messages
						if USSDResponseHeaders[count] in enter_to_database:
							if '\n' in i:
								i=i.strip('\n')
							if USSDResponseHeaders[count] == "MSISDN":
								i=hashlib.md5(i.encode()).hexdigest()
							document_content[USSDResponseHeaders[count]] = i
						count+=1
				listofdocuments.append(document_content)
				#an array of the dictionaries are saved
				
			print FILENAME
			#a bulk write significantly reduces the running time of the code
			collection.insert_many(listofdocuments)
			#every transaction/message is written to the db
		client.close()
		#close the connection