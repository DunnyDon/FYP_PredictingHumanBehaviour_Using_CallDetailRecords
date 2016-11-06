import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
cursor = everything.find({},{'_id':0,'CDRID':1,'SesID':1}).limit(2000).skip(3000000)
#documents = cursor[:]
cdr_array = []
session_array = []
count = 0
for i in cursor:
	cdr_array.append(i["CDRID"])
	session_array.append(i["SesID"])
print "Saved values in Array"
print 'Begin Search'
for j in cdr_array:
	cdrid = re.compile(j)
	cdr_cursor = everything.find({"CDRID":j},{'_id':0,'CDRID':1,'SesID':1}).limit(2)
	for k in cdr_cursor:
		if j!=k['CDRID'] or session_array[count]!=k["SesID"]:
			print 'Found Error\t',j,"\t",k["CDRID"],"\t",session_array[count],'\t',k["SesID"]
	count+=1
client.close()