import sys
import argparse
import string
import signal
import os

import Global

import contextlib
import datetime
from datetime import datetime

import time
from time import sleep

from pathlib import Path

import ModuleFunctions
#from ModuleFunctions import *

import ModuleTime
from ModuleTime import *

absPath = os.path.dirname(os.path.realpath(sys.argv[0]))
PERIOD_OLD_LOGS = 60*60*24*30

def ReadFile0(path):
	b = False

	try:
		if ModuleFunctions.IsPython36() == True:
			with open(path,'r',encoding='utf8') as content_file:
				content = content_file.read()
		else:
			with open(path,'r') as content_file:
				content = content_file.read()

		s = content
		lb = sys.getsizeof(s)
		ls = len(s)
		nl = NumberOfLines()
		b = True
	except Exception as e:
		print(e)
		WriteLog(str(e))
		b = False

	return b
	
def ReadFile(path):
	try:
		f = open(path, "r")
		s1 = f.readline()
		f.close()
	except Exception as e:
		print(stre)

def ReadFileToString(path):
	try:
		f = open(path, "r")
		s1 = f.readline()
		f.close()
		return s1
	except Exception as e:
		print(str(e))
		return ''

def ReadFileToString2(path):
	try:
		with open(path, 'r') as f:
			s1 = f.read().replace('\n', '*')

		f.close()

		s2 = s1.replace('\r','')
		s3 = s2.replace(" ","")
		s1 = s3.replace("*", " ")

		return s1

	except Exception as e:
		print(str(e))
		return ''

def ReadFileToArrayStrings(FileDati):
	list_of_lists = []

	try:
		#FileDati = absPath + "\\Giornaliero_Min.tmp"

		with open(FileDati) as f:
			for line in f:
				inner_list = [elt.strip() for elt in line.split(',')]
				# in alternative, if you need to use the file content as numbers
				# inner_list = [int(elt.strip()) for elt in line.split(',')]
				list_of_lists.append(inner_list)
		f.close

	except Exception as e:
		print(str(e))
		list_of_lists = []

	return list_of_lists

def WriteFileNew(filepath,my_line,mode):
	#filepath = os.path.join(Global.absPath,filename)
	if mode==0:
		with open(filepath, 'a+') as f:
			f.write(my_line)
			f.close
	else:
		with open(filepath, 'w+') as f:
			f.write(my_line)
			f.close

def AppendFile(filename,my_line):
	#filepath = os.path.join(Global.absPath,filename)
	with open(filename, 'a+') as f:
		f.write(my_line)
		f.close

def WriteFile(filename,my_line):
	#filepath = os.path.join(Global.absPath,filename)
	with open(filename, 'w+') as f:
		f.write(my_line)
		f.close

def NumberOfLines(s):
	n = s.count('\n', 0, ls)
	n2 = s.count('\r', 0, ls)
	return max(n,n2)

def NumberOfChars(s,c):
	n = s.count(c, 0, ls)
	return n

def get_path_and_extension(filename):
	index = filename.find('.')
	return filename[:index], filename[index + 1:]

def GetFileSize(filename):
	size = os.path.getsize(filename)
	return size

def RenameFile(OldName,NewName):
	try:
		os.rename(OldName, NewName)
	except:
		pass

def DeleteOldLogFiles(debug):
	if debug==True:
		print('Delete old LOG files')

	fullpathLog = os.path.join(Global.absPath,'log')
	os.chdir(fullpathLog)
	list_files = sorted(os.listdir(fullpathLog))
	n_files = 0

	for d in list_files:
		try:
			for root, dirs, files in os.walk(fullpathLog,topdown=True):
				l = len(files)
				if l<= 0:
					break

				for name in files:
					file_to_delete = os.path.join(root, name)
					s1 = GetFileModificationDate(file_to_delete)
					date_file_mod = s1[0]
					epoch = Epoch()

					if epoch < date_file_mod+PERIOD_OLD_LOGS:
						SleepMsec(10)
						continue
					try:
						os.remove(file_to_delete)
						if debug==True:
							print(file_to_delete)
						n_files = n_files+1
					except Exception as e:
						print(str(e))
						continue

					SleepMsec(10)
					if (n_files >= 50):
						break
				if (n_files >= 50):
					break
				pass
			if (n_files >= 50):
				break
		except Exception as e:
			print(str(e))
			break
	pass

def GetFileModificationDate(filename):
	f = os.path.getmtime(filename)
	t = datetime.fromtimestamp(f)
	frac, whole = math.modf(f)
	ep_int = int(whole)
	ep_flo = float(frac)
	return ep_int,ep_flo,t

def GetFileCreationDate(filename):
	t = os.path.getctime(filename)
	return datetime.fromtimestamp(t)

def GetFileModificationDate_components(filename):
	t = os.path.getmtime(filename)
	d = datetime.fromtimestamp(t)
	DD = int(d.day)
	MM = int(d.month)
	YYYY = int(d.year)
	hh = int(d.day)
	mm = int(d.minute)
	ss = int(d.second)
	return YYYY

