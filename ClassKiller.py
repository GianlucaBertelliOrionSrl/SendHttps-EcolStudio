import signal
import sys

class SIGINT_handler():
	def __init__(self):
		self.SIGINT = False

	def signal_handler(self, signal, frame):
		print('You pressed Ctrl+C!')
		self.SIGINT = True

class ClassKiller(object):
	__slots__ = 'kill_now'

	def __init__(self):

		self.kill_now = False

		signal.signal(signal.SIGINT, self.exit_gracefully)
		signal.signal(signal.SIGTERM, self.exit_gracefully)
		
		#if IsWindows() == True:
		if (("win" in sys.platform) == True):
			signal.signal(signal.SIGBREAK, self.exit_gracefully)

	def exit_gracefully(self,signum,frame):
		self.kill_now = True
		print ("KILLED")
