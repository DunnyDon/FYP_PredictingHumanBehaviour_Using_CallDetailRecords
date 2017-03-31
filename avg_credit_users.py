#gets top up of each user and plots
import statistics
import pymongo
from pymongo import MongoClient
import re,threading
import matplotlib.pyplot as plt
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.Weighted_Users
topUp_db = db.CallMe_TopUp
topUpCount = []
	
def get_users():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	users = []
	cursor = collect.find({},{'_id':0,'MSISDN':1})
	for j in cursor:
		users.append(j["MSISDN"])
	#get your ussd codes
	return users

def start_process():
	count = 0
	index=0
	threads=[]
	num_limit = 20
	users_arr = get_users()
	print 'Starting.........'
	for i in users_arr:
		t= threading.Thread(target = get_TopUp_Num, args=(i,))
		threads.append(t)
	print 'Finished Queuing Threads'
	for thre in threads:
		
		index = index+1
		thre.start()
		if(index%num_limit==0):
			for x in threads[count:index]:
				x.join()
				#print threading.activeCount()
			print 'Joining Threads',index
			count = index
			
def get_TopUp_Num(i):
	ussd_regex = '^\*130'
	ussd = re.compile(ussd_regex)
	c = topUp_db.find({"$and": [{"MSISDN":i},{"USSD":{"$regex":ussd}},{"Trans":"1"}]}).count()
	print i,c
	collect.update({"MSISDN":i},{"$set":{"CredCount":c}})
	topUpCount.append(c)

def get_average(data_vals):
	sum=0.0
	for i in data_vals:
		sum+=i
	try:
		average = float(sum)/float(len(data_vals))
	except ZeroDivisionError:
		average = float(sum)/float(len(data_vals)+1)
	return average

def print_plot(user_data,avg):
	plt.plot(user_data,'r')
	plt.axhline(y=avg, color='b')
	plt.ylabel('Number of Credit Top Ups per week')
	plt.xlabel('Week')
	plt.title('Weekly Count of Credit Top Ups')
	plt.show()

start_process()
avg = get_average(topUpCount)
print statistics.stdev(topUpCount)
#print_plot(topUpCount,avg)
