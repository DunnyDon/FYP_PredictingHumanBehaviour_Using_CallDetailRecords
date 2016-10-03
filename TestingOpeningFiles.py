import os
root = "D:\Airtel-Chad-USSD-MO-CDR's-6months"
USSDRequestHeaders = ["SubscriberID","ServiceID","Transaction","Date","Time","CDRCorrelationID","MSISDN","IMSI","SessionID","USSDContent"]
USSDResponseHeaders = ["SubscriberID","ServiceID","Transaction","Date","Time","CDRCorrelationID","MSISDN","SessionID","USSDContent","Status","ErrorCode"]
for root, dirs, files in os.walk(root):
	for FILENAME in files:
		if not FILENAME.endswith('.gz'):
			fd = open(root+"\\"+FILENAME, 'r')
			#print(FILENAME)
			#open it with read only privilages
			for line in fd:
				count = 0
				print line.split(",")[2]
				if int(line.split(",")[2]) == 1:
					for i in line.split(","):
						print USSDRequestHeaders[count]," ",i
						count+=1
				else:
					for i in line.split(","):
						print USSDResponseHeaders[count]," ",i
						count+=1
					break
			break