import psycopg2
from psycopg2 import sql, OperationalError
from datetime import datetime
import logging
import traceback
from time import sleep

import json
import requests

import ModuleTime
from ModuleTime import *
from ModuleTime import date2unix

from ModuleUtils import get_base_dir

#def verifica_connessione_db_postgres(db_ip,db_name,db_user,db_password,db_port):
def verifica_connessione_db_postgres(DB_CONFIG):
    try:
        connection = psycopg2.connect(**DB_CONFIG)

        cursor = connection.cursor()
        print ( connection.get_dsn_parameters(),"\n")

        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        return -1

    finally:
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

            return 1
        else:
            return -1

############################################################################

def leggi_dati(DB_CONFIG, db_table, paramid_list, period_sec, logger=None,
               timeout=10, retries=3, retry_delay=2):
    """
    Legge dal database l'ultimo record per ciascun paramid.
    Esegue una query per ogni paramid, identica alla query VB.NET:
      SELECT * FROM {table} WHERE {table}.paramid = {paramid}
        AND {table}.epoch >= {epoch_dbl}
        AND {table}.epoch <= {epoch_dbl_now}
        AND {table}.media != '-9999'
        AND {table}.status != -9999
        ORDER BY {table}.epoch DESC LIMIT 1;

    Restituisce i record nell'ordine specificato da paramid_list.
    """

    if not paramid_list:
        raise ValueError("Lista parametri vuota")
    if not isinstance(db_table, str) or not db_table.strip():
        raise ValueError(f"Nome tabella non valido: '{db_table}'")
    if not isinstance(period_sec, (int, float)) or period_sec < 0:
        raise ValueError(f"Periodo non valido: {period_sec}")

    if period_sec <= 0:
        period_sec = 900

    epoch_dbl_now = int((datetime.now() - datetime(2000, 1, 1)).total_seconds())
    epoch_dbl = epoch_dbl_now - period_sec

    rows = []

    attempt = 0
    while attempt < retries:
        try:
            conn = psycopg2.connect(**DB_CONFIG, connect_timeout=timeout)
            cur = conn.cursor()

            for paramid in paramid_list:
                strSQL = (
                    f"SELECT * FROM {db_table}"
                    f" WHERE {db_table}.paramid = {paramid}"
                    f" AND {db_table}.epoch >= {epoch_dbl}"
                    f" AND {db_table}.epoch <= {epoch_dbl_now}"
                    f" AND {db_table}.media != '-9999'"
                    f" AND {db_table}.status != -9999"
                    f" ORDER BY {db_table}.epoch DESC LIMIT 1;"
                )

                if logger:
                    logger.info(f"SQL: {strSQL}")

                cur.execute(strSQL)
                row = cur.fetchone()
                if row is not None:
                    rows.append(row)

            cur.close()
            conn.close()
            return rows

        except (OperationalError, psycopg2.DatabaseError) as e:
            attempt += 1
            tb = traceback.format_exc()
            msg = f"Tentativo {attempt}/{retries} - Errore DB '{db_table}': {e}\n{tb}"
            if logger:
                logger.error(msg)
            else:
                print(msg)
            if attempt < retries:
                sleep(retry_delay)
            else:
                return []

        except Exception as e:
            tb = traceback.format_exc()
            msg = f"Errore inatteso nella lettura DB '{db_table}': {e}\n{tb}"
            if logger:
                logger.error(msg)
            else:
                print(msg)
            return []

############################################################################

def leggi_dati_V0(DB_CONFIG, db_table, staz_name, paramid_list, period_sec):
    try:
        n_param = len(paramid_list)
        paramid_string = "(" + ",".join(str(x) for x in paramid_list) + ")"

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        epoch_dbl_now = date2unix(datetime.now())
        epoch_dbl = date2unix(datetime.now()) - period_sec

        placeholders = ','.join(['%s'] * len(paramid_list))

        strSQL = f"""
            SELECT * FROM {db_table}
            WHERE {db_table}.paramid IN ({placeholders})
              AND {db_table}.epoch >= %s
            ORDER BY epoch DESC
            LIMIT %s
        """

        params = paramid_list + [epoch_dbl, n_param]

        cur.execute(strSQL, params)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows

    except Exception as e:
        print(f"Errore durante la lettura dal database: {e}")
        return []

############################################################################

def leggi_dati_V1(DB_CONFIG, db_table, staz_name, paramid_list, period_sec):
    try:
        n_param = len(paramid_list)
        paramid_string = "(" + ",".join(str(x) for x in paramid_list) + ")"

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        epoch_dbl_now = date2unix(datetime.now())
        epoch_dbl = date2unix(datetime.now()) - period_sec

        placeholders = ','.join(['%s'] * len(paramid_list))

        strSQL = f"""
            SELECT * FROM {db_table}
            WHERE {db_table}.paramid IN ({placeholders})
              AND {db_table}.epoch >= %s
            ORDER BY epoch DESC
            LIMIT %s
        """

        params = paramid_list + [epoch_dbl, n_param]

        cur.execute(strSQL, params)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows

    except Exception as e:
        print(f"Errore durante la lettura dal database: {e}")
        return []