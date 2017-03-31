from __future__ import print_function
import pymongo,re,hashlib,json
from pymongo import MongoClient
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.No_Errors_Data
ussd='^\*701'


class Upload:
	'Object created to make uploading to Mongo Easier'
	def __init__(self, D,T,U,M):
		self.Date = D
		self.Time = T
		self.Source = U
		self.Target = M
		
	def displayObj(self):
		print(self.Date,'\n',self.Time,'\n',self.Target,'\n',self.Source)


		
		
cmb_data = collect.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]},{'_id':0,'USSD':1,'MSISDN':1,'Date':1,'Time':1})
new_collection = db.CMB_Data_NE
count = 0 
list_to_upload = []
for i in cmb_data:
	temp_num = i["USSD"].strip("*701*").strip("#")
	receiver = hashlib.md5(temp_num.encode('utf-8')).hexdigest()
	upload_object = Upload(i["Date"],i["Time"],i["MSISDN"],receiver)
	count +=1
	if count%100000 == 0:
		print(count, end='\r')
	list_to_upload.append(upload_object.__dict__)
	
new_collection.insert_many(list_to_upload)