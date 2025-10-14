from ast import Assign
from dataclasses import replace

import win32con
import win32com.client as win32
from win32com.client import Dispatch
import shutil
import sys, os
import argparse
import psutil
import string
import time
import win32gui
import threading

import ModuleJSON

import ModulePostgres
from ModulePostgres import *

import ModuleSendHttps
from ModuleSendHttps import *

import logging
import ModuleLogger

import Global

abspath = os.path.dirname(os.path.realpath(sys.argv[0]))
root_path = "D:\\Dati_ETL_Total_181000076"
logger = ModuleLogger.setup_logger(logging.DEBUG)

###############################################################################################

class ClassGeneralJSONConfig:
	def __init__(self, **kwargs):
		self.param_configurations = []

		for key, value in kwargs.items():
			setattr(self, key, value)
		pass
	
	def add_configuration(self, param_configurations):
		self.param_configurations.append(param_configurations)

	def __str__(self):
		return f'{self.Sigla}: {self.Codice}: {self.Nome}'

	def display_attributes(self):
		# Usa vars() per ottenere un dizionario degli attributi
		attributi = vars(self)
		#print(attributi)

		# Stampa ciascun attributo e valore
		for chiave, valore in attributi.items():
			print(f"{chiave}: {valore}")
		pass

###############################################################################################

general_json_config = ClassGeneralJSONConfig()
ConfigVarieJSON = None

###############################################################################################

def GetGraphConfig(sigla_staz):
	global ConfigVarieJSON

	file_name = "Grafico" + sigla_staz + ".json"
	FileConfigVarie = os.path.join(abspath,"cfg",file_name)

	try:
		ConfigVarieJSON = ModuleJSON.FileToJSON(FileConfigVarie)

	except Exception as e:
		print(f"Errore: {e}")
		return -1		

	return 1

###############################################################################################

def normalizza_colore(color):
	"""
	Accetta:
	- nome colore (stringa es: "blue")
	- codice hex stringa es: "#FF0000"
	- valore numerico es: 0xFF0000 o 16711680
	Ritorna sempre una stringa accettata da XlsxWriter
	"""
	if isinstance(color, int):
		# numerico → converto in hex #RRGGBB
		return "#{:06X}".format(color)

	elif isinstance(color, str):
		# già stringa → la ritorno così com’è
		return color.strip()

	else:
		raise ValueError(f"Formato colore non valido: {color}")

#############################################

def converti_valore(valore):
	if valore == "":
		return None  # valore nullo

	elif isinstance(valore, str):
		# sostituisco la virgola con il punto per numeri decimali
		valore_modificato = valore.replace(',', '.')
		try:
			# provo a convertire in int o float
			if '.' in valore_modificato:
				return float(valore_modificato)
			else:
				return int(valore_modificato)
		except ValueError:
			return valore  # se non è un numero, restituisco la stringa originale
	else:
		return valore  # se è già un numero

#############################################

def GetStationConfig(sigla_staz):
	global ConfigVarieJSON

	file_name = "Config" + sigla_staz + ".json"
	FileConfigVarie = os.path.join(abspath,"cfg",file_name)
	
	try:
		ConfigVarieJSON = ModuleJSON.FileToJSON(FileConfigVarie)

	except Exception as e:
		print(f"Errore: {e}")
		return -1
	
	return 1

#################################################

# --- Funzione ciclica che esegue il programma principale ---
def programma_ciclico_V0(interval_sec=300, db_config=None, sigla=None, paramid_list=None, param_name_list=None):

	logger.info("Inizio ciclo")
	secret_key = ConfigVarieJSON['secret_key']
	to_do = 0

	while True:
		#start_time = time.time()
		t = time.time()
		nn = Minutes()
		ss = Seconds()

		if (nn%5 == 0) and (ss < 5):
			start_time = time.time()

			try:
				db_connesso = verifica_connessione_db_postgres(db_config)

				if db_connesso == 1:
					#(DB_CONFIG, db_table, staz_name, paramid_list, period_sec)
					#secret_key = ConfigVarieJSON['secret_key']

					r = leggi_dati(db_config, "averages.avg_60s_01479", sigla, paramid_list, 60*60*24)
		
					valori_parametri = [float(r[0][4]), float(r[1][4]), float(r[2][4]), float(r[3][4])]  # valori letti dinamicamente		
					dati_completi = dict(zip(param_name_list, valori_parametri))

					#epoch_utc = ModuleTime.epoch
					epoch_utc = epoch_utc()
					epoch_utc_5min = epoch_utc - (epoch_utc % 300)
					version = "1.0"

					payload = {
						"time": epoch_utc_5min,
						"version": "1.0",
						**dati_completi  # unisce le coppie chiave/valore di `dati`
					}

					check = ModuleSendHttps.invia_dati_https(secret_key, payload)

			except Exception as e:
				logger.error("Errore durante il ciclo", exc_info=True)

			# Attendi l'intervallo specificato, considerando il tempo di esecuzione
			elapsed = time.time() - start_time
			sleep_time = max(0, interval_sec - elapsed)
			logger.info(f"Fine ciclo, prossimo ciclo tra {sleep_time:.1f} sec")
		else:
			if (ss%5 == 0) and (to_do == 0):
				to_do = 1
				s = PresentDateTime(0)
				print(s)
			
			if (ss%5 != 0) and (to_do != 0):
				to_do = 0
		pass

		time.sleep(0.1)

########################

import time
from datetime import datetime

def programma_ciclico(interval_sec=300, db_config=None, sigla=None, paramid_list=None, param_name_list=None):
	"""
	Ciclo principale:
	- legge dati dal DB
	- costruisce payload con parametri
	- invia via HTTPS
	- cicla ogni 'interval_sec' secondi
	"""

	secret_key = ConfigVarieJSON['secret_key']
	url_send_https = ConfigVarieJSON['send_https']

	logger.info("Avvio ciclo continuo")

	to_do_send = 0
	to_do_flag = False

	while True:
		now = datetime.utcnow()
		minute = now.minute
		second = now.second
		
		try:
			# Condizione: solo se siamo su multipli di 5 minuti e secondi < 5
			if (minute % 5 == 0) and (second < 5) and (to_do_send == 0):
				to_do_send = 1
				start_time = time.time()
				try:
					if verifica_connessione_db_postgres(db_config) != 1:
						logger.warning("DB non connesso")
					else:
						# Lettura dati dal DB
						logger.info("Invio dati https")
						rows = leggi_dati(db_config, "averages.avg_60s_"+sigla, sigla, paramid_list, 60*60*24)

						# # Estrazione valori dinamica
						# valori_parametri = [float(row[4].replace(',', '.')) for row in rows[:len(param_name_list)]]
						# dati_completi = dict(zip(param_name_list, valori_parametri))

						valori_parametri = []
						for row in rows[:len(param_name_list)]:
							valore_str = row[4]
							if valore_str is None or valore_str.strip() == "":
								# Gestione valore mancante
								valore_float = None
							else:
								try:
									# Sostituisco la virgola e converto a float
									valore_float = float(valore_str.replace(',', '.'))
								except ValueError:
									# Se non è convertibile, metto None o un valore di default
									valore_float = None

							valori_parametri.append(valore_float)

						dati_completi = dict(zip(param_name_list, valori_parametri))

						# Epoch UTC arrotondato a 5 minuti
						epoch_now = epoch_utc()
						epoch_5min = epoch_now - (epoch_now % 300)

						payload = {
							"time": epoch_5min,
							"version": "1.0",
							**dati_completi
						}

						# Invio HTTPS
						ModuleSendHttps.invia_dati_https(secret_key, payload, url_send_https)
						logger.info(f"Dati inviati: {dati_completi}")

				except Exception:
					logger.error("Errore durante il ciclo", exc_info=True)

				# Attende l'intervallo specificato considerando il tempo di esecuzione
				elapsed = time.time() - start_time
				sleep_time = max(0, interval_sec - elapsed)
				logger.info(f"Fine ciclo, prossimo ciclo tra {sleep_time:.1f} sec")

			else:
				# Esempio di log ogni 5 secondi
				if (second % 5 == 0) and (not to_do_flag):
					to_do_flag = True
					print(PresentDateTimeEng(0))  # stampa ogni 5 secondi

				elif second % 5 != 0:
					to_do_flag = False
			pass

			if (minute % 5 != 0) and (to_do_send != 0):
				to_do_send = 1

		except Exception as e:
			s = f"Errore: {e}"		
			print(s)
			logger.error(s,  exc_info=True)

		time.sleep(0.1)

########################

def main(*args):
	try:	

		if os.getenv("VS_ENV") == "1":
			s = "Avviato da Visual Studio"
			print(s)
			logger.info(s)

		else:
			s = "Avviato da riga di comando"
			print("Avviato da riga di comando")
			logger.info(s)
			root_path = "C:\\Dati_ETL"

		pass

		parser = argparse.ArgumentParser(description="Report mensile Tirreno Power")	
		parser.add_argument('--sigla_staz', type=str, default="001", help='Sigla staz.')
		parser.add_argument('--dbg', type=str, default="exe", help='Sigla staz.')
		args = parser.parse_args()

		sigla_staz = args.sigla_staz
		dbg = args.dbg

		if dbg == "dbg":
			root_path = "D:\\Dati_ETL_Total_181000076"
		else:
			root_path = "C:\\Dati_ETL"
		pass

		check = GetStationConfig(sigla_staz)

		# Estrae la lista dei parametri
		params = ConfigVarieJSON["params_tx_dashboard"]

		# Crea un vettore con tutti i paramid
		paramid_list = [p["paramid"] for p in params]
		param_name_list = [p["name_param"] for p in params]
		
		sigla = ConfigVarieJSON['sigla']
		db_ip = ConfigVarieJSON['db_ip']
		db_name = ConfigVarieJSON['db_name']
		db_user = ConfigVarieJSON['db_user']
		db_password = ConfigVarieJSON['db_password']
		db_port = ConfigVarieJSON['db_port']

		DB_CONFIG = {
			"dbname": db_name,
			"user": db_user,
			"password": db_password,
			"host": db_ip,
			"port": db_port
		}
		
		##############################

		# --- Thread per eseguire il programma ciclico ---
		interval_seconds = 300  # es. 5 minuti
		thread = threading.Thread(target=programma_ciclico, args=(interval_seconds,DB_CONFIG, sigla, paramid_list, param_name_list,), daemon=True)
		thread.start()

		# --- Il main thread può fare altro o rimanere attivo ---
		try:
			while True:
				time.sleep(0.1)  # main thread attivo, thread ciclico lavora in background

		except KeyboardInterrupt:
			logger.info("Programma terminato dall'utente")

		##############################

	except Exception as e:
		s = f"Errore: {e}"		
		#print(f"Errore: {e}")
		print(s)
		logger.info(s)

	sys.exit(0)
	os._exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Report mensile Tirreno Power")	
	parser.add_argument('--sigla_staz', type=str, default="01479", help='Sigla staz.')
	parser.add_argument('--dbg', type=str, default="exe", help='Sigla staz.')
	args = parser.parse_args()

	# ########################

	main(args)