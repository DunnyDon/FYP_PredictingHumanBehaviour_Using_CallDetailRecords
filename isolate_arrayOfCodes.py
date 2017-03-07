import os, hashlib
import pymongo
from pymongo import MongoClient
#import modules needed especially the pymongo modules
#which is a python integration for Mongo
root_file = "D:\Airtel-Chad-USSD-MO-CDR's-6months"
#the location of where the files were stored
USSDRequestHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","IMSI","SesID","USSD"]
USSDResponseHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","SesID","USSD","Status","Error"]
enter_to_database = ["Trans","Date","Time","CDRID","MSISDN","USSD"]
find_errors=["error","not authorized","not eligible","not qualified","don't qualify","unknown service","wrong short code","already subscribed","technical difficulties", "invalid","try again","unavailable","failed","no httpcontext","wrong input","access denied","not registered","Your not a user yet...GET OUT!","you are not part of","you are not a postpaid subscriber","not available","no message"]
us_codes=['*701','*130','*126','*202']
#define the attributes for each type of message
#and define the attributes that are wanted in the db
def fill_db(root):
	for root, dirs, files in os.walk(root):
		#ussd_regex = '*701'
		for FILENAME in files:
			#walk the directory and subdirectory and get every file
			messages2include=[]
			messages2remove=[]
			error_check=0
			listofdocuments = []
			callmeback = []
			#open a connection to mongo db 
			if not FILENAME.endswith('.gz'):
				fd = open(root+"\\"+FILENAME, 'r')
				#open the files with read only privilages
				#and loop through each line
				for line in fd:
					document_content = {}
					split_line = line.split(",")
					count = 0
					if int(split_line[2]) == 1 :
						if split_line[9].startswith('*701') or split_line[9].startswith('*130') or split_line[9].startswith('*126') or split_line[9].startswith('*202'):
							if split_line[9].startswith('*701'):
								callmeback.append(split_line[5])
							messages2include.append(split_line[5])
							
							#this is finding the transaction id which states whether or not the 
							#message is USSD request or a response
							#Different arrays have to be used for the two and hence why the if statement is there
							for i in split_line:
								if USSDRequestHeaders[count] in enter_to_database :
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
									break
							if chk==0 and  split_line[5] in messages2include:
								for i in split_line:
									#The same principle applies for USSD response messages
									if USSDResponseHeaders[count] in enter_to_database:
										if '\n' in i:
											i=i.strip('\n')
										if USSDResponseHeaders[count] == "MSISDN":
											i=hashlib.md5(i.encode()).hexdigest()
										if USSDResponseHeaders[count] == "USSD" and split_line[5] in callmeback :
											temp_num = i.strip("*701*").strip("#")
											#print i[:11], hashlib.md5(temp_num.encode()).hexdigest()
											i= hashlib.md5(temp_num.encode()).hexdigest()
									
										document_content[USSDResponseHeaders[count]] = i
									count+=1
								listofdocuments.append(document_content)
							#an array of the dictionaries are saved
						else:
							messages2remove.append(split_line[5])
							#print split_line
				#print len(listofdocuments)," ",len(messages2remove), " ", len(messages2include)		
				listofdocuments=remove_errors(listofdocuments,messages2remove)
				print len(listofdocuments)
				print FILENAME
				#a bulk write significantly reduces the running time of the code
				collection.insert_many(listofdocuments)
				#every transaction/message is written to the db
			
	
def remove_errors(db_content,err_content):
	for i in db_content:
		if i["CDRID"] in err_content:
			#print i["USSD"]
			db_content.remove(i)
			#print 'Found Error', i["CDRID"], ' ' , i["Date"], ' ', i["Time"]
		elif i["CDRID"] in err_content:
			print 'Found Error not being removed', i
		'''else:
			for j in range(0,11):
				if USSDResponseHeaders[j] in enter_to_database:
					print j,' ',USSDResponseHeaders[j],' ', i[USSDResponseHeaders[j]]'''

	return db_content
	
client = MongoClient()
db = client.FYP_Airtel_Storage
collection = db.CallMe_TopUp
fill_db(root_file)
client.close()
#close the connection