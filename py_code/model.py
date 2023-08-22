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

# TINE
class Clan:
    def __init__(self, emso, ime, priimek, funkcija, cin,zdravniski):
        self.emso = emso
        self.ime = ime
        self.priimek = priimek
        self.funkcija = funkcija
        self.cin = cin
        self.zdravniski = zdravniski

    def __str__(self):
        return f"Član {self.ime} {self.priimek}"

    
    def dodaj_clana(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO clan (emso, ime, priimek, funkcija,cin,zdravniski) VALUES (%s, %s, %s, %s,%s,%s);"
                cur.execute(sql_niz, (self.emso, self.ime, self.priimek, self.funkcija,self.cin,self.zdravniski))
                return "Shranjeno"
            except ValueError:
                return "Napaka"
            
    @staticmethod
    def odstrani_clana(emso):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = f"DELETE FROM clan WHERE emso = {emso}"
            cur.execute(sql_niz)

    @staticmethod
    def popravi_clana(emso,ime,priimek,funkcija,cin,zd):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = f"UPDATE clan SET emso = {emso},ime = '{ime}',priimek='{priimek}',funkcija={funkcija},cin={cin},zdravniski='{zd}' WHERE emso = {emso}"
            cur.execute(sql_niz)
# KLARA
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
    def dodaj_clana(self):
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

# TINE
class Vozila:
    def __init__(self, registerska_st, tip_vozila, potreben_izpit, st_potnikov,znamka,tehnicni):
            self.registerska_st = registerska_st
            self.tip_vozila = tip_vozila
            self.potreben_izpit = potreben_izpit
            self.st_potnikov = st_potnikov
            self.znamka = znamka
            self.tehnicni = tehnicni
#KLARA
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
    
# TINE
    def dodaj_vozilo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO vozilo (registrska_st, tip_vozila, potreben_izpit, st_potnikov,znamka,tehnicni) VALUES (%s, %s, %s, %s, %s, %s);"
                cur.execute(sql_niz, (self.registerska_st, self.tip_vozila, self.potreben_izpit, self.st_potnikov,self.znamka,self.tehnicni))
                return "Shranjeno"
            except ValueError:
                return "Napaka"

    @staticmethod
    def odstrani_vozilo(reg):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM vozilo WHERE registrska_st = %s"
            cur.execute(sql_niz,[reg])
    @staticmethod
    def popravi_vozilo(reg,tip,izpit,potniki,znamka,tehnicni):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = f"UPDATE vozilo  SET registrska_st  = '{reg}',tip_vozila = {tip},potreben_izpit={izpit},st_potnikov={potniki},znamka='{znamka}',tehnicni='{tehnicni}' WHERE registrska_st  = '{reg}'"
            cur.execute(sql_niz)
# KLARA
        baza.commit()
        cur.close()
        baza.close()

###############################################################################
# INTERVENCIJE
###############################################################################

# TINE
### prvotno sa mislia dodat še kraj ma ni pa nič kritičnega če to spustimo in je kako to itak v opisu
class Intervencije:
    def __init__(self, opis, datum, tip):
        self.opis = opis
        self.datum = datum
        self.tip = tip

    def __str__(self):
        niz = f"Intervencija tipa {self.tip} dne {self.datum} z opisom: {self.opis}"
        return niz

    def dodaj_intervencijo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO intervencija (opis,datum,tip) VALUES (%s, %s, %s);"
                cur.execute(sql_niz, (self.opis, self.datum, self.tip))
                ## ko dadoamo intervencijo bi mogli potem pot self.id skranit id intervencija
                ## ker jo potem potrebujemo za izpris ali bilo kaj
                ### filter če intevencija ze obstaja
                sql_niz_za_id =  "SELECT id FROM intervencija"
                id = cur.execute( sql_niz_za_id)
                id = cur.fetchall()[0]
                self.id = id
                return "Shranjeno"
            except ValueError:
                return "Napaka"
    @staticmethod
    def dodaj_clana_intervenciji(id_intervencije_za_dodat_clane,emso_clan_na_intervenciji):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz_za_dodajanje_posameznega_clana = "INSERT into prisotnost_na_intervencijah ( id_intervencije,emso_prisotnega) VALUES (%s, %s)"
                cur.execute(sql_niz_za_dodajanje_posameznega_clana,(id_intervencije_za_dodat_clane,emso_clan_na_intervenciji))
                return "Shranjeno"
            except ValueError:
                return "Napaka"
            
    @staticmethod
    def dodaj_vozilo_intervenciji(id_intervencije_za_dodat_vozilo,reg_vozila_na_intervenciji):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz_za_dodajanje_posameznega_vozila = "INSERT into vozila_na_intervencijah (id_intervencije,registracija_vozila) VALUES (%s, %s)"
                cur.execute(sql_niz_za_dodajanje_posameznega_vozila,(id_intervencije_za_dodat_vozilo,reg_vozila_na_intervenciji))
                return "Shranjeno"
            except ValueError:
                return "Napaka"
    @staticmethod
    def odstrani_intervencijo(id):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            cur.execute(f"DELETE FROM prisotnost_na_intervencijah WHERE id_intervencije = {id}")
            cur.execute(f"DELETE FROM vozila_na_intervencijah WHERE id_intervencije = {id}")
            sql_niz = f"DELETE FROM intervencija WHERE id = {id}"
            cur.execute(sql_niz)

class Vaja:
    def __init__(self,datum,obvezna,tip_vaje,vodja):
        self.datum = datum
        self.obvezna = obvezna
        self.tip_vaje = tip_vaje
        self.vodja = vodja

    def __str__(self):
        niz = f"vaja tipa {self.tip_vaje} dne {self.datum}, ki jo vodi: {self.vodja}"
        return niz

    def dodaj_vajo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO vaja (datum,obvezna,tip_vaje,vodja) VALUES (%s, %s, %s,%s);"
                cur.execute(sql_niz, ( self.datum,self.obvezna,self.tip_vaje,self.vodja))
                ## ko dadoamo vajo bi mogli potem pot self.id shranit id vaje
                ## ker jo potem potrebujemo za izpris ali bilo kaj
                return "Shranjeno"
            except ValueError:
                return "Napaka"
            
    def odstrani_vajo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM intervencija WHERE id = {self.id}"
            cur.execute(sql_niz)    

class Tekomvanje:
    def __init__(self,datum,lokacija,tip_tekmovanja):
        self.datum = datum
        self.lokacija = lokacija
        self.tip_tekomvanja = tip_tekmovanja

    def __str__(self):
        niz = f"tekomvanje tipa {self.tip_tekomvanja} dne {self.datum} v  {self.lokacija}"
        return niz

    def dodaj_tekmovanje(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO tekmovanje (datum,lokacija,tip_tekmovanja) VALUES (%s, %s, %s);"
                cur.execute(sql_niz, ( self.datum,self.lokacija, self.tip_tekomvanja))
                ## ko dadoamo tekmovanja bi mogli potem pot self.id shranit id tekomvanja
                ## ker jo potem potrebujemo za izpris ali bilo kaj
                sql_niz_za_id =  "SELECT id FROM tekmovanje"
                id = cur.execute( sql_niz_za_id)
                id = cur.fetchall()[0]
                self.id = id
                return "Shranjeno"
            except ValueError:
                return "Napaka"
            
    @staticmethod        
    def odstrani_tekmovanje(id):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = f"DELETE FROM tekmovanje WHERE id = {id}"
            cur.execute(sql_niz)
    



# KLARA
@dataclass_json
@dataclass
class Intervencija:
    id: int= field(init=False) # Ker ga baza generira sama!
    opis: str 
    datum: date = field(metadata={"format": "date"})
    tip: int

    def __str__(self):
        return f"Intervencija ({self.tip}) dne {self.datum} z opisom: {self.opis}"
        
    # Metoda, s katero preko id dostopamo do intervencij
    @classmethod
    def get_intervencija(cls, id):
        # Povezava z bazo
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        query = f"SELECT * FROM intervencija WHERE id = {id};"
        cursor.execute(query)
        fetched_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if fetched_data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, fetched_data))
            return cls(**data_dict)
        else:
            print("Take intervencije žal ne najdem!")
            return None
        
    # POZOR! To ne dela z dekoratorji @staticmethod ali @classmethod
    def dodaj_intervencijo(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        #SQL podatki
        sql_niz = "INSERT INTO intervencija (opis,datum,tip) VALUES (%s, %s, %s);"
        values = (self.opis, self.datum, self.tip)
        
        try:
            cur.execute(sql_niz, values)
            # Pridobiti želimo ustvarjen id!
            cur.execute("SELECT currval(pg_get_serial_sequence('intervencija', 'id'));")
            generated_id = cur.fetchone()[0]  # Generiran id
            self.id = generated_id # Shranimo id
            baza.commit()
            cur.close()
            baza.close()
            return "Shranjeno"
            
        except ValueError:
            cur.close()
            baza.close()
            return "Napaka"
            
    def odstrani_intervencijo(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()

        sql_niz = f"DELETE FROM intervencija WHERE id = {self.id}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()

    def popravi_intervencijo(self, nov_opis=None, nov_datum=None, nov_tip=None):
        # Filter
        if not nov_opis and not nov_datum and not nov_tip:
            return "Ni zahtevanih sprememb. Član se ni spremenil."
        
        # Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        sql_niz = "UPDATE clan SET"
        values = []

        if nov_opis:
            sql_niz += " opis = %s,"
            values.append(nov_opis)
        
        if nov_tip:
            sql_niz += " tip = %s,"
            values.append(nov_tip)
            
        if nov_datum:
            sql_niz += " datum = %s,"
            values.append(nov_datum)

        sql_niz = sql_niz.rstrip(',') + " WHERE id = %s;"
        values.append(self.id)

        cur.execute(sql_niz, tuple(values))
        print(f"Popravljena intervencija z id: {self.id}")
    
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


