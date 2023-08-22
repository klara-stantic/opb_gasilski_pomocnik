# Jedro aplikacije
import psycopg2
# podatki za dostop do postgreSQL baze
from auth import *

conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)

# Ostale potrebne knjižnjice
import pandas as pd
from dataclasses import dataclass, field, asdict
from dataclasses_json import dataclass_json
from datetime import date

#POZOR! @dataclass sam ustvari __init__


###############################################################################
# ČLANI
###############################################################################

@dataclass_json
@dataclass
class Clan:
    emso: int 
    ime: str 
    priimek: str 
    funkcija: int
    cin: int
    zdravniski: date = field(metadata={"format": "date"})

    def __str__(self):
        return f"Član {self.ime} {self.priimek}"
        
    # Metoda, s katero preko emsota dostopamo do clanov
    @classmethod
    def get_clan(cls, emso):
        # Povezava z bazo
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        query = f"SELECT * FROM clan WHERE emso = {emso};"
        cursor.execute(query)
        fetched_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if fetched_data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, fetched_data))
            return cls(**data_dict)
        else:
            print("Takega člana žal ne najdem!")
            return None
        
    # POZOR! To ne dela z dekoratorji @staticmethod ali @classmethod
    def dodaj_clana_v_bazo(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        #SQL podatki
        sql_niz = "INSERT INTO clan (emso, ime, priimek, funkcija, cin, zdravniski) VALUES (%s, %s, %s, %s,%s,%s);"
        values = (self.emso, self.ime, self.priimek, self.funkcija, self.cin, self.zdravniski)
        
        try:
            cur.execute(sql_niz, values)
            baza.commit()
            cur.close()
            baza.close()
            return "Shranjeno"
            
        except ValueError:
            cur.close()
            baza.close()
            return "Napaka"
            
    def odstrani_clana(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()

        sql_niz = f"DELETE FROM clan WHERE emso = {self.emso}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()

    def popravi_clana(self, novo_ime=None, nov_priimek=None, nova_funkcija=None, nov_cin=None, nov_zd=None):
        # Filter
        if not novo_ime and not nov_cin and not nov_priimek and not nov_zd and not nova_funkcija:
            return "Ni zahtevanih sprememb. Član se ni spremenil."
        
        # Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        sql_niz = "UPDATE clan SET"
        values = []

        if novo_ime:
            sql_niz += " ime = %s,"
            values.append(novo_ime)
        
        if nov_priimek:
            sql_niz += " priimek = %s,"
            values.append(nov_priimek)
            
        if nova_funkcija:
            sql_niz += " funkcija = %s,"
            values.append(nova_funkcija)
            
        if nov_cin:
            sql_niz += " cin = %s,"
            values.append(nov_cin)
            
        if nov_zd:
            sql_niz += " zdravniski = %s,"
            values.append(nov_zd)

        sql_niz = sql_niz.rstrip(',') + " WHERE emso = %s;"
        values.append(self.emso)

        cur.execute(sql_niz, tuple(values))
        print(f"Popravljen član z emšo: {self.emso}")
    
        baza.commit()
        cur.close()
        baza.close()


###############################################################################
# INTERVENCIJE
###############################################################################

@dataclass_json
@dataclass
class Intervencija:
    id: int
    opis: str 
    datum: date = field(metadata={"format": "date"})
    tip = int

    def __str__(self):
        return f"Intervencija ({self.tip}) dne {self.datum} z opisom: {self.opis}"
        
    @classmethod
    def dodaj_intervencijo_v_bazo(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        #SQL podatki
        sql_niz = "INSERT INTO intervencija (opis,datum,tip) VALUES (%s, %s, %s);"
        values = (self.opis, self.datum, self.tip)
        
        try:
            cur.execute(sql_niz, values)
            baza.commit()
            cur.close()
            baza.close()
            return "Shranjeno"
            
        except ValueError:
            cur.close()
            baza.close()
            return "Napaka"
            
    @staticmethod
    def odstrani_intervencijo(id: int):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()

        sql_niz = f"DELETE FROM intervencija WHERE id = {id}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()

    @staticmethod
    def popravi_intervencijo(id: int, nov_opis=None, nov_datum=None, nov_tip=None):
        # Filter
        if not nov_opis and not nov_datum and not nov_tip:
            return "Ni zahtevanih sprememb. Intervencija se ni spremenila."
        
        # Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        sql_niz = "UPDATE intervencija SET"
        values = []

        if nov_opis:
            sql_niz += " ime = %s,"
            values.append(nov_opis)
        
        if nov_datum:
            sql_niz += " priimek = %s,"
            values.append(nov_datum)
            
        if nov_tip:
            sql_niz += " funkcija = %s,"
            values.append(nov_tip)

        sql_niz = sql_niz.rstrip(',') + " WHERE id = %s;"
        values.append(id)

        cur.execute(sql_niz, tuple(values))
    
        baza.commit()
        cur.close()
        baza.close()

###############################################################################
# VOZILA
###############################################################################



###############################################################################
# VAJE
###############################################################################



###############################################################################
# TEKMOVANJA
###############################################################################


