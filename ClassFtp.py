import ftplib
from ftplib import FTP

import sys
import argparse
import string
import signal
import os,glob
import contextlib

import ModuleFunctions
from ModuleFunctions import *

import ModuleTime
from ModuleTime import *

import threading
from threading import Thread

import ModuleJSON
from ModuleJSON import *

class ClassFtp(threading.Thread):
	__slots__ = ()

	"""description of class"""
	t_conn = 0
	connected = False
	UploadCompleted = False
	DownloadCompleted = False
	ftp = FTP
	absPath = ""
	active = False
	host = ""
	username = ""
	password = ""
	folder = ""
	timeout = 1.0
	freq_send = 1
	delete_old = 1
	days_period_old = 30
	debug = 0

	#def __init__(self, *args, **kwargs): 
	#	super(ClassFtp, self).__init__(*args, **kwargs) 
	#	self._stop = threading.Event() 
	def __init__(self):
		Thread.__init__(self)
		self.continua = 1
		self._stop = threading.Event()
		self.FolderFtp = ''
		self.FolderToSend = ''
		self.FolderSent = ''

	# function using _stop function 
	def stop(self): 
		self._stop.set() 

	def stopped(self): 
		return self._stop.isSet() 

	def GetConfigFtp(self):
		b = False

		FileConfigVarie = os.path.join(ModuleFunctions.absPath,"cfg","Ftp.json")
		ConfigVarieJSON = FileToJSON(FileConfigVarie)

		try:
			self.host = ConfigVarieJSON['host']
		except:
			self.host = ""

		try:
			self.username = ConfigVarieJSON['username']
		except:
			self.username = ""

		try:
			self.password = ConfigVarieJSON['password']
		except:
			self.password = ""

		try:
			self.folder = ConfigVarieJSON['folder']
		except:
			self.folder = ""

		try:
			self.timeout = ConfigVarieJSON['timeout']
			b = True
		except:
			self.timeout = 1.0

		try:
			self.freq_send = ConfigVarieJSON['freq_send']
			b = True
		except:
			self.freq_send = 1

		try:
			self.delete_old = ConfigVarieJSON['delete_old']
			b = True
		except:
			self.delete_old = 1

		try:
			self.days_period_old = ConfigVarieJSON['days_period_old']
			b = True
		except:
			self.days_period_old = 30

		try:
			self.debug = ConfigVarieJSON['debug']
			b = True
		except:
			self.debug = 0

		return b

	def CreateSentFolder(self,type):
		date_file_now = ModuleTime.PresentStrDateFile()

		if (type != 'FTP') and (type != 'CSV'):
			type = 'FTP'

		folderSent = os.path.join(self.FolderFtp,"Sent",date_file_now)
		ModuleFunctions.MakeDirFullPath(folderSent,self.debug)

		return folderSent

	def DeleteOldFilesFolders(self,debug):
		days_actual = ModuleTime.PresentStrDateFile()
		year = ModuleTime.Year()
		month = ModuleTime.Month()
		day = ModuleTime.Day()
		date_now = year*10000 + month*100 + day
		days_period_old = self.days_period_old
		n_files=0

		if debug==True:
			print('Delete old FTP files')

		folderSent = self.FolderSent

		os.chdir(folderSent)
		list_dir = sorted(os.listdir(folderSent))
		
		for d in list_dir:
			try:
				name_folder = os.path.join(folderSent,str(d))
				date_folder = int(d)

				if (date_folder < date_now-days_period_old):
					if debug==True:
						string_to_print = 'Date folder: ' + str(date_folder)
						print(string_to_print)
						string_to_print = 'Date now: ' + str(date_now)
						print(string_to_print)

					os.chdir(name_folder)
					for root, dirs, files in os.walk(name_folder,topdown=True):
						l = len(files)
						if l<= 0:
							break

						for name in files:
							file_to_delete = os.path.join(root, name)

							try:
								os.remove(file_to_delete)

								if debug==True:
									print(file_to_delete)

								n_files = n_files+1
							except:
								continue

							if n_files%8==0:
								#ModuleTime.SleepMsec(5)
								ModuleTime.SleepMsec(200)

							if (n_files >= 50):
								break

						if (n_files >= 50):
							break

					l=len(os.listdir(name_folder))
					if l == 0:
						try:
							os.chdir(folderSent)
							os.rmdir(name_folder)

							if debug==True:
								print(name_folder)
						except:
							pass
					pass

				if (n_files >= 50):
					break
			except:
				break

	def run(self,debug): 
		self.absPath = ModuleFunctions.absPath
		b0 = b1 = b2 = b3 = False
		local_folder = ""
		b0 = self.GetConfigFtp()

		ModuleFunctions.MakeDirFullPath(self.FolderToSend,debug)
		ModuleTime.SleepMsec(100)

		ModuleFunctions.MakeDirFullPath(self.FolderSent,debug)
		ModuleTime.SleepMsec(100)

		if self.delete_old == True:
			self.DeleteOldFilesFolders(debug)

		while True:
			if self.stopped(): 
				self.Disconnect()
				self.connected = False
				return

			t = ModuleTime.Epoch()

			#ModuleTime.SleepMsec(100)
			ModuleTime.SleepMsec(200)

			if (t < self.t_conn+60):
				continue

			min = ModuleTime.Minutes()
			date_file_now = ModuleTime.PresentStrDateFile()
			sec = ModuleTime.Seconds()

			if (self.delete_old == True) and (min%10 == 0):
				self.DeleteOldFilesFolders(debug)

			self.t_conn = t

			if b0==True:
				try:
					b1 = self.Connect(self.host,self.username,self.password)
					self.connected = True
				except:
					self.connected = False
					b1 = False

				if self.connected == False:
					if debug == True:
						print ("No Ftp connection")
					continue

				if b1 == True:
					try:
						resp = self.ftp.sendcmd('MLST '+self.folder)
						if 'type=dir;' in resp:
							b2 = True
						else:
							b2 = False
					except:
						b2 = False

				if b2 == False:
					try:
						self.MakeFolder(self.folder)
						#ModuleTime.SleepMsec(50.0)
						ModuleTime.SleepMsec(200.0)
						b3 = True
					except:
						b3 = False

				try:
					b4 = self.ChangeFolder(self.folder)
					local_folder = self.FolderToSend
					folderSent = self.CreateSentFolder('FTP') #in base a data e ora

					while True:
						if self.stopped(): 
							self.Disconnect()
							self.connected = False
							return

						ModuleTime.SleepMsec(100.0)

						date_file_now = ModuleTime.PresentStrDateFile()
						sec = ModuleTime.Seconds()
						min = ModuleTime.Minutes()

						if(min == 0) and (sec < 10):
							folderSent = self.CreateSentFolder('FTP')
			
						if (min%self.freq_send != 0):
							continue

						if (sec < 10) or (sec > 45):
							continue

						self.UploadCompleted = False

						os.chdir(local_folder)
						i = 0
						for name in glob.glob("*.csv"):
							if self.stopped(): 
								self.Disconnect()
								return

							if debug==True:
								print(name)

							fullpath = os.path.join(local_folder,name)

							if debug==True:
								print ("Send file " + name)

							self.UploadFile(local_folder,name)
							
							if self.UploadCompleted == True:
								fullpathSent = os.path.join(folderSent,name)

								if ModuleFunctions.IsWindows() == True:
									copy_cmd = 'copy'
								else:
									copy_cmd = 'cp'

								command_str = [copy_cmd,' ',fullpath,' ',fullpathSent]
								command = "".join(command_str)

								if debug == True:
									print(command)

								os.system(command)
								os.remove(fullpath)
							i=i+1
							if i>=8: 
								break
						pass
					pass
				except Exception as e:
					print(str(e))
					continue

				if self.connected == True:
					self.Disconnect()

	def Connect(self,host,username,password):
		self.ftp = FTP(host)

		b = ""
		b = self.ftp.login(user=username, passwd = password)

		if ('logged in' in b) or ('OK' in b):
			self.connected =  True
			return True
		else:
			self.connected = False
			return False

	def ChangeFolder(self,name):
		#ftp.cwd('/whyfix/')
		b = self.ftp.cwd('/'+name+'/')

	def MakeFolder(self,name):
		self.ftp.mkd('/'+name+'/')

	def DownloadFile(self,name):
		localfile = open(name, 'wb')
		b = self.ftp.retrbinary('RETR ' + name, localfile.write, 1024)

		#ftp.quit()
		localfile.close()

	def UploadFile(self,folder,name):
		fileName = os.path.join(folder,name)

		if os.path.isfile(fileName):
			fh = open(fileName, 'rb')
			b = self.ftp.storbinary('STOR ' + name, fh)
			fh.close()

			#if 'Transfer complete' in b:
			if ('complete' in b ) | ('completato' in b ) | ('success' in b ):
				self.UploadCompleted = True
			else:
				self.UploadCompleted = False
		else:
			pass
			print ("Source File does not exist")

	def Disconnect(self):
		self.ftp.quit
		#ClassFtp.ftp.quit

		self.connected =  False
