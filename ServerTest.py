import pymongo
from pymongo import MongoClient
import re
client = MongoClient('mongodb://user:password@host:port/db')
db = client.mongodb2706
Tes = db.FYP_USSD_Codes
document_cursor = Tes.find({}, {'_id':0})
docs = document_cursor[:]

def checkduplicates(s):
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

print "There are ",countduplicates, " duplicates."
