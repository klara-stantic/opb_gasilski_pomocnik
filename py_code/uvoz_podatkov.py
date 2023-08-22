# Koda za uvoz podatkov in delo z bazo

# priprava knjižnjic
import psycopg2
import csv

# datoteka za bazo
baza_filename="gasilcitest.db"

# podatki za dostop do postgreSQL baze
from auth import *

conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)

# uvoz podatkov iz sql
def uvoziSQL(cur, datoteka):
    '''Funkcija za uvoz podatkov iz SQL datoteke'''
    with open(datoteka) as file:
        koda = file.read()
        cur.execute(koda)

# uvoz podatkov iz csv
def uvoziCSV(cur, tabela):
    '''Funkcija za uvoz podatkov iz CSV datoteke v tabelo z istim imenom'''
    with open("podatki/{0}.csv".format(tabela), encoding="utf8") as csvfile:
        vsebina = csv.reader(csvfile)
        all_data = [vrstica for vrstica in vsebina]
        glava = all_data[0]
        podatki = all_data[1:]
        cur.executemany("INSERT INTO {0} ({1}) VALUES ({2})".format(tabela, " , ".join(glava), " , ".join(["%s"]*len(glava))), podatki)
        
# Glavna funkcija za uvoz podatkov iz SQL in CSV datotek
with psycopg2.connect(conn_string) as baza:
    cur = baza.cursor()
    cur.execute("DROP TABLE IF EXISTS opravljeni_tecaji, del_ekipe, prisotnost_na_intervencijah, prisotnost_na_vajah, vozila_na_intervencijah, ekipe_na_tekmovanjih, lastnistva_opreme, oprema_v_vozilih, skrbnik_vozila, potrebuje_tecaj CASCADE")
    cur.execute("DROP TABLE IF EXISTS osebna_oprema, skupna_oprema, ekipa, tekmovanje, tehnicni_pregledi_vozil, clan, vaja, intervencija, vozilo, tecaj CASCADE")
    cur.execute("DROP TABLE IF EXISTS funkcija, cin, kategorija_vozniskega_dovoljenja, tip_vozila, tip_intervencije, tip_tecaja, tip_tekmovanja CASCADE")
    uvoziSQL(cur, "sql_code/osnovnetabele.sql")
    uvoziSQL(cur, "sql_code/relacije1.sql")
    csv_datoteke = ["cin", "funkcija", "kategorija_vozniskega_dovoljenja", "tip_intervencije", "tip_tecaja", "tip_tekmovanja", "tip_vozila"]
    for ime in csv_datoteke:
        uvoziCSV(cur, ime)

#delo z bazo 
#with psycopg2.connect(conn_string) as con:
#    cur = con.cursor()