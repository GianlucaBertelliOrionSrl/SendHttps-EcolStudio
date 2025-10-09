import pyodbc
import os, sys
from win32com.client import Dispatch

import ModuleFunctions
from ModuleFunctions import *

abspath = os.path.dirname(os.path.realpath(sys.argv[0]))

########################################

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

##############################################

class ClassStationParamConfig:
    def __init__(self, station_configurations=None, param_configurations=None):
        self.station_configurations = station_configurations if station_configurations is not None else []
        self.param_configurations = param_configurations if param_configurations is not None else []

    def add_param_config(self, param):
        self.param_configurations.append(param)

    def add_station_config(self, config):
        self.station_configurations.append(config)

    def display_attributes0(self):
        # Visualizza i parametri di configurazione
        #print("Parametri di configurazione:")
        for param in self.param_configurations:
            print(param)

        # Visualizza le altre configurazioni
        #print("\nAltre configurazioni:")
        for config in self.station_configurations:
            print(config)
    
    def display_attributes(self):
        # Usa vars() per ottenere un dizionario degli attributi
        attributi = vars(self)
        #print(attributi)

        # Stampa ciascun attributo e valore
        for chiave, valore in attributi.items():
            print(f"{chiave}: {valore}")
        pass

    def display_all_vars(self):
        # Visualizza tutti i nomi e i valori delle variabili della classe principale
        print("\nVariabili della classe MainConfig:")

        for key, value in vars(self).items():
            if isinstance(value, list):
                print(f'{key}:')
                for item in value:
                    print(f'  {item}')
            else:
                print(f'{key}: {value}')
            pass
        pass

##############################################

class ClassConfigContainer:
    def __init__(self):
        self.station_configurations = []

    def add_configuration(self, config):
        self.station_configurations.append(config)

    def __str__(self):
        return "\n".join(str(config) for config in self.station_configurations)

    def display_attributes0(self):
        # Visualizza i parametri di configurazione
       # print("Parametri di configurazione:")
        for param in self.param_configurations:
            print(param)

        # Visualizza le altre configurazioni
        #print("\nAltre configurazioni:")
        for config in self.station_configurations:
            print(config)
        pass

    def display_all_vars0(self):
        # Visualizza tutti i nomi e i valori delle variabili della classe principale
        #print("\nVariabili della classe MainConfig:")

        for key, value in vars(self).items():
            if isinstance(value, list):
                print(f'{key}:')
                for item in value:
                    print(f'  {item}')
            else:
                print(f'{key}: {value}')
            pass
        pass

    def display_attributes(self):
        # Usa vars() per ottenere un dizionario degli attributi
        attributi = vars(self)
        #print(attributi)

        # Stampa ciascun attributo e valore
        for chiave, valore in attributi.items():
            print(f"{chiave}: {valore}")
        pass

#############################################

class MainConfig:
    def __init__(self):
        self.config_containers = []

    def add_config_container(self, container):
        self.config_containers.append(container)

    def __str__(self):
        return "\n\n".join(str(container) for container in self.config_containers)

    def display_attributes(self):
        # Usa vars() per ottenere un dizionario degli attributi
        attributi = vars(self)
        #print(attributi)

        # Stampa ciascun attributo e valore
        for chiave, valore in attributi.items():
            print(f"{chiave}: {valore}")
        pass

    def display_attributes0(self):
        # Visualizza i parametri di configurazione
       # print("Parametri di configurazione:")
        for param in self.param_configurations:
            print(param)

        # Visualizza le altre configurazioni
        #print("\nAltre configurazioni:")
        for config in self.station_configurations:
            print(config)
        pass

    def display_all_vars0(self):
        # Visualizza tutti i nomi e i valori delle variabili della classe principale
        #print("\nVariabili della classe MainConfig:")

        for key, value in vars(self).items():
            if isinstance(value, list):
                print(f'{key}:')
                for item in value:
                    print(f'  {item}')
            else:
                print(f'{key}: {value}')
            pass
        pass

##############################################

