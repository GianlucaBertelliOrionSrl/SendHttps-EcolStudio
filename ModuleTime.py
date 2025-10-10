import calendar
import time
import math

import ModuleFunctions
from ModuleFunctions import *

import datetime
from datetime import datetime, timedelta, timezone

from time import strftime
from time import sleep

def SleepMsec(millisec):
	sec = millisec/1000.0
	sleep(sec)

def SleepSec(sec):
	sleep(sec)

def epoch():
	epoch_time = int(time.time())
	return epoch_time

def epoch_utc():
	# Ora corrente in UTC
	ora_utc = datetime.now(timezone.utc)

	# Epoch (secondi dall'1/1/1970 UTC)
	epoch_utc = int(ora_utc.timestamp())

	return epoch_utc

def Seconds():
	dt = datetime.now().time() 
	sec = dt.second
	return sec

def Minutes():
	dt = datetime.now().time()
	min = dt.minute
	return min
		
def Hours():
	dt = datetime.now().time()
	hour = dt.hour
	return hour

def Day():
	dt = datetime.now().date()
	day = dt.day
	return day

def Month():
	dt = datetime.now().date()
	month = dt.month
	return month

def Year():
	dt = datetime.now().date()
	year = dt.year
	return year

def GetDateTimeElements():
	now = datetime.now()
		
	time_now = now.replace(microsecond=0).isoformat(' ')
	s = str(time_now)
	s1 = s.replace("-"," ")
	s2 = s1.replace(":"," ")
	s3 = s2.split(" ") 
	res = []

	for item in s3:
		try:
			c = int(item,10)
			res.append(c)
		except Exception as e:
			print(e)
			#ModuleFunctions.WriteLog(str(e))
			continue

	return res

def PresentDateTimeOLD():
	now = datetime.now()
	time_now = now.strftime("%d-%m-%Y,%H:%M:%S") + "\r\n"

	if len(time_now) == 0:
		s = []
		s = GetDateTimeElements() #[YYYY M D h m s]

		D0 = int(s[2])
		DD = "%02d" % (D0)

		M0 = int(s[1])
		MM = "%02d" % (M0)

		Y0 = int(s[0])
		YYYY = "%04d" % (Y0)
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		time_now = DD + "-" + MM +"-" + YYYY + "," + hh + ":" + mm + ":"+ ss + "\r\n"

	return time_now
		
def PresentDateTime(f):
	now = datetime.now()

	if f==0:
		time_now = now.strftime("%d-%m-%Y,%H:%M:%S")
	else:
		time_now = now.strftime("%d-%m-%Y,%H:%M:%S") + "\r\n"

	if len(time_now) == 0:
		s = []
		s = GetDateTimeElements() #[YYYY M D h m s]
		
		D0 = int(s[2])
		DD = "%02d" % (D0)

		M0 = int(s[1])
		MM = "%02d" % (M0)

		Y0 = int(s[0])
		YYYY = "%04d" % (Y0)
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		time_now = DD + "-" + MM +"-" + YYYY + "," + hh + ":" + mm + ":"+ ss + "\r\n"

	return time_now

def PresentDateTimeEng(f):
	now = datetime.now()

	if f==0:
		time_now = now.strftime("%Y-%m-%d %H:%M:%S")
	else:
		time_now = now.strftime("%Y-%m-%d %H:%M:%S") + "\r\n"

	if len(time_now)==0:
		s = GetDateTimeElements() #[YYYY M D h m s]
		
		D0 = int(s[2])
		DD = "%02d" % (D0)

		M0 = int(s[1])
		MM = "%02d" % (M0)

		Y0 = int(s[0])
		YYYY = "%04d" % (Y0)
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		if f==0:
			time_now = YYYY + "-" + MM + "-" + DD + " " + hh + ":" + mm + ":"+ ss
		else:
			time_now = YYYY + "-" + MM + "-" + DD + " " + hh + ":" + mm + ":"+ ss + "\r\n"

	return time_now

def PresentDateTimeEngFile():
	now = datetime.now()
	time_now = now.strftime("%Y%m%d%H%M%S")
		
	if len(time_now)==0:
		s = GetDateTimeElements() #[YYYY M D h m s]
		
		D0 = int(s[2])
		DD = "%02d" % (D0)

		M0 = int(s[1])
		MM = "%02d" % (M0)

		Y0 = int(s[0])
		YYYY = "%04d" % (Y0)
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		#("%Y%m%d%H%M%S")
		time_now = YYYY + MM + DD + hh + mm + ss
		
	return time_now

def PresentStrDate():
	now = datetime.now()
	date_now = now.strftime("%Y-%m-%d")

	if len(date_now) == 0:
		s = GetDateTimeElements() #[YYYY M D h m s]
		
		D0 = int(s[2])
		DD = "%02d" % (D0)

		M0 = int(s[1])
		MM = "%02d" % (M0)

		Y0 = int(s[0])
		YYYY = "%04d" % (Y0)
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		date_now = YYYY + "-" + MM + "-" + DD

	return date_now

def PresentStrTimeFile():
	now = datetime.now()
	time_now = now.strftime("%H%M%S")
		
	if len(time_now)==0:
		s = self.GetDateTimeElements() #[YYYY M D h m s]
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		time_now = hh + mm + ss
		
	return time_now

def PresentStrTimeFile10min():
	s = GetDateTimeElements() #[YYYY M D h m s]

	l_str = []
	h0 = int(s[3])
	hh = "%02d" % (h0)
	l_str.append(hh)

	m0 = (int(s[4])//10)*10
	mm = "%02d" % (m0)
	l_str.append(mm)

	#s0 = int(s[5])
	#ss = "%02d" % (s0)
	ss = '00'
	l_str.append(ss)

	time_now = "".join(l_str)

	return time_now

def PresentStrTimeFile60min():
	s = GetDateTimeElements() #[YYYY M D h m s]

	l_str = []
	h0 = int(s[3])
	hh = "%02d" % (h0)
	l_str.append(hh)

	mm = '00'
	l_str.append(mm)

	ss = '00'
	l_str.append(ss)

	time_now = "".join(l_str)

	return time_now

def MinSecStr():
	s = []
	s = GetDateTimeElements() #[YYYY M D h m s]

	l_str = []
	m0 = int(s[4])
	mm = "%02d" % (m0)
	l_str.append(mm)

	s0 = int(s[5])
	ss = "%02d" % (s0)
	l_str.append(ss)

	time_now = "".join(l_str)

	return time_now

def OraMinSecStr():
	s = []
	s = GetDateTimeElements() #[YYYY M D h m s]

	l_str = []

	h0 = int(s[3])
	hh = "%02d" % (h0)
	l_str.append(hh)

	m0 = int(s[4])
	mm = "%02d" % (m0)
	l_str.append(mm)

	s0 = int(s[5])
	ss = "%02d" % (s0)
	l_str.append(ss)

	time_now = "".join(l_str)

	return time_now

def AnnoMeseGioStr():
	s = []
	s = GetDateTimeElements() #[YYYY M D h m s]

	l_str = []

	Y0 = int(s[0])
	Y = "%04d" % (Y0)
	l_str.append(Y)

	M0 = int(s[1])
	M = "%02d" % (M0)
	l_str.append(M)

	D0 = int(s[2])
	D = "%02d" % (D0)
	l_str.append(D)

	time_now = "".join(l_str)

	return time_now

def PresentStrHourFile():
	now = datetime.now()
	time_now = "000000"
		
	s = GetDateTimeElements() #[YYYY M D h m s]
		
	h0 = int(s[3])
	hh = "%02d" % (h0)

	time_now = hh + "0000"
		
	return time_now

def PresentStrDateFile():
	now = datetime.now()
	date_now = now.strftime("%Y%m%d")

	if len(date_now)==0:
		s = GetDateTimeElements() #[YYYY M D h m s]
		
		D0 = int(s[2])
		DD = "%02d" % (D0)

		M0 = int(s[1])
		MM = "%02d" % (M0)

		Y0 = int(s[0])
		YYYY = "%04d" % (Y0)
		
		h0 = int(s[3])
		hh = "%02d" % (h0)

		m0 = int(s[4])
		mm = "%02d" % (m0)

		s0 = int(s[5])
		ss = "%02d" % (s0)

		date_now = YYYY + MM + DD

	return date_now

def PresentStrDateFileEda(language):
	s = GetDateTimeElements() #[YYYY M D h m s]
		
	D0 = int(s[2])
	DD = "%d" % (D0)
	MM = int(s[1])

	MM_str = ''
	if MM==1:
		MM_str = 'JANUARY'
	elif MM==2:
		MM_str = 'FEBRUARY'
	elif MM==3:
		MM_str = 'MARCH'
	elif MM==4:
		MM_str = 'APRIL'
	elif MM==5:
		MM_str = 'MAY'
	elif MM==6:
		MM_str = 'JUNE'
	elif MM==7:
		MM_str = 'JULY'
	elif MM==8:
		MM_str = 'AUGUST'
	elif MM==9:
		MM_str = 'SEPTEMBER'
	elif MM==10:
		MM_str = 'OCTOBER'
	elif MM==11:
		MM_str = 'NOVEMBER'
	elif MM==12:
		MM_str = 'DECEMBER'

	Y0 = int(s[0])
	YYYY = "%04d" % (Y0)
	date_now = DD + ' ' + MM_str + ' ' + YYYY

	return date_now

def YesterdayStrDateFileEda(language):
	yesterday = datetime.now() - timedelta(1)
	s = yesterday.strftime("%Y %m %d")
		
	DD = int(yesterday.day)
	MM = int(yesterday.month)
		
	MM_str = ''
	if MM==1:
		MM_str = 'JANUARY'
	elif MM==2:
		MM_str = 'FEBRUARY'
	elif MM==3:
		MM_str = 'MARCH'
	elif MM==4:
		MM_str = 'APRIL'
	elif MM==5:
		MM_str = 'MAY'
	elif MM==6:
		MM_str = 'JUNE'
	elif MM==7:
		MM_str = 'JULY'
	elif MM==8:
		MM_str = 'AUGUST'
	elif MM==9:
		MM_str = 'SEPTEMBER'
	elif MM==10:
		MM_str = 'OCTOBER'
	elif MM==11:
		MM_str = 'NOVEMBER'
	elif MM==12:
		MM_str = 'DECEMBER'

	YYYY = int(yesterday.year)

	date_now = str(DD) + ' ' + MM_str + ' ' + str(YYYY)
	return date_now		

def Time():
	return time.time()

def DateTimeFromSeconds(sec,utc):
	if utc == 0:
		d = datetime.fromtimestamp(int(sec))
	else:
		d = datetime.utcfromtimestamp(int(sec))

	time_now = d.strftime("%Y-%m-%d %H:%M:%S")

	return time_now

def AddDate(date_and_time,delta_time_min):
	try:
		# Calling the timedelta() function 
		#time_change = datetime.timedelta(minutes=75)
		time_change = timedelta(minutes = delta_time_min)
		new_time = date_and_time + time_change

	except Exception as e:
		print(str(e))
		new_time = date_and_time
	
	return new_time

def date2unix(vDate: datetime) -> int:
    """
    Converte una data in secondi trascorsi dal 1 gennaio 2000
    """
    base_date = datetime(2000, 1, 1)
    delta = vDate - base_date
    return int(delta.total_seconds())
