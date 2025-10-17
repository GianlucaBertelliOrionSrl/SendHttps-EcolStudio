import sys
import os
import platform

import shutil
import tempfile

import datetime
from datetime import datetime
import inspect

#import ModuleContentFile


from ModuleUtils import get_base_dir


#abspath = (os.path.dirname(os.path.abspath(__file__))
#           if '__file__' in globals()
#           else os.path.dirname(os.path.realpath(sys.argv[0])))

# def get_base_dir():
#     if getattr(sys, 'frozen', False):
#         return os.path.dirname(sys.executable)
#     elif '__file__' in globals():
#         return os.path.dirname(os.path.abspath(__file__))
#     else:
#         return os.path.dirname(os.path.realpath(sys.argv[0]))

def create_temp_copy(file_path):
    # Crea una directory temporanea
    temp_dir = tempfile.mkdtemp()

    # Estrai il nome del file dal percorso originale
    file_name = os.path.basename(file_path)

    # Costruisci il percorso per la copia temporanea
    temp_file_path = os.path.join(temp_dir, file_name)

    # Copia il file nella directory temporanea
    shutil.copy(file_path, temp_file_path)

    return temp_file_path

def OperativeSystem():
	s = str(platform.system())
	return s

def IsLinux():
	s = OperativeSystem()
	if (("Linux" in s) == True):
		return True
	else:
		return False

def IsWindows():
	if (("win" in sys.platform) == True):
		return True
	else:
		return False

def IsPython36():
	if sys.version_info>=(3,6,0):
		return True
	else:
		return False

def IsPython34():
	if sys.version_info>=(3,4,0) and sys.version_info<(3,5,0):
		return True
	else:
		return False

def IsPython27():
	if (sys.version_info>=(2,7,0)) and (sys.version_info<(2,8,0)):
		return True
	else:
		return False

def IsRoot():
	if IsWindows() == True:
		return False
		
	if os.geteuid() != 0:
		return False
	else:
		return True


def WriteLog(s):
	base_dir = get_base_dir()

	fileLog = os.path.join(base_dir,"log","log.txt")
	now = datetime.now()
	time_now = now.strftime("%Y-%m-%d %H:%M:%S")

	l = [time_now," ",s,'\n']
	my_line = "".join(l)
		
	with open(fileLog, 'a+') as f:
		f.write(my_line)
		f.close

	d = ModuleContentFile.GetFileSize(fileLog)
	if d >= 200000:
		print("Rename log file")
		s = ModuleContentFile.PresentStrDateFile()
		l = ['log_',s,'.txt']
		my_line = "".join(l)
		fileLogNew = os.path.join(base_dir,"log",my_line)
		ModuleContentFile.RenameFile(fileLog,fileLogNew)
	pass

def WriteLog2(folder,file,s):
	try:
		base_dir = get_base_dir()

		fileLog = os.path.join(base_dir,folder,file)
		now = datetime.now()
		time_now = now.strftime("%Y-%m-%d %H:%M:%S")

		l = [time_now,' ',s,'\n']
		my_line = "".join(l)
		with open(fileLog, 'a+') as f:
			f.write(my_line)
			f.close

	except Exception as e:
		print("Generic error")

def __LINE__():
	return inspect.currentframe().f_lineno

def __FILE__():
	return inspect.currentframe().f_code.co_filename

def strstr(str,str_to_find):
	pos = str.find(str_to_find, 0) # The offset is optional
	if pos < 0: # not found
		str2 = None
	else:
		str2 = str[pos:]
	return str2

def indexstr(str,str_to_find):
	pos = str.find(str_to_find, 0) # The offset is optional
	return int(pos)

def substring(str,start,end):
	s = str[start:end]
	return s

def CheckFileExists(filename):
	try:
		my_file = open(filename)
		my_file.close
		b = True
	except IOError as e:
		#print(str(e))
		b = False
	except Exception as e:
		#print(str(e))
		b = False
	return b

def MakeDir(namedir,debug):
	base_dir = get_base_dir()
	dirName = os.path.join(base_dir,namedir)

	if debug == True:
		print("namedir:"+namedir)
		print("dirName:"+dirName)

	if not os.path.exists(dirName):
		try:
			os.mkdir(dirName)
		except Exception as e:
			print(str(e))

		if debug == True:
			print("Directory " , dirName ,  " Created ")
	else:
		if debug == True:
			print("Directory " , dirName ,  " already exists")
			
	return

def MakeDirFullPath(dirName, debug):
	if debug == True:
		print(dirName)

	if not os.path.exists(dirName):
		try:
			access_rights = 0o755
			os.makedirs(dirName,access_rights)
			if debug == True:
				print("Directory " , dirName ,  " Created ")
		except:
			if debug == True:
				print("Directory " , dirName ,  " Not created ")
			pass
	else:
		if debug == True:
			print("Directory " , dirName ,  " already exists")
		pass
			
	return

def __get_all_files_in_local_dir(local_dir,debug):
	all_files = list()

	if os.path.exists(local_dir):
		files = os.listdir(local_dir)
		for x in files:
			filename = os.path.join(local_dir, x)

			if debug==True: 
				print ("filename:" + filename)

			# isdir
			if os.path.isdir(filename):
				all_files.extend(__get_all_files_in_local_dir(filename))
			else:
				all_files.append(filename)
	else:
		if debug==True: 
			print ('{}does not exist'.format(local_dir))
		else: 
			pass
		
	return all_files

def is_debug():
	gettrace = getattr(sys, 'gettrace', None)

	if gettrace is None:
		return False
	else:
		v = gettrace()
		if v is None:
			return False
		else:
			return True
	pass

def get_filename_without_ext(file_name_full):

	try:
		file_name = os.path.splitext(file_name_full)[0]
	except Exception as e:
		print(str(e))
		file_name = ""
	
	return file_name

def conta_decimali(numero_str):
	if '.' in numero_str:
		parte_decimale = numero_str.split('.')[1]
		return len(parte_decimale)
	else:
		return 0
	pass

def format_number_to_string(number, formato_numerico):
	f_tmp = float(number)
	number_str = f"{f_tmp:.{formato_numerico}f}"
	return number_str
