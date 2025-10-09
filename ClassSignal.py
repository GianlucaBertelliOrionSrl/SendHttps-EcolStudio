import sys
import string
import signal
import os
import contextlib

class SignalExit(object):
	__slots__ = 'kill'

	def __init__(self):
		self.kill = False

		#if IsWindows() == True:
		if (("win" in sys.platform) == True):
			sigmap = [signal.SIGINT, signal.SIGTERM, signal.SIGBREAK]
		else:
			sigmap = [signal.SIGINT, signal.SIGTERM]

		n = len(sigmap)

		for i in range(0,n):
			signum = sigmap[i]
			signal.signal(signum, self.exit)

	def exit(self,signum, frame):
		self.kill = True
		print ("KILL SIG RECEIVED")
		#WriteIsKilled(True)
