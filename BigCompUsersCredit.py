#gets all users with more than one top up and plots them


import pymongo
from pymongo import MongoClient
import re,threading
import matplotlib.pyplot as plt
client = MongoClient()
#this will work on the local database
db = client.FYP_Airtel_Storage
collect = db.Weighted_Users
credit = []
def get_users():
	#get a limited abount of ussd codes and save them in an array
	#you can limit it ro try and isolate certain codes and reduce
	#computation time
	users = []
	cursor = collect.find({"CredCount":{"$ne":0}},{'_id':0,'CredCount':1})
	for j in cursor:
		users.append(j["CredCount"])
	#get your ussd codes
	return users

def get_average(data_vals):
	sum=0.0
	for i in data_vals:
		sum+=i
	try:
		average = float(sum)/float(len(data_vals))
		weekly_average = (float(sum)/(float(len(data_vals))))/26.0		
	except ZeroDivisionError:
		average = float(sum)/float(len(data_vals)+1)
		weekly_average = (float(sum)/(float(len(data_vals))+1))/26.0
	print 'Weekly Average ',weekly_average
	return average

def print_plot(user_data,avg):
	user_data.sort()
	x_axis = []
	for i in range(1,len(user_data)+1):
		x_axis.append(i)
	plt.scatter(x_axis,user_data)
	plt.axhline(y=avg, color='r')
	plt.ylabel('Number of Credit Top Ups')
	plt.xlabel('Users')
	#plt.xscale('log',basex=2)
	#plt.yscale('log',basey=2)
	plt.title('Count of Total Credit Top Ups')
	plt.axis([0,50000, -250,1300])
	plt.show()
def print_histogram(user_data):
	plt.hist(user_data)
	plt.title("Top Up Histogram")
	#plt.xlabel("")
	#plt.ylabel("Frequency")
	plt.show()
print 'Get Top up info......'
credit = get_users()
print len(credit)
print 'Get Average amount of Top ups........'
average_topup = get_average(credit)
print 'Average is ',average_topup
print_plot(credit,average_topup)
#print_histogram(credit)