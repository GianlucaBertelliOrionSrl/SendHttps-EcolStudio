import requests
import time
from urllib.parse import urlencode

import logging
import ModuleLogger

from ModuleUtils import get_base_dir

logger = ModuleLogger.setup_logger(logging.DEBUG)

# Configurazione
API_URL = "https://ioms.tabsrl.com/api/measures/STBN9NW"
API_KEY = "Tbggllb3x46t0J3nY3Nj_kGpUY_jEp"

HEADERS = {
    "X-IOMS-KEY": API_KEY,
    "accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Funzione per inviare una riga di dati
def invia_dati_https(secret_key, payload, url_send_https):
    """
    row = tuple con i valori (epoch, version, voc, c6h6, h2s, pid)

    Es:
    curl -X 'POST' 'https://ioms.tabsrl.com/api/measures/STBN9NW' \
    -H 'X-IOMS-KEY: Tbggllb3x46t0J3nY3Nj_kGpUY_jEp' \
    -H 'accept: */*' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'time=1758705000&version=1.0&voc=0.15&c6h6=0.44&h2s=0.0&pid=0.08'

    """
    # payload = {
    # 	"time": int(row[0]),         # epoch
    # 	"version": row[1],          # version, es. "1.0"
    # 	"voc": float(row[2]),
    # 	"c6h6": float(row[3]),
    # 	"h2s": float(row[4]),
    # 	"pid": float(row[5])
    # }

    MY_API_URL = url_send_https

    MY_HEADERS = {
        "X-IOMS-KEY": secret_key,
        "accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(MY_API_URL, headers=MY_HEADERS, data=payload)
        if response.status_code == 200:
            s = f"✅ Dato inviato: {payload}"
            #print(f"✅ Dato inviato: {payload}")
            print(s)
            logger.info(s)
            return 1

        else:
            s = f"⚠️ Errore {response.status_code}: {response.text}"
            #print(f"⚠️ Errore {response.status_code}: {response.text}")
            print(s)
            logger.info(s)
            return -1

    except Exception as e:
        s = f"❌ Errore durante invio: {e}"
        #print(f"❌ Errore durante invio: {e}")
        print(s)
        logger.info(s)
        return -2


def invia_dati_https_get(param_config, valore, epoch_time):
    """
    Invio dati via GET URL per configurazioni senza secret_key.

    Costruisce la URL nel formato:
      {send_https}{name_param}{value_suffix}{valore}{time_prefix}{epoch}

    Es:
      https://online.purenviro.com/api_addSensorData.php?db=P73&ui=P73API&p=xxx...&tb=C6H6&v=0.27&t=1790010311

    Parametri:
      param_config : dict con i campi del parametro dal JSON di configurazione
      valore       : valore numerico da inviare
      epoch_time   : timestamp epoch per il campo time
    """

    name_param = param_config.get("name_param", "")
    url_base = param_config.get("send_https", "")
    value_suffix = param_config.get("value_suffix", "&v=")
    time_prefix = param_config.get("time_prefix", "&t=")
    use_timestamp = param_config.get("use_timestamp", 1)

    if valore is None:
        s = f"⚠️ Valore None per parametro {name_param}, invio saltato"
        print(s)
        logger.info(s)
        return 0

    url = f"{url_base}{name_param}{value_suffix}{valore}"

    if use_timestamp == 1:
        url = f"{url}{time_prefix}{int(epoch_time)}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            s = f"✅ Dato inviato GET: {name_param}={valore} t={int(epoch_time)}"
            print(s)
            logger.info(s)
            return 1
        else:
            s = f"⚠️ Errore GET {response.status_code}: {response.text} URL: {url}"
            print(s)
            logger.info(s)
            return -1

    except Exception as e:
        s = f"❌ Errore durante invio GET: {e}"
        print(s)
        logger.info(s)
        return -2