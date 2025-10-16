import sys, os, time, atexit
from signal import SIGTERM 

import inspect
frame = inspect.currentframe()

import ModuleFunctions
from ModuleFunctions import *

#LinuxFolder = '/mnt/sda2/home/AcqApm2'
LinuxFolder = '/mnt/mmcblk0p1/home/AcqApm2'


class Daemon:
	__slots__ = ()
	"""
	A generic daemon class.
	Usage: subclass the Daemon class and override the run() method
	"""

	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
	
	def daemonize(self,abspath):
		"""do the UNIX double-fork magic, see Stevens' "Advanced 
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16"""

		base_dir = ModuleFunctions.get_base_dir()

		try: 
			pid = os.fork() 
			#s = 'PID = ' + str(pid)
			command_str = ['PID = ',str(pid)]
			command = "".join(command_str)
			WriteLog(command)

			s = "Try first fork"
			WriteLog(s)

			if pid > 0:
				sys.exit(0) 
		except IOError as e:
			s = "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror)
			WriteLog(s)
			sys.stderr.write(s)
			sys.exit(1)
	
		if (IsLinux() == True) and (base_dir == ''):
			base_dir = LinuxFolder

		s = ModuleFunctions.get_base_dir()

		#s1 = "Abs path folder = " + s
		command_str = ['Abs path folder = ',s]
		command = "".join(command_str)
		WriteLog(command)

		os.chdir(s)
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			#s = 'PID = ' + str(pid)
			command_str = ['PID = ',str(pid)]
			command = "".join(command_str)
			WriteLog(command)

			s = "Try second fork"
			WriteLog(s)

			if pid > 0:
				s = "Exit second parent"
				WriteLog(s)
				sys.exit(0)
			pass
		except IOError as e:
			s = "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror)
			WriteLog(s)
			sys.stderr.write(s)
			sys.exit(1) 
	
		# redirect standard file descriptors
		s = "Close terminals"
		WriteLog(s)

		#s  =  "Filename: " + frame.f_code.co_filename
		#WriteLog(s)
		#s = str("Linenumber: " + frame.f_lineno)
		#WriteLog(s)

		sys.stdout.flush()
		sys.stderr.flush()

		si = open(os.devnull, 'r')
		so = open(os.devnull, 'w')
		se = open(os.devnull, 'w')
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())

		atexit.register(self.delpid)
		pid = str(os.getpid())

		#s  =  "PID = " + pid
		command_str = ['PID = ',str(pid)]
		command = "".join(command_str)
		WriteLog(command)
		open(self.pidfile,'w+').write("%s\n" % pid)
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self,abspath):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = open(self.pidfile,'r')

			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)
		
		self.daemonize(ModuleFunctions.get_base_dir())
		self.run()

	def stop(self):
		# Get the pid from the pidfile
		try:
			pf = open(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.pidfile)
			return # not an error in a restart

		# Try killing the daemon process	
		try:
			command = "kill -9 " + str(pid)
			os.system(command)

			if os.path.exists(self.pidfile):
				os.remove(self.pidfile)
		except IOError as e:
			err = str(e)
			WriteLog(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print (str(err))
				sys.exit(1)

		if os.path.exists(self.pidfile):
			os.remove(self.pidfile)

	def restart(self):
		self.stop()
		self.start()
