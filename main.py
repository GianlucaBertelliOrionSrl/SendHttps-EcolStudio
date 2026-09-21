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

import win32gui
import threading

import time
from datetime import datetime

import ModuleJSON

import ModulePostgres
from ModulePostgres import *

import ModuleSendHttps
from ModuleSendHttps import *

from ModuleUtils import get_base_dir

import logging
import ModuleLogger

from ModuleLogger import setup_logger

import Global

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
        attributi = vars(self)

        for chiave, valore in attributi.items():
            print(f"{chiave}: {valore}")
        pass

###############################################################################################

general_json_config = ClassGeneralJSONConfig()
ConfigVarieJSON = None

###############################################################################################

def GetGraphConfig(sigla_staz):
    global ConfigVarieJSON

    base_dir = get_base_dir()

    file_name = "Grafico" + sigla_staz + ".json"
    FileConfigVarie = os.path.join(base_dir,"cfg",file_name)

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
        return "#{:06X}".format(color)

    elif isinstance(color, str):
        return color.strip()

    else:
        raise ValueError(f"Formato colore non valido: {color}")

#############################################

def converti_valore(valore):
    if valore == "":
        return None

    elif isinstance(valore, str):
        valore_modificato = valore.replace(',', '.')
        try:
            if '.' in valore_modificato:
                return float(valore_modificato)
            else:
                return int(valore_modificato)
        except ValueError:
            return valore
    else:
        return valore

#############################################

def GetStationConfig(sigla_staz):
    global ConfigVarieJSON

    base_dir = get_base_dir()

    file_name = "Config" + sigla_staz + ".json"
    FileConfigVarie = os.path.join(base_dir,"cfg",file_name)

    try:
        ConfigVarieJSON = ModuleJSON.FileToJSON(FileConfigVarie)

    except Exception as e:
        print(f"Errore: {e}")
        return -1

    return 1

#################################################

def programma_ciclico(interval_sec=300, db_config=None, sigla=None, paramid_list=None, param_name_list=None, logger=None):
    """
    Ciclo principale:
    - legge dati dal DB
    - costruisce payload con parametri
    - invia via HTTPS
    - cicla ogni 'interval_sec' secondi

    Modalita' di invio:
    - secret_key non vuota: POST con header X-IOMS-KEY e payload unico
    - secret_key vuota: GET per ogni parametro con URL costruita da config
    """

    if logger is None:
        logger = logging.getLogger("AppLogger")

    secret_key = ConfigVarieJSON['secret_key']
    url_send_https = ConfigVarieJSON['send_https']
    params_config = ConfigVarieJSON['params_tx_dashboard']

    use_post_mode = (secret_key is not None and secret_key.strip() != "")

    logger.info("Avvio ciclo continuo")
    if use_post_mode:
        logger.info("Modalita' invio: POST con secret_key")
    else:
        logger.info("Modalita' invio: GET per parametro")

    to_do_send = 0
    to_do_flag = False

    while True:
        now = datetime.utcnow()
        minute = now.minute
        second = now.second

        try:
            if (minute % 5 == 0) and (second < 5) and (to_do_send == 0):
                to_do_send = 1
                start_time = time.time()
                try:
                    if verifica_connessione_db_postgres(db_config) != 1:
                        logger.warning("DB non connesso")
                    else:
                        logger.info("Invio dati https")

                        rows = leggi_dati(db_config, "averages.avg_60s_"+sigla.lower(), paramid_list, 1800, logger=logger)

                        valori_parametri = []
                        for row in rows[:len(param_name_list)]:
                            valore_str = row[4]
                            if valore_str is None or valore_str.strip() == "":
                                valore_float  = None
                            else:
                                try:
                                    valore_float = float(valore_str.replace(',', '.'))
                                except ValueError:
                                    valore_float = None

                            valori_parametri.append(valore_float)

                        dati_completi = dict(zip(param_name_list, valori_parametri))

                        epoch_now = epoch_utc()
                        epoch_5min = epoch_now - (epoch_now % 300)

                        if use_post_mode:
                            payload = {
                                "time": epoch_5min,
                                "version": "1.0",
                                **dati_completi
                            }

                            ModuleSendHttps.invia_dati_https(secret_key, payload, url_send_https)
                            logger.info(f"Dati inviati POST: {dati_completi}")

                        else:
                            for i, param_cfg in enumerate(params_config):
                                nome = param_cfg.get("name_param", "")
                                valore = dati_completi.get(nome, None)
                                ModuleSendHttps.invia_dati_https_get(param_cfg, valore, epoch_5min)

                            logger.info(f"Dati inviati GET: {dati_completi}")

                except Exception:
                    logger.error("Errore durante il ciclo", exc_info=True)

                elapsed = time.time() - start_time
                sleep_time = max(0, interval_sec - elapsed)
                logger.info(f"Fine ciclo, prossimo ciclo tra {sleep_time:.1f} sec")

            else:
                if (second % 5 == 0) and (not to_do_flag):
                    to_do_flag = True
                    print(PresentDateTimeEng(0))

                elif second % 5 != 0:
                    to_do_flag = False
            pass

            if (minute % 5 != 0) and (to_do_send != 0):
                to_do_send = 0

        except Exception as e:
            s = f"Errore: {e}"
            print(s)
            logger.error(s,  exc_info=True)

        time.sleep(0.1)

########################

def main(sigla_staz, dbg):

    logger = setup_logger(logging.DEBUG)
    logger.info("Applicazione avviata")

    try:

        if dbg == "dbg":
            root_path = "D:\\Dati_ETL_Total_181000076"
        else:
            root_path = "C:\\Dati_ETL"
        pass

        if os.getenv("VS_ENV") == "1":
            s = "Avviato da Visual Studio"
            print(s)
            logger.info(s)
        else:
            s = "Avviato da riga di comando"
            print(s)
            logger.info(s)
        pass

        check = GetStationConfig(sigla_staz)

        log_level_str = ConfigVarieJSON.get('log', 'debug').upper()
        log_level = getattr(logging, log_level_str, logging.DEBUG)
        logger.setLevel(log_level)
        for handler in logger.handlers:
            handler.setLevel(log_level)
        logger.info(f"Livello log impostato: {log_level_str}")

        params = ConfigVarieJSON["params_tx_dashboard"]

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

        interval_seconds = 300
        thread = threading.Thread(
            target=programma_ciclico,
            args=(interval_seconds, DB_CONFIG, sigla, paramid_list, param_name_list, logger),
            daemon=True
        )
        thread.start()

        try:
            while True:
                time.sleep(0.1)

        except KeyboardInterrupt:
            logger.info("Programma terminato dall'utente")

        ##############################

    except Exception as e:
        s = f"Errore: {e}"
        print(s)
        logger.error(s, exc_info=True)

    sys.exit(0)
    os._exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Report mensile Tirreno Power")
    parser.add_argument('--sigla_staz', type=str, default="1592309e102_etl02", help='Sigla staz.')
    parser.add_argument('--dbg', type=str, default="exe", help='Sigla staz.')
    args = parser.parse_args()

    main(args.sigla_staz, args.dbg)