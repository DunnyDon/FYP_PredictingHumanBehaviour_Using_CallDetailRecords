import pymongo
from pymongo import MongoClient
import re
client = MongoClient()
db = client.FYP_Airtel_Storage
c = db.FYP_USSD_Codes
searchforhash = re.compile('#')
db.FYP_USSD_Codes.remove({"USSD":searchforhash})
document_cursor = c.find({"USSD":searchforhash}, {'_id':0})
docs = document_cursor[:]
for i in docs:
	print i["USSD"]
#db.FYP_USSD_Codes.remove()
