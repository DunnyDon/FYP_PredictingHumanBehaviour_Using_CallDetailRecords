from lockfile import LockFile
filename = "C:\Users\Conor\Desktop\pythonwrite.txt"
f= open(filename,'a')
#print f.read()
lock = LockFile(filename)
with lock:
		print lock.path, 'is locked.'
		f.write("\n Testing18")
		
f=open(filename,'r')
print f.read()