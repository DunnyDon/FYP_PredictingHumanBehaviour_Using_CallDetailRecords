import os, hashlib
import pymongo
from pymongo import MongoClient
client = MongoClient()
root = "D:\Airtel-Chad-USSD-MO-CDR's-6months"
USSDRequestHeaders = ["SubscriberID","ServiceID","Transaction","Date","Time","CDRCorrelationID","MSISDN","IMSI","SessionID","USSDContent"]
USSDResponseHeaders = ["SubscriberID","ServiceID","Transaction","Date","Time","CDRCorrelationID","MSISDN","SessionID","USSDContent","Status","ErrorCode"]
db = client.FYP_Data_Storage
collection = db.Airtel_Data
for root, dirs, files in os.walk(root):
	for FILENAME in files:
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
						if USSDRequestHeaders[count] == "IMSI":
							i=hashlib.md5(i.encode()).hexdigest()
						document_content[USSDRequestHeaders[count]] = i
						#print USSDRequestHeaders[count]," ",i
						count+=1
				else:
					for i in line.split(","):
						#print USSDResponseHeaders[count]," ",i
						document_content[USSDResponseHeaders[count]] = i
						count+=1
					#break
				collection.insert_one(document_content)
				#print document_content
			#break