import psycopg2
import json
import requests

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
            return None

def leggi_dati(DB_CONFIG, db_table):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # # Modifica la query secondo le tue colonne reali
        # cur.execute("""
        #     SELECT time, version, voc, c6h6, h2s, pid
        #     FROM avg_60s_10479
        #     ORDER BY time DESC
        #     LIMIT 10
        # """)
       
        strSQL = f"SELECT * FROM {db_table} ORDER BY epoch DESC LIMIT 10"

        # cur.execute("""
        #     SELECT time, version, voc, c6h6, h2s, pid
        #     FROM {%}
        #     ORDER BY time DESC
        #     LIMIT 10
        # """)

        cur.execute(strSQL)

        dati = cur.fetchall()
        cur.close()
        conn.close()

        return dati

    except Exception as e:
        print(f"❌ Errore durante la lettura dal database: {e}")
        return []