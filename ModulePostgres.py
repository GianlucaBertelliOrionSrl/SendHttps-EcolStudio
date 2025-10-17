import psycopg2
import json
import requests
import time

import ModuleTime
from ModuleTime import *

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

def leggi_dati(DB_CONFIG, db_table, staz_name, paramid_list, period_sec):
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