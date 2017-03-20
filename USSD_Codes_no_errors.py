import pymongo,threading
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
f = open('C:\Users\Conor\Desktop\USSDResponses_NoErrors.txt','a')
ussd_others = {}
keep_count=0
#create your functions before you call them

def get_ussd_codes():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	uscodearr = []
	cursor = ussd_codes.find({},{'_id':0})
	for j in cursor:
		uscodearr.append(j)
		print j
	#get your ussd codes
	return uscodearr

def code_response(ussd):
	#searches on a one by one basis, hence the k in the .skip() method
	ussd_cursor = everything.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]},{'_id':0,'CDRID':1,'USSD':1,'Time':1,'Date':1}).limit(10)
	for g in ussd_cursor:
		#you must loop through the cursor returned if even only one result is present
		cdr_to_search_for = re.compile(g["CDRID"])
		#search for the CDRID in the response to see if it is an error response
		cdr_id_cursor = everything.find({"$and": [{"CDRID":{"$regex":cdr_to_search_for}},{"Trans":"2"}]},{'_id':0,'Error':1,'USSD':1}).limit(1)
		for cdr_index in cdr_id_cursor:
			code = g["USSD"]
			print g["Time"], " ",g["Date"]," ",code
			#print g["Time"], " ",g["Date"]," ",i," ",num_of_Non_errors
			#The print statement is used to help debug and give progress feedback to the user
			f.write(code+'\t'+cdr_index["USSD"]+"\t"+cdr_index["USSD"]+'\n')
			#write data to file 
				
def get_session_id(uca):
	cdrar = []
	usdiction = {}
	num_of_Non_errors=0
	count = 0
	index=0
	threads=[]
	num_limit = 10
	#loop through the USSD codes
	for i in uca:
		k=0
		#ussd_regex = '^\*'+str(i)
		ussd_regex = '^\*'+str(i["USSD"])
		#search for USSD codes which begin with *USSD_code_ eg *125
		ussd = re.compile(ussd_regex)
		#reset variable for each USSD code so 25 of each one can be written to a file
		t= threading.Thread(target = code_response, args=(ussd,))
		threads.append(t)
		index = index+1
		if(index%num_limit==0):
			for thre in threads:
				thre.start()
				print 'bob'
			for x in threads[count:index]:
				x.join()
				print keep_count
				#print threading.activeCount()                                
			count = index
			threads=[]
			#k is used to ensure that the same eg *125# with CDRID of 1nzjhe4g is used everytime
		f.write('\n\n')
		
		
		
us_code_array = get_ussd_codes()
#us_code_array = ["548"]
get_session_id(us_code_array)
f.close()
client.close()				
