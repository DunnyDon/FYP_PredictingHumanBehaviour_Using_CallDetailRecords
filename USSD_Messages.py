import pymongo,threading
from lockfile import LockFile
from pymongo import MongoClient
import re
import json
from collections import defaultdict
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.No_Errors_Data
ussd_codes = db.FYP_USSD_Codes
session_array = []
ussd_dict = {}
us_code_array =[]
#initialise all variables and open a file to write the responses too
f = open('C:\Users\Conor\Desktop\CodesNoError51.txt','a')
fle = 'C:\Users\Conor\Desktop\CodesNoErrors51.txt'
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

def code_response(ussd,k):
	try:
		#searches on a one by one basis, hence the k in the .skip() method
		ussd_cursor = everything.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]},{'_id':0,'CDRID':1,'USSD':1,'Time':1,'Date':1}).skip(k+20).limit(1).max_time_ms(120000)
		for g in ussd_cursor:
			print g["Time"], " ",g["Date"],g["USSD"]
			#you must loop through the cursor returned if even only one result is present
			cdr_to_search_for = re.compile(g["CDRID"])
			#search for the CDRID in the response to see if it is an error response
			cdr_id_cursor = everything.find({"$and": [{"CDRID":{"$regex":cdr_to_search_for}},{"Trans":"2"}]},{'_id':0,'USSD':1}).limit(1).max_time_ms(120000)
			for cdr_index in cdr_id_cursor:
				code = g["USSD"]
				#print g["Time"], " ",g["Date"]," ",i," ",num_of_Non_errors
				#The print statement is used to help debug and give progress feedback to the user
				lock = LockFile(fle)
				with lock:
						f.write(code+'\t'+cdr_index["USSD"]+'\n')
						f.flush()
						print g["Time"], " ",g["Date"]," ",code," ",k
						
				
	except:
		print "Failed"
	
def get_session_id(uca):
	cdrar = []
	usdiction = {}
	num_of_Non_errors=0
	count = 0
	index=0
	threads=[]
	num_limit = 675
	#loop through the USSD codes
	for i in uca:
		k=0
		ussd_regex = '^\*'+str(i)
		#ussd_regex = '^\*'+str(i["USSD"])
		#search for USSD codes which begin with *USSD_code_ eg *125
		ussd = re.compile(ussd_regex)
		#print i["USSD"]
		print i
		#f.write(i["USSD"]+"\n")
		f.write(i+"\n")
		f.flush()
		#reset variable for each USSD code so 25 of each one can be written to a file
		while k<10:
			t= threading.Thread(target = code_response, args=(ussd,k,))
			threads.append(t)
			for thre in threads:
				thre.start()
			for x in threads:
				x.join()
				#print threading.activeCount()                                
			threads=[]
			k+=1
			#k is used to ensure that the same eg *125# with CDRID of 1nzjhe4g is used everytime
		f.write('\n\n')
		
		
		
#us_code_array = get_ussd_codes()
us_code_array = ["500","156","365","170","554","136","909","026","440","455","100","761","157","111","551","606","150","234","555","706","206","444","888","180","420","558","406","545","144","183","109","152","808","147","759","143","560","148","158","541","233","108","119","153","587","717","333","574","577","251","522","467","709","564","453","547","712","353","623","462","515","611","322","581","561","417","758","548","415","762","765","766","418","373","763","451","549","419","413","757","590","756","374","468","764","491","492","622","922","261","624","895","576","892","562","559","844","987","488","313","571","389","422","197","720","447","446","535","771","775","509","161","518","786","450","800","524","454","207","228","348","592","711","629","628","750","976","726"]
get_session_id(us_code_array)
f.close()
client.close()				
