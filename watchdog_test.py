#!/usr/bin/python 
import time,os
import fill_database_no_errors_user_input
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import isolate_one_code_demo
class MyHandler(FileSystemEventHandler):
	def process(self, event):
		"""
		event.event_type 
			'modified' | 'created' | 'moved' | 'deleted'
		event.is_directory
			True | False
		event.src_path
			path/to/observed/file
		"""
		# the file will be processed there
	def create_process(self, event):
		folder='\\'.join(event.src_path.split('\\')[0:-1])
		file = '\\'.join(event.src_path.split('\\')[-1:])
		print("File "+folder+"\\"+file)
		print("Test File "+event.src_path) 
		fill_database_no_errors_user_input.fill_db(folder+"\\"+file)
		isolate_one_code_demo.fill_db(folder+"\\"+file)
		os.remove("C:/Users/Conor/Documents/FYP/FYP_PredictingHumanBehaviour_Using_CallDetailRecords-master/gephi_data.csv")
		os.system('mongoexport -d FYP_Airtel_Storage -c call_gephi_demo --type=csv --fields "Source","Target","Time","Date" -o gephi_data.csv')
	
		
	def on_modified(self, event):
		print("File modified")
		#self.create_process(event)
	def on_created(self, event):
		self.create_process(event)
	def on_deleted(self, event):
		print("File deleted")
	def on_moved(self, event):
		print("File moved")

if __name__ == "__main__":
	starting_dir = raw_input("Please Enter Directory to Monitor:")
	event_handler = MyHandler()
	observer = Observer()
	observer.schedule(event_handler, path=starting_dir, recursive=True)
	observer.start()

	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()