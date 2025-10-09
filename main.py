from ast import Assign
from dataclasses import replace

#import xlsxwriter

import win32con
import win32com.client as win32
from win32com.client import Dispatch
import shutil
import tempfile
import sys, os
import argparse
import psutil
import copy
import string
import time
import win32gui

import ModuleJSON
import ModulePostgres
from ModulePostgres import *
import Global

abspath = os.path.dirname(os.path.realpath(sys.argv[0]))
root_path = "D:\\Dati_ETL_Total_181000076"


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

def main(*args):
	try:	
		if os.getenv("VS_ENV") == "1":
			print("Avviato da Visual Studio")
		else:
			print("Avviato da riga di comando")
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
		
		#db_connesso = verifica_connessione_db_postgres(db_ip, db_name, db_user, db_password, db_port)
		db_connesso = verifica_connessione_db_postgres(DB_CONFIG)

		if db_connesso == 1:
			db_dati = leggi_dati(DB_CONFIG, "averages.avg_60s_01479")

	except Exception as e:
		print(f"Errore: {e}")

	sys.exit(0)
	os._exit(0)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Report mensile Tirreno Power")	
	parser.add_argument('--sigla_staz', type=str, default="01479", help='Sigla staz.')
	parser.add_argument('--dbg', type=str, default="exe", help='Sigla staz.')
	args = parser.parse_args()

	# ########################

	main(args)