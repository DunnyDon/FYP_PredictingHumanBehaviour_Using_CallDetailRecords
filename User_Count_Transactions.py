import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
cursor = everything.find({},{"MSISDN":1})
one = 0
two = 0
three = 0
fourplus = 0
msisdn_array = []
for i in cursor:
	#save each value in arrays
	msisdn_array.append(i["MSISDN"])
total = msisdn_array.count()
print total
count = 0
for i in msisdn_array:
	number = i["MSISDN"]
	print number
	countnum = everything.find({"MSISDN":number, "Trans":"1"}).count()
	print countnum
	if  countnum == 1:
		print i,"\t","One"
		one+=1
	elif countnum == 2:
		print i,"\tTwo"
		two+=1
	elif countnum == 3:
		print i,"\tThree"
		three+=1
	elif countnum > 3:
		print i,"\tFour"
		fourplus+=1

print "1 : ", one
print "2 : ", two
print "3 : ", three
print "4 : ", fourplus
print "Total Number of Subscribers: ", one+two+three+fourplus