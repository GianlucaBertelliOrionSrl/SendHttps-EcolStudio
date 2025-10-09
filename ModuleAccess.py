import pyodbc
import os, sys
from datetime import datetime, timedelta
from win32com.client import Dispatch

from collections import defaultdict

from typing import List, Dict, Any, Tuple

import ModuleFunctions
from ModuleFunctions import *

import ClassAccess
from ClassAccess import *

import Global
from Global import *

#root_path = "D:\\Dati_ETL_Total_181000076"
# Specifica il percorso del tuo database Access97
#database_path = r"C:\percorso\al\tuo\database.mdb"
#database_path = root_path + "\\Config\\Rete.mdb"

#abspath = os.path.dirname(os.path.realpath(sys.argv[0]))
abspath = os.path.dirname(os.path.abspath(__file__))

def GetReteDbConfigs(root_path, database_path):

    rete_db_config = MainConfig()
    db_temp_file_path = create_temp_copy(database_path)

    ##############################################

    # Crea la stringa di connessione ODBC
    connection_string = (
	    r"DRIVER={Microsoft Access Driver (*.mdb)};"
	    r"DBQ=" + db_temp_file_path + ";"
    )

    try:
        # Crea una connessione al database
        connection = pyodbc.connect(connection_string)
    
        # Crea un cursore per eseguire le query
        cursor = connection.cursor()
    
        # Esegui una query per selezionare tutti i dati dalla tabella
        table_name = "Stazioni"  # Sostituisci con il nome della tua tabella

        stations_container = ClassConfigContainer()

        cursor.execute(f"SELECT * FROM Stazioni ORDER BY Sigla ASC")

        Stazione = ClassStazione()

        # # Ottieni i nomi dei campi
        column_names = []
        column_names = [desc[0] for desc in cursor.description]

        # for col in column_names:
        #     Stazione.add_attribute(col,col)
        # pass

        # Stampa i valori dei campi per ogni riga
        #print("\nValori dei campi:")

        for row in cursor.fetchall():
            db_field_values = []

            for name, value in zip(column_names, row):
                db_field_values.append(value)
                Stazione.add_attribute(name,value)
            pass

            # Inizializza un dizionario vuoto
            dictionary = {}

            # Usa un ciclo for per popolare il dizionario
            for name, value in zip(column_names, db_field_values):
                dictionary[name] = value
            pass

            config_sts = dictionary

            stazione1 = Global.ClassStationConfig(**config_sts)
            stazione1.display_attributes()

            staz_param_config = ClassStationParamConfig()
            staz_param_config.add_station_config(stazione1)

            SiglaSelezionata = dictionary["Sigla"]

            cursor.execute(f"SELECT * FROM Parametri WHERE Sigla = '" + SiglaSelezionata + "' ORDER BY Codice ASC")

            ##########################################################

            column_names2 = []
            column_names2 = [desc[0] for desc in cursor.description]
        
            # Stampa i valori dei campi per ogni riga
            print("\nValori dei campi:")

            config_params = []
            for row2 in cursor.fetchall():
                db_field_values2 = []

                for name, value in zip(column_names, row2):
                    db_field_values2.append(value)
                pass

                # Inizializza un dizionario vuoto
                dictionary2 = {}

                # Usa un ciclo for per popolare il dizionario
                for name, value in zip(column_names2, db_field_values2):
                    dictionary2[name] = value
                pass

                # Stampa il dizionario risultante
                #print(dictionary2)

                config_single_params = dictionary2
                param = ClassParamConfig(**config_single_params)
                
                #Stazione.aggiungi_parametro('exe', exe)

                param.display_attributes()

                #staz_param_config = ClassStationParamConfig()
                #staz_param_config.add_station_config(stazione1)

                staz_param_config.add_param_config(param)

                stations_container.add_configuration(staz_param_config)

                Stazione.add_param_config(config_single_params)
            pass

            ##########################################################

            #rete_db_config.add_config_container(stations_container)
            rete_db_config.add_config_container(staz_param_config)
        pass
          
        # Chiudi la connessione
        cursor.close()
        connection.close()

        for container in rete_db_config.config_containers:
            for config in container.station_configurations:
                for cfg in config.station_configurations:
                    #cfg.display_attributes()

                    station_configurations = vars(cfg)
                    station_code = station_configurations['Sigla']

                    # for chiave, valore in station_configurations.items():
                    #     #print(f"{chiave}: {valore}")
                    #     station_code = valore
                    #     station_code = station_configurations['Sigla']
                    # pass
                pass
            pass
        pass

    except Exception as e:
	    print(f"Errore durante l'accesso al database: {e}")

    # finally:
    # 	# Chiudi la connessione al database
    # 	if 'connection' in locals():
    # 		cursor.close()
    #         connection.close()

def GetReteDbConfig_V2(root_path, database_path):
    global Stazione

    db_temp_file_path = create_temp_copy(database_path)

    ##############################################

    # Crea la stringa di connessione ODBC
    connection_string = (
	    r"DRIVER={Microsoft Access Driver (*.mdb)};"
	    r"DBQ=" + db_temp_file_path + ";"
    )

    try:
        # Crea una connessione al database
        connection = pyodbc.connect(connection_string)
    
        # Crea un cursore per eseguire le query
        cursor = connection.cursor()
    
        # Esegui una query per selezionare tutti i dati dalla tabella
        table_name = "Stazioni"  # Sostituisci con il nome della tua tabella

        #stations_container = ClassConfigContainer()

        cursor.execute(f"SELECT * FROM Stazioni ORDER BY Sigla ASC")

        # # Ottieni i nomi dei campi
        column_names = []
        column_names = [desc[0] for desc in cursor.description]

        for row in cursor.fetchall():
            db_field_values = []

            for name, value in zip(column_names, row):
                db_field_values.append(value)
                Stazione.add_attribute(name,value)
            pass

            # Inizializza un dizionario vuoto
            dictionary = {}

            # Usa un ciclo for per popolare il dizionario
            for name, value in zip(column_names, db_field_values):
                dictionary[name] = value
            pass

            config_sts = dictionary

            stazione1 = Global.ClassStationConfig(**config_sts)
            stazione1.display_attributes()

            staz_param_config = ClassStationParamConfig()
            staz_param_config.add_station_config(stazione1)

            SiglaSelezionata = dictionary["Sigla"]

            cursor.execute(f"SELECT * FROM Parametri WHERE Sigla = '" + SiglaSelezionata + "' ORDER BY Codice ASC")

            ##########################################################

            column_names2 = []
            column_names2 = [desc[0] for desc in cursor.description]
        
            # Stampa i valori dei campi per ogni riga
            print("\nValori dei campi:")

            config_params = []
            for row2 in cursor.fetchall():
                db_field_values2 = []

                for name, value in zip(column_names, row2):
                    db_field_values2.append(value)
                pass

                # Inizializza un dizionario vuoto
                dictionary2 = {}

                # Usa un ciclo for per popolare il dizionario
                for name, value in zip(column_names2, db_field_values2):
                    dictionary2[name] = value
                pass

                config_single_params = dictionary2

                Stazione.add_param_config(config_single_params)
            pass

            ##########################################################
        pass
          
        # Chiudi la connessione
        cursor.close()
        connection.close()

        return 1

    except Exception as e:
        print(f"Errore durante l'accesso al database: {e}")
        return -1

##########################################################################################################

def query_medie_orarie(database_path,sigla_staz,giorno_inizio,giorno_fine,code_sez,tipo_dati,vettore_paramid,tipo_db):
    global Stazione

#SEZIONE = 155
#NOX_QAL2 = 702
#CO_QAL2 = 813
#PORTATA = 623
#O2_QAL2 = 629

    db_temp_file_path = database_path

    ##############################################

    ##############################################

    if tipo_db == 0:
        # Crea la stringa di connessione ODBC
        connection_string = (
	        r"DRIVER={Microsoft Access Driver (*.mdb)};"
	        r"DBQ=" + db_temp_file_path + ";"
        )
    else:
        # Crea la stringa di connessione ODBC
        connection_string = (
	        r"DRIVER={Microsoft Access Driver (*.mdb)};"
	        r"DBQ=" + db_temp_file_path + ";"
            r"PWD=eutiFrone;"
        )
    pass

    try:
        # Crea una connessione al database
        connection = pyodbc.connect(connection_string)
    
        # Crea un cursore per eseguire le query
        cursor = connection.cursor()
    
        # Esegui una query per selezionare tutti i dati dalla tabella
        table_name = "Misure"  # Sostituisci con il nome della tua tabella
       
        ####################################################################################
        
        if tipo_dati == 0:   #TAL QUALE
            strSQL = f"SELECT Data, Ora, ParamID, Media, Status FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
                "# AND Data <= #" + str(giorno_fine) + "# " + \
                " AND ParamID = " + str(code_sez) + \
                " AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"

        elif tipo_dati == 1: #NORM
            strSQL = f"SELECT Data, Ora, ParamID, Media, medianorm, statusnorm FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
                "# AND Data <= #" + str(giorno_fine) + "# " + \
                " AND ParamID = " + str(code_sez) + \
                " AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"

        if tipo_dati == 2:   #NORM.O2
            strSQL = f"SELECT Data, Ora, ParamID, Media, medianormO2, StatusnormO2 FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
                "# AND Data <= #" + str(giorno_fine) + "# " + \
                " AND ParamID = " + str(code_sez) + \
                " AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"
        pass

        #Data, Ora, Media, medianormO2, PercnormO2

        print(strSQL)
        cursor.execute(strSQL)

        # # Ottieni i nomi dei campi  
        column_names = []     
        column_names = [desc[0] for desc in cursor.description]
        valoriSEZ = []
        batch_size = 10

        ####################################################################################

        # for row in cursor.fetchall():
        #     db_field_values = []
        #     for name, value in zip(column_names, row):
        #         db_field_values.append(value)
        #     pass
        #     # Inizializza un dizionario vuoto
        #     dictionary = {}
        #     # Usa un ciclo for per popolare il dizionario
        #     for name, value in zip(column_names, db_field_values):
        #         dictionary[name] = value               
        #     pass           
        #     # Chiavi che vogliamo includere nel sotto-dizionario
        #     chiavi_da_includere = ["Data", "Ora", "Media", "medianormO2", "PercnormO2"]
        #     # Creazione del sotto-dizionario
        #     sotto_dizionario = {chiave: dictionary[chiave] for chiave in chiavi_da_includere}
        #     valoriSEZ.append(sotto_dizionario)
        # pass
        
        ####################################################################################

        ####################################################################################
        
        if tipo_dati == 0: #TAL QUALE
            # Chiavi che vogliamo includere nel sotto-dizionario
            chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "Status"]

        elif tipo_dati == 1: #NORM
            # Chiavi che vogliamo includere nel sotto-dizionario
            chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianorm", "StatusnormO2"]

        else:
            #tipo_dati == 2: #NORM.O2
            # Chiavi che vogliamo includere nel sotto-dizionario
            chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianormO2", "StatusnormO2"]
        pass

        #for row in cursor.fetchall():
        
        ##################################################################
        # Recupera 10 righe alla volta
        batch_size = 100
        while True:
            righe = cursor.fetchmany(batch_size)
            if not righe:
                break

            for row in righe:

                db_field_values = []

                for name, value in zip(column_names, row):
                    if (name == "Media") or (name == "medianorm") or (name == "medianormO2") or \
                        (name == "Status") or (name == "statusnorm") or (name == "StatusnormO2"):
                        val_format = f"{value:.0f}"
                    else:
                        val_format = value
                    pass

                    db_field_values.append(val_format)
                pass

                # Inizializza un dizionario vuoto
                dictionary = {}

                # Usa un ciclo for per popolare il dizionario
                for name, value in zip(column_names, db_field_values):
                    dictionary[name] = value               
                pass
                
                # Creazione del sotto-dizionario
                sotto_dizionario = {chiave: dictionary[chiave] for chiave in chiavi_da_includere}

                valoriSEZ.append(sotto_dizionario)
            pass
        pass
        ##################################################################

        ####################################################################################
        paramid_str = "("
        for p in vettore_paramid:
            paramid_str = paramid_str + str(p) + ","
        pass
        
        paramid_str = paramid_str[:-1] + ")"

        ####################################################################################
        # strSQL = f"SELECT * FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
        #     "# AND Data <= #" + str(giorno_fine) + "# " + \
        #     "AND ParamID IN " + paramid_str + \
        #     "AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"

        if tipo_dati == 0: #TAL QUALE            
            strSQL = f"SELECT Data, Ora, ParamID, Media, Status FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
                "# AND Data <= #" + str(giorno_fine) + "# " + \
                " AND ParamID IN " + paramid_str + \
                " AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"

        elif tipo_dati == 1: #NORM.           
            strSQL = f"SELECT Data, Ora, ParamID, Media, medianorm, statusnorm FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
                "# AND Data <= #" + str(giorno_fine) + "# " + \
                " AND ParamID IN " + paramid_str + \
                " AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"

        else: #NORM.O2            
            strSQL = f"SELECT Data, Ora, ParamID, Media, medianormO2, StatusnormO2 FROM Misure WHERE Data >= #" + str(giorno_inizio) + \
                "# AND Data <= #" + str(giorno_fine) + "# " + \
                " AND ParamID IN " + paramid_str + \
                " AND Ora > 0 AND Ora < 25 ORDER BY Data ASC, Ora ASC"
        pass

        cursor.execute(strSQL)

        # # Ottieni i nomi dei campi  
        column_names = []     
        column_names = [desc[0] for desc in cursor.description]
        valori = []

        # chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "Percentuale", "Status", \
        #     "medianorm", "Percnorm", "statusnorm", \
        #     "medianormO2", "PercnormO2", "StatusnormO2"]

        # Chiavi che vogliamo includere nel sotto-dizionario
        if tipo_dati == 0: #NORM.O2
            #chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianormO2", "PercnormO2", "StatusnormO2"]
            chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "Status"]

        elif tipo_dati == 1: #NORM.O2
            #chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianormO2", "PercnormO2", "StatusnormO2"]
            chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianorm", "statusnorm"]

        else: #NORM.O2
            #chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianormO2", "PercnormO2", "StatusnormO2"]
            chiavi_da_includere = ["Data", "Ora", "ParamID", "Media", "medianormO2", "StatusnormO2"]
        pass
        
        ####################################################################################
        # for row in cursor.fetchall():
        #     db_field_values = []
        #     for name, value in zip(column_names, row):
        #         db_field_values.append(value)
        #     pass
        #     # Inizializza un dizionario vuoto
        #     dictionary = {}
        #     # Usa un ciclo for per popolare il dizionario
        #     for name, value in zip(column_names, db_field_values):
        #         dictionary[name] = value               
        #     pass           
        #     # Creazione del sotto-dizionario
        #     sotto_dizionario = {chiave: dictionary[chiave] for chiave in chiavi_da_includere}
        #     valori.append(sotto_dizionario)          
        # pass       
        ####################################################################################

        ####################################################################################

        #for row in cursor.fetchall():

        # Recupera 10 righe alla volta
        batch_size = 10
        while True:
            righe = cursor.fetchmany(batch_size)
            if not righe:
                break

            for row in righe:
                db_field_values = []

                for name, value in zip(column_names, row):
                    #db_field_values.append(value)

                    if (name == "Media") or (name == "medianorm") or (name == "medianormO2") \
                            or (name == "Status") or (name == "statusnorm") or (name == "StatusnormO2"):
                        val_format = f"{value:.3f}"
                    else:
                        val_format = value
                    pass

                    db_field_values.append(val_format)
                pass

                # Inizializza un dizionario vuoto
                dictionary = {}

                # Usa un ciclo for per popolare il dizionario
                for name, value in zip(column_names, db_field_values):
                    dictionary[name] = value               
                pass
            
                # Creazione del sotto-dizionario
                sotto_dizionario = {chiave: dictionary[chiave] for chiave in chiavi_da_includere}

                valori.append(sotto_dizionario)
            pass
        pass
        
        ####################################################################################

        # Chiudi la connessione
        cursor.close()
        connection.close()

        ####################################################################################

        valori_validi = []
        for vSEZ in valoriSEZ:
            mediaSEZ = int(vSEZ["Media"])

            dataSEZ = vSEZ["Data"]
            oraSEZ = vSEZ["Ora"]

            if (mediaSEZ == 30):
                for v in valori:
                    if (v["Data"] == dataSEZ) and (v["Ora"] == oraSEZ):
                        #sotto_dizionario = {chiave: valori[chiave] for chiave in chiavi_da_includere}
                        valori_validi.append(v)
                    pass
                pass
            pass
        pass

        ####################################################################################

        return valori_validi

    except Exception as e:
        print(f"Errore durante l'accesso al database: {e}")
        return []

##########################################################################################################


def _get_db_info_and_query(database_path, giorno_inizio, giorno_fine, tipo_dati, tipo_db, vettore_paramid):
    """
    Costruisce la stringa di connessione e la query SQL in base ai parametri forniti.
    Ritorna la stringa di connessione e la query SQL.
    """
    if tipo_db == 0:
        connection_string = f"DRIVER={{Microsoft Access Driver (*.mdb)}};DBQ={database_path};"
    else:
        connection_string = f"DRIVER={{Microsoft Access Driver (*.mdb)}};DBQ={database_path};PWD=eutiFrone;"

    if tipo_dati == 0:  # TAL QUALE
        columns = "Data, Ora, ParamID, Media, Status"
    elif tipo_dati == 1:  # NORM
        columns = "Data, Ora, ParamID, Media, medianorm, statusnorm"
    else:  # NORM.O2
        columns = "Data, Ora, ParamID, Media, medianormO2, StatusnormO2"
    
    # Costruisci la stringa 'IN' per la clausola WHERE
    paramid_str = ",".join(map(str, vettore_paramid))

    strSQL = (
        f"SELECT {columns} FROM Misure WHERE "
        f"Data >= #{giorno_inizio}# AND Data <= #{giorno_fine}# "
        f"AND ParamID IN ({paramid_str}) "
        f"AND Ora > 0 AND Ora < 25 "
        f"ORDER BY Data ASC, Ora ASC, ParamID ASC"
    )

    return connection_string, strSQL


def query_medie_orarie_V2(database_path, sigla_staz, giorno_inizio, giorno_fine, code_sez, tipo_dati, vettore_paramid, tipo_db):
    """
    Ottimizzato per recuperare dati orari da un database Access
    in modo efficiente con una singola query.
    """
    valori_validi = []
    
    # Assicurati che il codice della sezione sia incluso nella lista dei parametri
    if code_sez not in vettore_paramid:
        vettore_paramid.insert(0, code_sez)

    try:
        # Step 1: Prepara la connessione e la query SQL
        connection_string, strSQL = _get_db_info_and_query(database_path, giorno_inizio, giorno_fine, tipo_dati, tipo_db, vettore_paramid)
        
        # Step 2: Connessione al database e esecuzione della query
        with pyodbc.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute(strSQL)
                column_names = [desc[0] for desc in cursor.description]
                
                # Step 3: Elabora i risultati in un'unica passata
                valori_per_ora = defaultdict(dict)
                
                for row in cursor.fetchall():
                    # Creazione del dizionario per la riga corrente
                    dictionary = dict(zip(column_names, row))
                    
                    # Raggruppa i dati per data e ora
                    data_ora_key = (dictionary["Data"], dictionary["Ora"])
                    valori_per_ora[data_ora_key][dictionary["ParamID"]] = dictionary
                
                # Step 4: Filtra i dati in base al codice di sezione
                for data_ora, params_data in valori_per_ora.items():
                    # Cerca il dizionario per il codice di sezione
                    dati_sez = params_data.get(code_sez)
                    
                    if dati_sez and int(dati_sez["Media"]) == 30:
                        # Se il codice di sezione è valido, aggiungi tutti gli altri
                        # parametri di quell'ora e data alla lista finale
                        for param_id, data in params_data.items():
                            if param_id != code_sez:
                                valori_validi.append(data)
                                print(f"Data: {data_ora[0]}, ora: {data_ora[1]}, param_id: {param_id}") # Output di debugging
                
                
    except Exception as e:
        print(f"Errore durante l'accesso al database: {e}")
        return []
    
    return valori_validi

#####################################

def query_medie_orarie_V3(
    database_path: str,
    sigla_staz: str,
    giorno_inizio,
    giorno_fine,
    code_sez: int,
    tipo_dati: int,
    vettore_paramid: List[int],
    tipo_db: int,
    debug: bool = False
) -> List[Dict[str, Any]]:
    """
    Recupera dati orari da un database Access in modo efficiente.
    """
    valori_validi: List[Dict[str, Any]] = []

    # Assicurati che il codice della sezione sia incluso
    if code_sez not in vettore_paramid:
        vettore_paramid.insert(0, code_sez)

    try:
        # Prepara connessione e query
        connection_string, strSQL = _get_db_info_and_query(
            database_path, giorno_inizio, giorno_fine, tipo_dati, tipo_db, vettore_paramid
        )

        with pyodbc.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                cursor.execute(strSQL)
                column_names = [desc[0] for desc in cursor.description]

                # Raggruppa dati per data e ora
                valori_per_ora: Dict[Tuple, Dict[int, Dict[str, Any]]] = defaultdict(dict)
                for row in cursor.fetchall():
                    record = dict(zip(column_names, row))
                    key = (record["Data"], record["Ora"])
                    valori_per_ora[key][record["ParamID"]] = record

                # Filtra dati validi in base al codice sezione
                for (data, ora), params in valori_per_ora.items():
                    dati_sez = params.get(code_sez)
                    if dati_sez and int(dati_sez.get("Media", -1)) == 30:  # Puoi adattare la condizione
                        for param_id, record in params.items():
                            if param_id != code_sez:
                                valori_validi.append(record)
                                if debug:
                                    print(f"[DEBUG] Data: {data}, Ora: {ora}, ParamID: {param_id}, Media: {record.get('Media')}")

    except Exception as e:
        print(f"Errore durante l'accesso al database: {e}")
        return []

    return valori_validi

