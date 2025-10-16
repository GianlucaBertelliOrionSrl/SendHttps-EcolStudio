# import ClassSms
# from ClassSms import ClassSms

# ClassSms = ClassSms()

GlobalExit = 0
abspath = ""

class ClassStazione(object):
    abspath = ""
    def __init__(self):
        self.parametri_cfg = {}
        self.parametri = []
        self.sotto_configurazioni = []
        self.esiste = False
        self.cartelle = {}
        self.type_station = 0

    def add_attribute(self, attr_name, attr_value):
        setattr(self, attr_name, attr_value)

    def add_param_config(self, param):
        self.parametri.append(param)

    def aggiungi_parametro(self, chiave, valore):
        self.parametri[chiave] = valore

    def aggiungi_sotto_configurazione(self, sotto_configurazione):
        self.sotto_configurazioni.append(sotto_configurazione)

    def esiste_parametro(self, chiave):
        b = hasattr(self.ConfigJSON, chiave)
        return b
    
	# def aggiungi_cartella(self, chiave, valore):
	# 	self.cartelle[chiave] = valore	
	# def creazione_cartelle(self):
	# 	for chiave, cartella in self.cartelle.items():
	# 		print(f"Cartella: {chiave}   --> {cartella}")
	# 		ModuleFunctions.MakeDirFullPath(cartella,False)
	# 	pass
	# 	    
	# Funzione per leggere il file JSON e creare un'istanza della classe Configurazione
	# def leggi_configurazione(self,file_path):
	# 	try:
	# 		self.ConfigurazioneJSON = leggi_configurazione_da_file
	# 		if self.ConfigurazioneJSON != None:
	# 			self.esiste = True
	# 		else:
	# 			self.esiste = False
	# 	except Exception as e:
	# 		self.esiste = False
	# 		self.ConfigurazioneJSON = None
	# def stampa_configurazione(self):
	# 	stampa_configurazione(self.ConfigJSON, livello=0)

class ClassStationConfig:
    def __init__(self, **kwargs):
        # station_dictionary = {}
        # self.station_configuration = []

        for key, value in kwargs.items():
            setattr(self, key, value)

            #station_dictionary = {key,value}
            #self.station_configuration.append(station_dictionary)
        pass

    def __str__(self):
        return f'{self.Sigla}: {self.NomeEsteso}: {self.Ubicazione}'

    def add_configuration(self, station_configurations):
        self.configurations.append(station_configurations)

    def display_attributes(self):
        # Usa vars() per ottenere un dizionario degli attributi
        attributi = vars(self)
        #print(attributi)

        # Stampa ciascun attributo e valore
        for chiave, valore in attributi.items():
            print(f"{chiave}: {valore}")
        pass

#####################

class ClassParamConfig:
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

#################################

Stazione = ClassStazione()

cfg_stazione_json = ClassStationConfig()
