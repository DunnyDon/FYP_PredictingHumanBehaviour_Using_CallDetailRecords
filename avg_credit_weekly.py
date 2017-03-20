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

def count_perWeek():
	print "Starting Now..........."
	week_count_dict={}
	changed = False
	week_count=0
	week_stored=0
	ussd_regex = '^\*130'
	ussd = re.compile(ussd_regex)
	cursor = collect.find({"$and": [{"USSD":{"$regex":ussd}},{"Trans":"1"}]},{'USSD':1,'Date':1,'Time':1,'_id':0}, no_cursor_timeout=True)

	for i in cursor:
		dattim = convert_DateTime(i)
		wk = dattim.isocalendar()[1]
		if week_stored!= wk and wk>week_stored:
			print 'Week ',week_stored,week_count
			if changed == False:
				week_count_dict[week_stored]=week_count
			elif changed ==True:
				week_count_dict[week_stored] = week_count + week_count_dict[week_stored]
			week_stored=wk
			week_count=0		
		elif week_stored!= wk and wk<week_stored:
			changed = True
		else:
			week_count+=1
		
		
	print dattim, dattim.weekday(), wk
	#del week_count_dict[0]
	return week_count_dict
	
	
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



data_per_week = count_perWeek()
print len(data_per_week)
avg = get_average(data_per_week)
print 'Average is ',avg
for i in data_per_week:
	print i,data_per_week[i]
plt.plot(data_per_week,'r')
plt.axhline(y=avg, color='b')
plt.ylabel('Number of Credit Top Ups per week')
plt.xlabel('Week')
plt.title('Weekly Count of Credit Top Ups')
plt.show()
