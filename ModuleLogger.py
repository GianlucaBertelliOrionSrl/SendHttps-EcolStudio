import logging
import os
from datetime import datetime

def setup_logger(level=logging.INFO):
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
