import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
#open connection the db collection
cursor = everything.find({},{'_id':0,'CDRID':1,'SesID':1})
#return every Correlation ID and Session ID
cdr_array = []
session_array = []
count = 0
for i in cursor:
	#save each value in arrays
	cdr_array.append(i["CDRID"])
	session_array.append(i["SesID"])
print "Saved values in Array"
print 'Begin Search'
#Pymongo seems to not allow nested cursors and hence the reason for two loops
for j in cdr_array:
	cdrid = re.compile(j)
	cdr_cursor = everything.find({"CDRID":j},{'_id':0,'CDRID':1,'SesID':1}).limit(2)
	#search for the USSD request and response for each CDRID
	for k in cdr_cursor:
		if j!=k['CDRID'] or session_array[count]!=k["SesID"]:
			#this should never print out as the Session IDs and Correlation IDs should always be the same in the cursor and the arrays
			print 'Found Error\t',j,"\t",k["CDRID"],"\t",session_array[count],'\t',k["SesID"]
	count+=1
client.close()
#close the connection