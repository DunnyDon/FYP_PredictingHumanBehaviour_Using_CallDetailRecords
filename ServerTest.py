import pymongo
from pymongo import MongoClient
import re
client = MongoClient('mongodb://user:password@host:port/db')
# this is used for connecting to a remote MongoDb
db = client.mongodb2706
Tes = db.FYP_USSD_Codes
document_cursor = Tes.find({}, {'_id':0})
docs = document_cursor[:]
#pass the findings into an array so they can be looped through
def checkduplicates(s):
	#search for the duplicates with # and their corresponding without
	#this can be done by stripping # from the number and using regex
	#to search for the number in the database
	print "Searching for ", s.strip('#')
	searchstring = re.compile(s.strip("#"))
	test_cursor = Tes.find({"USSD":searchstring},{'_id':0})
	d = test_cursor[:]
	for j in d:
		print j

countduplicates = 0
for i in docs:
	if "#" in i["USSD"]:
		checkduplicates(i["USSD"])
		countduplicates+=1
		#count the number of duplicates

print "There are ",countduplicates, " duplicates."
