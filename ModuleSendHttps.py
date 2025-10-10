import requests
import time

# Configurazione
API_URL = "https://ioms.tabsrl.com/api/measures/STBN9NW"
API_KEY = "Tbggllb3x46t0J3nY3Nj_kGpUY_jEp"

HEADERS = {
    "X-IOMS-KEY": API_KEY,
    "accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Funzione per inviare una riga di dati
def invia_dati_https(row):
	"""
	row = tuple con i valori (epoch, version, voc, c6h6, h2s, pid)
  
	Es:
    curl -X 'POST' 'https://ioms.tabsrl.com/api/measures/STBN9NW' \
    -H 'X-IOMS-KEY: Tbggllb3x46t0J3nY3Nj_kGpUY_jEp' \
    -H 'accept: */*' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'time=1758705000&version=1.0&voc=0.15&c6h6=0.44&h2s=0.0&pid=0.08'

	"""
	payload = {
		"time": int(row[0]),         # epoch
		"version": row[1],          # version, es. "1.0"
		"voc": float(row[2]),
		"c6h6": float(row[3]),
		"h2s": float(row[4]),
		"pid": float(row[5])
	}

	try:
		response = requests.post(API_URL, headers=HEADERS, data=payload)
		if response.status_code == 200:
			print(f"✅ Dato inviato: {payload}")
		else:
			print(f"⚠️ Errore {response.status_code}: {response.text}")

	except Exception as e:
		print(f"❌ Errore durante invio: {e}")