import time
import logging
import sys
import argparse
import string
import signal
import os
import contextlib
import datetime
from datetime import datetime
from time import sleep
import subprocess

try:
	import psutil
	psutilExist = True

except ImportError:
	psutilExist = False
	pass

def checkIfProcessRunning(processName):
	'''
	Check if there is any running process that contains the given name processName.
	'''
	#Iterate over the all the running process
	if psutilExist==True:
		for proc in psutil.process_iter():
			try:
				# Check if process name contains the given name string.
				if processName.lower() in proc.name().lower():
					p = proc.name()
					return True
			except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
				pass
	else:
		return False

	return False;

def findProcessIdByName(processName):
	'''
	Get a list of all the PIDs of a all the running process whose name contains
	the given string processName
	'''
	listOfProcessObjects = []

	if psutilExist==True:
		#Iterate over the all the running process
		for proc in psutil.process_iter():
			try:
				pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
				# Check if process name contains the given name string.
				if processName.lower() in pinfo['name'].lower() :
					listOfProcessObjects.append(pinfo)
			except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
				pass
	else:
		return listOfProcessObjects;

	return listOfProcessObjects;

def GetProcessListByName(processName):
	if psutilExist==True:
		procObjList = [procObj for procObj in psutil.process_iter() if 'chrome' in procObj.name().lower() ]
		return procObjList
	else:
		return null

def kill_by_ID(processID):
	os.system("taskkill /F /T /PID %i"%processID)
	return True

def kill_by_process_name(processName):
	os.system("taskkill /f /im " + processName + ".exe")
	b = True
	return b
	
def prompt_sudo():
	b = False
	if os.geteuid() != 0:
		msg = "User not root"
		b = False
	else:
		msg = "User not root"
		b = False
		
	print (msg)
		
	return b