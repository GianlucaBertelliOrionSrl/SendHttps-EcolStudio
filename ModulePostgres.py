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
from ModuleTime import date2unix  # importa la tua funzione di conversione epoch

from ModuleUtils import get_base_dir

#def verifica_connessione_db_postgres(db_ip,db_name,db_user,db_password,db_port):
def verifica_connessione_db_postgres(DB_CONFIG):
	try:
		# connection = psycopg2.connect(user = db_user,
		#     password = db_password,host = db_ip,
		#     port = db_port,database = db_name)

		connection = psycopg2.connect(**DB_CONFIG)

		cursor = connection.cursor()
		# Print PostgreSQL Connection properties
		print ( connection.get_dsn_parameters(),"\n")

		# Print PostgreSQL version
		cursor.execute("SELECT version();")
		record = cursor.fetchone()
		print("You are connected to - ", record,"\n")

	except (Exception, psycopg2.Error) as error :
		print ("Error while connecting to PostgreSQL", error)
		return -1

	finally:
		#closing database connection.
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
    Legge dal database l'ultimo record per ciascun paramid, in modo sicuro e resiliente.
    Restituisce i record nell'ordine specificato da paramid_list.

    Parametri:
      DB_CONFIG     : dict con host, dbname, user, password, ecc.
      db_table      : nome tabella, eventualmente con schema (es. "averages.avg_60s_01492")
      paramid_list  : lista di paramid da filtrare (numeri interi)
      period_sec    : periodo in secondi da sottrarre all'ora corrente
      logger        : logger opzionale per loggare errori e debug
      timeout       : tempo massimo in secondi per connessione ed esecuzione query
      retries       : numero di tentativi su errori di connessione
      retry_delay   : secondi da attendere prima del retry

    Restituisce:
      Lista di tuple (record)
    """

    # --- Validazioni preliminari ---
    if not paramid_list:
        raise ValueError("Lista parametri vuota")
    if not isinstance(db_table, str) or not db_table.strip():
        raise ValueError(f"Nome tabella non valido: '{db_table}'")
    if not isinstance(period_sec, (int, float)) or period_sec < 0:
        raise ValueError(f"Periodo non valido: {period_sec}")
    if not all(isinstance(p, int) for p in paramid_list):
        raise ValueError("Tutti i paramid devono essere interi")

    # --- Calcolo epoch limite ---
    epoch_start = date2unix(datetime.now()) - period_sec

    # --- Gestione schema e tabella ---
    if '.' in db_table:
        schema_name, table_name = db_table.split('.', 1)
        table_sql = sql.Identifier(schema_name) + sql.SQL('.') + sql.Identifier(table_name)
    else:
        table_sql = sql.Identifier(db_table)

    # --- Costruzione query sicura ---
    placeholders = sql.SQL(',').join(sql.Placeholder() * len(paramid_list))
    # Array per ordine personalizzato
    order_array = sql.SQL(',').join(sql.Literal(p) for p in paramid_list)

    query = sql.SQL("""
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (PARTITION BY paramid ORDER BY epoch DESC) AS rn
            FROM {table}
            WHERE paramid IN ({params})
              AND epoch >= %s
        ) sub
        WHERE rn = 1
        ORDER BY ARRAY_POSITION(ARRAY[{order_list}], paramid);
    """).format(
        table=table_sql,
        params=placeholders,
        order_list=order_array
    )

    params = paramid_list + [epoch_start]

    if logger:
        logger.debug(f"Eseguo query su '{db_table}' per paramid: {paramid_list} a partire da epoch {epoch_start}")

    # --- Retry loop ---
    attempt = 0
    while attempt < retries:
        try:
            with psycopg2.connect(**DB_CONFIG, connect_timeout=timeout) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    rows = cur.fetchall()
            return rows

        except (OperationalError, psycopg2.DatabaseError) as e:
            attempt += 1
            tb = traceback.format_exc()
            msg = f"❌ Tentativo {attempt}/{retries} - Errore DB '{db_table}': {e}\n{tb}"
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
            msg = f"❌ Errore inatteso nella lettura DB '{db_table}': {e}\n{tb}"
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

		#s = "SELECT * FROM " & table & " WHERE " & staz_name & ".data >= '" & FromDate & "' AND " &
		#   table & ".data <= '" & ToDate & "' AND " & table & ".paramid IN (" & ParametriSel & ");"


		epoch_dbl_now = date2unix(datetime.now())
		epoch_dbl = date2unix(datetime.now()) - period_sec

		# # strSQL = (
		# #     f"SELECT * FROM {db_table} "
		# #     f"WHERE {db_table}.paramid IN {paramid_string} "
		# #     f"AND {db_table}.epoch >= {epoch_dbl} "
		# #     f"ORDER BY epoch DESC LIMIT {n_param}"
		# # )

		# strSQL = (
		#     "SELECT * FROM {table} "
		#     "WHERE {table}.paramid IN {paramid} "
		#     "AND {table}.epoch >= {epoch} "
		#     "ORDER BY epoch DESC LIMIT {limit}"
		# ).format(
		#     table=db_table,
		#     paramid=paramid_string,
		#     epoch=epoch_dbl,
		#     limit=n_param
		# )
		# cur.execute(strSQL)


		#"SELECT * FROM averages.avg_60s_01479 WHERE averages.avg_60s_01479.paramid = 1 
		# AND averages.avg_60s_01479.epoch >= 811597916 AND averages.avg_60s_01479.epoch <= 813397916
		# AND averages.avg_60s_01479.media != '-9999' AND averages.avg_60s_01479.status != -9999
		# ORDER BY averages.avg_60s_01479.epoch DESC LIMIT 1;"

		placeholders = ','.join(['%s'] * len(paramid_list))

		strSQL = f"""
			SELECT * FROM {db_table}
			WHERE {db_table}.paramid IN ({placeholders})
			  AND {db_table}.epoch >= %s
			ORDER BY epoch DESC
			LIMIT %s
		"""

		# --- Parametri da passare alla query ---
		params = paramid_list + [epoch_dbl, n_param]

		# --- Esecuzione query ---
		cur.execute(strSQL, params)

		rows = cur.fetchall()
		cur.close()
		conn.close()

		return rows

	except Exception as e:
		print(f"❌ Errore durante la lettura dal database: {e}")
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

		# --- Parametri da passare alla query ---
		params = paramid_list + [epoch_dbl, n_param]

		# --- Esecuzione query ---
		cur.execute(strSQL, params)

		rows = cur.fetchall()
		cur.close()
		conn.close()

		return rows

	except Exception as e:
		print(f"❌ Errore durante la lettura dal database: {e}")
		return []