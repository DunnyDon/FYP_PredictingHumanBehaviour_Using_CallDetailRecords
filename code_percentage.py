import pymongo,threading,re
from lockfile import LockFile
from pymongo import MongoClient
client = MongoClient()
db = client.FYP_Airtel_Storage
everything = db.No_Errors_Data
ussd_codes = db.FYP_USSD_Codes
fle = 'C:\Users\Conor\Desktop\Code_Percentage.txt'
fl = open('C:\Users\Conor\Desktop\Code_Percentage.txt','a')
def get_ussd_codes():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	uscodearr = []
	cursor = ussd_codes.find({},{'_id':0})
	for j in cursor:
		uscodearr.append(j)
	#get your ussd codes
	return uscodearr

def get_percent(usd_cde):
	#ussd_regex = '/^\*'+str(usd_cde["USSD"])+'/'
	ussd_regex='^\*'+str(usd_cde["USSD"])
	#print ussd_regex
	#search for USSD codes which begin with *USSD_code_ eg *125
	ussd = re.compile(ussd_regex)
	print "Searching for ", usd_cde["USSD"]
	pcent = everything.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]}).count()
	#pcent = everything.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]}).count()
	lock = LockFile(fle)
	with lock:
			#for j in pcent:
			fl.write(usd_cde["USSD"]+"\t"+str(pcent)+"\t"+str(total)+"\n")
			fl.flush()
			print usd_cde["USSD"],"\t",pcent
def start_process():
	count = 0
	index=0
	threads=[]
	num_limit = 18
	usdcodes = get_ussd_codes()
	for i in usdcodes:
		t= threading.Thread(target = get_percent, args=(i,))
		threads.append(t)
	for thre in threads:
		index = index+1
		thre.start()
		if(index%num_limit==0):
			for x in threads[count:index]:
				x.join()
				#print threading.activeCount()                                
			count = index
			print index		

#total = everything.find({"Trans":"1"}).count()
total = 139398682
print "Total :",total			
start_process()
#fl.close()