'''for i in range(1,26):
	print i/4, i
	'''
import pymongo,threading,re
from pymongo import MongoClient
from datetime import datetime, date, time
import matplotlib.pyplot as plt
client = MongoClient()
db = client.FYP_Airtel_Storage
collect = db.CallMe_TopUp

def convert_DateTime(i):
	date_split = i["Date"].split('-')
	d = date(int(date_split[0]),int(date_split[1]),int(date_split[2]))
	time_split = i["Time"].split(':')
	t = time(int(time_split[0]),int(time_split[1]),int(time_split[2]))
	dt=datetime.combine(d, t)
	# 0 for weekday is Monday
	#print dt, dt.weekday()
	return dt
	
def count_perMonth():
	print "Starting Now..........."
	month_count_dict={}
	for k in range(2,9):
		month_count_dict[k] = 0
	ussd_regex = '^\*701'
	ussd = re.compile(ussd_regex)
	for j in range(2,9):
		d = '-0'+str(j)+'-'
		print d
		date_reg = re.compile(d)
		c = collect.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"},{"Date":{"$regex":date_reg}}]},{'USSD':1,'Date':1,'_id':0}, no_cursor_timeout=True).count()
		print c
		month_count_dict[j] +=c		
	#del week_count_dict[0]
	return month_count_dict
	
	
def get_average(data_vals):
	sum=0.0
	for i in data_vals:
		sum+=i
	print sum
	average = float(sum)/float(len(data_vals))
	return average
'''d = date(2005, 7, 14)
t = time(12, 30)
dt=datetime.combine(d, t)
print dt
c = date(2005, 7, 21)
diff = c-d
print diff'''



data_per_Month = count_perMonth()
print len(data_per_Month)
avg = get_average(data_per_Month)
print 'Average is ',avg
for i in data_per_Month:
	print i,data_per_Month[i]
