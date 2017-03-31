import os, hashlib, sys
import pymongo
from pymongo import MongoClient
reload(sys)
sys.setdefaultencoding('utf8')
USSDRequestHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","IMSI","SesID","USSD"]
USSDResponseHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","SesID","USSD","Status","Error"]
enter_to_database = ["Date","Time","MSISDN","USSD","CDRID"]
find_errors=["error","not authorized","not eligible","not qualified","don't qualify","unknown service","wrong short code","already subscribed","technical difficulties", "invalid","try again","unavailable","failed","no httpcontext","wrong input","access denied","not registered","Your not a user yet...GET OUT!","you are not part of","you are not a postpaid subscriber","not available","no message"]
	
#import modules needed especially the pymongo modules
#which is a python integration for Mongo
#the location of where the files were stored
#define the attributes for each type of message
#and define the attributes that are wanted in the db
def fill_db(filenam):
	print "Test ",filenam
	ussd_regex = '*701'
	messages2include=[]
	messages2remove = []
	error_check=0
	listofdocuments = []
	client = MongoClient()
	db = client.FYP_Airtel_Storage
	collection = db.call_gephi_demo
	#open a connection to mongo db 
	if not filenam.endswith('.gz'):
		fd = open(filenam, 'r')
		#open the files with read only privilages
		#and loop through each line
		for line in fd:
			count = 0
			document_content = {}
			split_line = line.split(",")
			if int(split_line[2]) == 1 and split_line[9].startswith(ussd_regex):
				messages2include.append(split_line[5])
				#this is finding the transaction id which states whether or not the 
				#message is USSD request or a response
				#Different arrays have to be used for the two and hence why the if statement is there
				for i in split_line:
					if USSDRequestHeaders[count] in enter_to_database:
						#make sure the sttribute is wanted in the db
						if '\n' in i:
							i=i.strip('\n')
							#ensure that no extra characters are saved
						if USSDRequestHeaders[count] == "MSISDN":
							#for privacy and ethical reasons the numbers in the db must be hashed
							i=hashlib.md5(i.encode()).hexdigest()
							document_content['Source'] = i
						if USSDRequestHeaders[count] == "USSD":
							temp_num = i.strip("*701*").strip("#")
							#print i[:11], hashlib.md5(temp_num.encode()).hexdigest()
							i= hashlib.md5(temp_num.encode()).hexdigest()
							document_content['Target'] = i
						if USSDRequestHeaders[count] == "Date" or USSDRequestHeaders[count] == "Time" or USSDRequestHeaders[count] == "CDRID" :	
							document_content[USSDRequestHeaders[count]] = i
						#create a dictionary for each transaction
						#NOTE: one for each response AND request
					count+=1
				listofdocuments.append(document_content)
				#an array of the dictionaries are saved
					#this is used to make sure the attribute assigned in the dictionary is pointing at the right
					#value from the files
			else:
				if split_line[9]!="-1":
						chk=0
						for e in find_errors:
							if e in split_line[8].lower():
								#print split_line
								messages2remove.append(split_line[5])
								chk=1
						if chk==0 and split_line[5] in messages2include:							
							for i in split_line:
								#The same principle applies for USSD response messages
								if USSDResponseHeaders[count] in enter_to_database:
									if '\n' in i:
										i=i.strip('\n')
									if USSDResponseHeaders[count] == "MSISDN":
										i=hashlib.md5(i.encode()).hexdigest()
									if USSDResponseHeaders[count] == "USSD":
										temp_num = i[:11]
										#print i[:11], hashlib.md5(temp_num.encode()).hexdigest()
										i= hashlib.md5(temp_num.encode()).hexdigest() + i[12:]
										#print i
									#document_content[USSDResponseHeaders[count]] = i
								count+=1
							#print document_content["USSD"] ,'\n'
							#listofdocuments.append(document_content)
				else:
					messages2remove.append(split_line[5])
					#print split_line
					
					#an array of the dictionaries are saved
		print len(listofdocuments)," ",len(messages2remove)		
		listofdocuments=remove_errors(listofdocuments,messages2remove)
		print len(listofdocuments)
		print filenam
		#a bulk write significantly reduces the running time of the code
		collection.insert_many(listofdocuments)
		#every transaction/message is written to the db
	client.close()
	#close the connection
			
def remove_errors(db_content,err_content):
	for i in db_content:
		if i["CDRID"] in err_content:
			#print i["USSD"]
			db_content.remove(i)
			#print 'Found Error', i["CDRID"], ' ' , i["Date"], ' ', i["Time"]
		
	return db_content
	