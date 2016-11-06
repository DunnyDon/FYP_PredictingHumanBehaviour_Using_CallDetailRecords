import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
cursor = everything.find({},{"IMSI":1})
imsi_array = cursor[:]
one = 0
two = 0
three = 0
fourplus = 0
total = imsi_array.count()
print total
count = 0
for i in imsi_array:
	number = i["IMSI"]
	print number
	if number in imsi_array:
		print True
	else:
		print False
	countnum = everything.find({"IMSI":number}).count()
	print countnum
	if  countnum == 1:
		print "One"
		one+=1
	elif countnum == 2:
		print "Two"
		two+=1
	elif countnum == 3:
		print "Three"
		three+=1
	elif countnum > 3:
		print "Four"
		fourplus+=1

print "1 : ", one
print "2 : ", two
print "3 : ", three
print "4 : ", fourplus
print "Total Number of Subscribers: ", one+two+three+fourplus