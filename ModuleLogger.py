import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger_V0(level=logging.INFO):
	# Percorso base = cartella dove si trova l'eseguibile o lo script
	base_dir = os.path.dirname(os.path.abspath(__file__))

	# Crea sottocartella LogFiles/YYYY-MM-DD
	today_str = datetime.now().strftime("%Y-%m-%d")
	log_dir = os.path.join(base_dir, "LogFiles", today_str)
	os.makedirs(log_dir, exist_ok=True)

	# Nome file log
	log_file = os.path.join(log_dir, "LogFile.log")

	# Crea il logger
	logger = logging.getLogger("AppLogger")
	logger.setLevel(level)

	# Evita duplicazione handler se setup_logger viene chiamato più volte
	if not logger.handlers:
		# Formato del log
		formatter = logging.Formatter(
			"%(asctime)s | %(levelname)s | %(message)s",
			datefmt="%Y-%m-%d %H:%M:%S"
		)

		# Handler per console
		ch = logging.StreamHandler()
		ch.setFormatter(formatter)
		logger.addHandler(ch)

		# Handler per file
		fh = logging.FileHandler(log_file, encoding="utf-8")
		fh.setFormatter(formatter)
		logger.addHandler(fh)

	return logger



def setup_logger(level=logging.INFO, max_bytes=5_000_000, backup_count=10):
	"""
	Crea un logger compatibile con PyInstaller, con log rotante.
	Salva i log in:
	  <cartella_eseguibile_o_script>/LogFiles/YYYY-MM-DD/LogFile.log

	Parametri:
	  - level: livello di logging (es. logging.DEBUG)
	  - max_bytes: dimensione massima per file log prima della rotazione (default 5 MB)
	  - backup_count: numero massimo di file log conservati (default 10)
	"""

	# Determina la directory base (diversa se l'app è "freezata" da PyInstaller)
	if getattr(sys, 'frozen', False):
		base_dir = os.path.dirname(sys.executable)
	else:
		base_dir = os.path.dirname(os.path.abspath(__file__))

	# Crea sottocartella LogFiles/YYYY-MM-DD
	today_str = datetime.now().strftime("%Y-%m-%d")
	log_dir = os.path.join(base_dir, "LogFiles", today_str)
	os.makedirs(log_dir, exist_ok=True)

	# Nome file log
	log_file = os.path.join(log_dir, "LogFile.log")

	# Crea il logger
	logger = logging.getLogger("AppLogger")
	logger.setLevel(level)

	# Evita duplicazione handler
	if not logger.handlers:
		formatter = logging.Formatter(
			"%(asctime)s | %(levelname)s | %(message)s",
			datefmt="%Y-%m-%d %H:%M:%S"
		)

		# Handler console
		ch = logging.StreamHandler()
		ch.setFormatter(formatter)
		logger.addHandler(ch)

		# Handler file rotante
		fh = RotatingFileHandler(
			log_file,
			maxBytes=max_bytes,
			backupCount=backup_count,
			encoding="utf-8"
		)
		fh.setFormatter(formatter)
		logger.addHandler(fh)

		logger.info(f"Logger inizializzato, scrive su: {log_file}")

	return logger



# # Esempio di utilizzo
# if __name__ == "__main__":
#     logger = setup_logger(logging.DEBUG)

#     logger.info("Avvio programma")
#     logger.debug("Esempio di messaggio di debug")
#     try:
#         x = 10 / 0
#     except Exception as e:
#         logger.error("Errore durante l'elaborazione", exc_info=True)
#     logger.info("Fine programma")
