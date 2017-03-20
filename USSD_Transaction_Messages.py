import pymongo
from pymongo import MongoClient
import re
import json
from collections import defaultdict
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.FYP_Data
ussd_codes = db.FYP_USSD_Codes
limit = 1
num = 1
session_array = []
ussd_dict = {}
us_code_array =[]
#initialise all variables and open a file to write the responses too
f = open('C:\Users\Conor\Desktop\ErrorsCodesMoreInfo_3.txt','a')
ussd_others = {}				
#create your functions before you call them
def ussd_message(sesarr, ussdiction):
	for j in sesarr:
		cdr_cursor = everything.find({"$and": [{"CDRID":j},{"Trans":"2"}]},{'_id':0,'USSD':1}).limit(1)
		code = ussdiction[j] 
		for k in cdr_cursor:
			if(len(code)==5):
				#print ussdiction[j],'\t',k["USSD"],"\t",j
				f.write(ussdiction[j]+'\t'+k["USSD"]+"\t"+j+'\n')
				#write to file if USSD code is in the format of *xxx#
			elif code.startswith('*') and code.endswith('#'): 
				#make sure it is a valid ussd code
				if code.count("*")>1:
					new_code = code.split("*")
					#some codes contained vouchers and were not in the format *xxx# 
					#this has to be adjusted for so the original number xxx can be got and saved
					split_code = new_code[1]
					if split_code in ussd_dict:
						ussd_dict[split_code] +=1
						#check to make sure the code in the dicitonary
						#if not then initialise it
					else:
						ussd_dict[split_code] = 1
						ussd_others.setdefault(split_code,[]).append(k["USSD"])
						#this is a dictionary which holds the ussd code and the response
					if ussd_dict[split_code] <=400:
						ussd_others.setdefault(split_code,[]).append(k["USSD"])
						#limit to however responses per message the user wishes
				#print ussdiction[j],'\t',k["USSD"],"\t",j				
	f.write(json.dumps(ussd_others, indent=4))
	#write to the file
	
def get_ussd_codes(lim):
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	uscodearr = []
	cursor = ussd_codes.find({},{'_id':0})
	for j in cursor:
		uscodearr.append(j)
	#get your ussd codes
	return uscodearr

def get_session_id(uca):
	cdrar = []
	count = 0
	usdiction = {}
	#get a limited amount of cdr ids relating to the ussd codes 
	for i in uca:
		count+=1
		ussd = re.compile(i)
		ussd_cursor = everything.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"},{"ignore":{'$ne':"1"}}]},{'_id':0,'CDRID':1,'USSD':1}).limit(1000).skip(1800)
		for k in ussd_cursor:
			usdiction[k['CDRID']] = k['USSD']
			cdrar.append(k['CDRID'])
			#save the ussd code and the cdr id in a dictionary
	ussd_message(cdrar,usdiction)
	
#us_code_array = get_ussd_codes(limit)
us_code_array = ["500","455","206","800","450","509","109","108","775","161","467","564","454","518","711","161","228","462","786","348","108","858"]
get_session_id(us_code_array)
f.close()
				
