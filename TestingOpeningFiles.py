import os, hashlib
import pymongo
from pymongo import MongoClient
root = "D:\Airtel-Chad-USSD-MO-CDR's-6months"
USSDRequestHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","IMSI","SessID","USSD"]
USSDResponseHeaders = ["SubID","ServID","Trans","Date","Time","CDRID","MSISDN","SessID","USSD","Status","Error"]

for root, dirs, files in os.walk(root):
	for FILENAME in files:
		listofdocuments = []
		client = MongoClient()
		db = client.FYP_Airtel_Storage
		collection = db.Airtel_Data_Storage
		if not FILENAME.endswith('.gz'):
			fd = open(root+"\\"+FILENAME, 'r')
			#print(FILENAME)
			#open it with read only privilages
			for line in fd:
				count = 0
				#print line.split(",")[2]
				document_content = {}
				if int(line.split(",")[2]) == 1:
					for i in line.split(","):
						if '\n' in i:
							i=i.strip('\n')
						if USSDRequestHeaders[count] == "IMSI":
							i=hashlib.md5(i.encode()).hexdigest()
						document_content[USSDRequestHeaders[count]] = i
						#print USSDRequestHeaders[count]," ",i
						count+=1
				else:
					for i in line.split(","):
						if '\n' in i:
							i=i.strip('\n')
						#print USSDResponseHeaders[count]," ",i
						document_content[USSDResponseHeaders[count]] = i
						count+=1
					#break
				listofdocuments.append(document_content)
				#collection.insert_one(document_content)
				#print document_content
			
			print FILENAME
			collection.insert_many(listofdocuments)
			#break
		client.close()