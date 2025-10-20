import os
import sys
import logging
import threading
import time

from datetime import datetime

#from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

from ModuleUtils import get_base_dir

"""
    Crea un logger compatibile con PyInstaller, servizi e script Python.
    Ogni giorno crea un nuovo file log nella cartella:
        <cartella_eseguibile_o_script>/LogFiles/LogFile_YYYY-MM-DD.log

    Parametri:
      - level: livello di logging (es. logging.DEBUG)
      - max_bytes: dimensione massima per ogni file log (default 5 MB)
      - backup_count: numero massimo di file log conservati (default 10)
    """

# 🔹 Setup logger giornaliero con rotazione
def setup_logger(level=logging.INFO):
    """
    Crea un logger che scrive in:
      <base_dir>/LogFiles/LogFile_YYYY-MM-DD.log
    Il file cambia automaticamente a mezzanotte.
    """
    base_dir = get_base_dir()
    log_dir = os.path.join(base_dir, "LogFiles")
    os.makedirs(log_dir, exist_ok=True)

    def make_logger_for_today():
        today_str = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"LogFile_{today_str}.log")

        logger = logging.getLogger("AppLogger")
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(level)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info(f"Logger inizializzato: {log_file}")
        return logger, today_str

    # Crea logger iniziale
    logger, current_date = make_logger_for_today()

    # Thread che controlla il cambio giorno
    def watch_day_change():
        nonlocal logger, current_date
        while True:
            time.sleep(0.1)
            new_date = datetime.now().strftime("%Y-%m-%d")
            if new_date != current_date:
                logger.info("Cambio data rilevato, creazione nuovo file log...")
                logger, current_date = make_logger_for_today()

    threading.Thread(target=watch_day_change, daemon=True).start()

    return logger


#TENERE ESEMPIO
# def setup_logger_V1(level=logging.INFO, max_bytes=5_000_000, backup_count=10):
#     # 🔸 1. Determina la directory base
#     base_dir = get_base_dir()

#     # 🔸 2. Crea sottocartella "LogFiles" se non esiste
#     log_dir = os.path.join(base_dir, "LogFiles")
#     os.makedirs(log_dir, exist_ok=True)

#     # 🔸 3. Nome file log con data giornaliera
#     today_str = datetime.now().strftime("%Y-%m-%d")
#     log_file = os.path.join(log_dir, f"LogFile_{today_str}.log")

#     # 🔸 4. Crea/recupera il logger
#     logger = logging.getLogger("AppLogger")

#     # 🔸 5. Rimuove eventuali handler precedenti (evita duplicati e percorsi vecchi)
#     if logger.hasHandlers():
#         logger.handlers.clear()

#     # 🔸 6. Configura livello e formato
#     logger.setLevel(level)
#     formatter = logging.Formatter(
#         "%(asctime)s | %(levelname)-8s | %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )

#     # 🔸 7. Handler console
#     ch = logging.StreamHandler()
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)

#     # 🔸 8. Handler file rotante
#     fh = RotatingFileHandler(
#         log_file,
#         maxBytes=max_bytes,
#         backupCount=backup_count,
#         encoding="utf-8"
#     )
#     fh.setFormatter(formatter)
#     logger.addHandler(fh)

#     # 🔸 9. Messaggio iniziale
#     logger.info(f"Logger inizializzato. Scrive su: {log_file}")
#     logger.debug(f"Base dir: {base_dir}")

#     return logger

############################################################################

#TENERE ESEMPIO
# def setup_logger_V0(level=logging.INFO):
# 	# Percorso base = cartella dove si trova l'eseguibile o lo script
# 	#base_dir = os.path.dirname(os.path.abspath(__file__))

# 	# Determina la directory base (diversa se l'app è "freezata" da PyInstaller)
# 	base_dir = get_base_dir()

# 	# Crea sottocartella LogFiles/YYYY-MM-DD
# 	today_str = datetime.now().strftime("%Y-%m-%d")
# 	log_dir = os.path.join(base_dir, "LogFiles", today_str)
# 	os.makedirs(log_dir, exist_ok=True)

# 	# Nome file log
# 	log_file = os.path.join(log_dir, "LogFile.log")

# 	# Crea il logger
# 	logger = logging.getLogger("AppLogger")
# 	logger.setLevel(level)

# 	# Evita duplicazione handler se setup_logger viene chiamato più volte
# 	if not logger.handlers:
# 		# Formato del log
# 		formatter = logging.Formatter(
# 			"%(asctime)s | %(levelname)s | %(message)s",
# 			datefmt="%Y-%m-%d %H:%M:%S"
# 		)

# 		# Handler per console
# 		ch = logging.StreamHandler()
# 		ch.setFormatter(formatter)
# 		logger.addHandler(ch)

# 		# Handler per file
# 		fh = logging.FileHandler(log_file, encoding="utf-8")
# 		fh.setFormatter(formatter)
# 		logger.addHandler(fh)

# 	return logger

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
