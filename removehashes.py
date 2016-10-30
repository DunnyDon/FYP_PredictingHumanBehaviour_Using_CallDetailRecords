import pymongo
from pymongo import MongoClient
import re
#this scaript was created to remove the USSD
#entries in the database which were incorrectly types the user
#This script is for the local database but can be modified for a remote
#MongoDb by altering the line below
client = MongoClient()
db = client.FYP_Airtel_Storage
c = db.FYP_USSD_Codes
searchforhash = re.compile('#')
db.FYP_USSD_Codes.remove({"USSD":searchforhash})
#remove any USSD entry with a #
document_cursor = c.find({"USSD":searchforhash}, {'_id':0})
docs = document_cursor[:]
for i in docs:
	print i["USSD"]
	#This is done to ensure that they are all removed
	#It searches for any left and prints them out
	#This should never print anything
#db.FYP_USSD_Codes.remove()
