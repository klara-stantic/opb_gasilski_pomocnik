# Jedro aplikacije
import psycopg2
# podatki za dostop do postgreSQL baze
from auth import *

conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)

# Ostale potrebne knjižnjice
#import pandas as pd
from dataclasses import dataclass, field #, asdict
from dataclasses_json import dataclass_json
from datetime import date


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
    zdravniski: date = field(metadata={"format": "date"}, default=None)
    aktiven: bool = field(default=True)

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
            print("Takega člana ne najdem!")
            return None
    
    # TO SAMO SPREMENI AKTIVNOST
    # Ob priliki je treba nardit dve loceni funkciji za pretvorbo IN uskladit zs spletnim vmesnikom
    @staticmethod
    def spremeni_aktivnost(emso):
        # Poisci clana
        clan = Clan.get_clan(emso)
        
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        bool = not clan.aktiven

        sql_niz = f"UPDATE clan SET aktiven= {bool} WHERE emso = {clan.emso}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()
    
    @staticmethod
    def popravi_clana(emso, novo_ime, nov_priimek, nova_funkcija, nov_cin, nov_zd=None):
        # Poisci clana
        clan = Clan.get_clan(emso)
        
        # Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        sql_niz = "UPDATE clan SET ime = %s, priimek = %s, funkcija = %s, cin = %s,"
        values = [novo_ime, nov_priimek, nova_funkcija, nov_cin]
            
        if nov_zd:
            sql_niz += " zdravniski = %s,"
            values.append(nov_zd)

        sql_niz = sql_niz.rstrip(',') + " WHERE emso = %s;"
        values.append(clan.emso)

        cur.execute(sql_niz, tuple(values))
        print(f"Popravljen član z emšo: {clan.emso}")

        baza.commit()
        cur.close()
        baza.close()
    
    # POZOR! To ne dela z dekoratorji @staticmethod ali @classmethod
    def dodaj_clana(self):
        # Poisci clana
        clan = Clan.get_clan(self.emso)
        
        if clan:
            clan.spremeni_aktivnost(self.emso)
            clan.popravi_clana(self.emso, novo_ime=self.ime, nov_priimek=self.priimek, nova_funkcija=self.funkcija, nov_cin=self.cin, nov_zd=self.zdravniski)
            return "Ta član že obstaja"
        
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        if self.zdravniski:        
        #SQL podatki
            sql_niz = "INSERT INTO clan (emso, ime, priimek, funkcija, cin, zdravniski) VALUES (%s, %s, %s, %s,%s,%s);"
            values = (self.emso, self.ime, self.priimek, self.funkcija, self.cin, self.zdravniski)
        else:
            sql_niz = "INSERT INTO clan (emso, ime, priimek, funkcija, cin) VALUES (%s, %s, %s, %s,%s);"
            values = (self.emso, self.ime, self.priimek, self.funkcija, self.cin)
        
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
            
    # Te načeloma ne rabiva
    #def odstrani_clana(self):
    #    #Ustvarjanje povezave
    #    baza = psycopg2.connect(conn_string)
    #    cur = baza.cursor()

    #    sql_niz = f"DELETE FROM clan WHERE emso = {self.emso}"
    #    cur.execute(sql_niz)
    
    #    baza.commit()
    #    cur.close()
    #    baza.close()

###############################################################################
# VOZILA
###############################################################################

@dataclass_json
@dataclass
class Vozilo:
    registrska_st: str 
    tip_vozila: int 
    potreben_izpit: int 
    st_potnikov: int
    znamka: str
    tehnicni: date = field(metadata={"format": "date"}, default=None)
    aktivno: bool = field(default=True)

    def __str__(self):
        return f"Vozilo {self.registrska_st} znamke {self.znamka}"
        
    # Metoda, s katero preko emsota dostopamo do clanov
    @classmethod
    def get_vozilo(cls, registrska_st):
        # Povezava z bazo
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        query = f"SELECT * FROM vozilo WHERE registrska_st = '{registrska_st}';"
        cursor.execute(query)
        fetched_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if fetched_data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, fetched_data))
            return cls(**data_dict)
        else:
            print("Takega vozila ne najdem!")
            return None
    
    @staticmethod
    def spremeni_aktivnost(registrska_st):
        # Poisci vozilo
        vozilo = Vozilo.get_vozilo(registrska_st)
        
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        bool_niz = not vozilo.aktivno

        sql_niz = f"UPDATE vozilo SET aktivno = {bool_niz} WHERE registrska_st = '{registrska_st}';"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()
      
    @staticmethod
    def popravi_vozilo(registrska_st, nov_tip, nov_potreben_izpit, novo_st_potnikov, nova_znamka, nov_tehnicni=None):
        # Poisci vozilo
        vozilo = Vozilo.get_vozilo(registrska_st)
        
        # Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        sql_niz = "UPDATE vozilo SET tip_vozila = %s, potreben_izpit = %s, st_potnikov = %s, znamka = %s,"
        values = [nov_tip, nov_potreben_izpit, novo_st_potnikov, nova_znamka]
            
        if nov_tehnicni:
            sql_niz += " tehnicni = %s,"
            values.append(nov_tehnicni)

        sql_niz = sql_niz.rstrip(',') + " WHERE registrska_st = %s;"
        values.append(vozilo.registrska_st)

        cur.execute(sql_niz, tuple(values))
        print(f"Popravljeno vozilo z registrsko: {vozilo.registrska_st}")

        baza.commit()
        cur.close()
        baza.close()
    
    # POZOR! To ne dela z dekoratorji @staticmethod ali @classmethod
    def dodaj_vozilo(self):
        # Poisci vozilo
        vozilo = Vozilo.get_vozilo(self.registrska_st)
        
        if vozilo:
            vozilo.spremeni_aktivnost(self.registrska_st)
            vozilo.popravi_vozilo(self.registrska_st, nov_tip=self.tip_vozila, nov_potreben_izpit=self.potreben_izpit, novi_potniki=self.st_potnikov, nova_znamka=self.znamka, nov_tehnicni=self.tehnicni)
            return "To vozilo že obstaja"
        
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
        if self.tehnicni == "":        
        #SQL podatki
            sql_niz = "INSERT INTO vozilo (registrska_st, tip_vozila, potreben_izpit, st_potnikov, znamka, tehnicni) VALUES (%s, %s, %s, %s,%s,%s);"
            values = (self.registrska_st, self.tip_vozila, self.potreben_izpit, self.st_potnikov, self.znamka, None)
        else:
            sql_niz = "INSERT INTO vozilo (registrska_st, tip_vozila, potreben_izpit, st_potnikov, znamka, tehnicni) VALUES (%s, %s, %s, %s,%s, %s);"
            values = (self.registrska_st, self.tip_vozila, self.potreben_izpit, self.st_potnikov, self.znamka, self.tehnicni)
        
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


###############################################################################
# INTERVENCIJE
###############################################################################

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
        

    ####### mogoče bi blo za ločit sql stavke alpa jih dodelat zaradi pravilnosti.
    @staticmethod        
    def odstrani_intervencijo(id):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        cur.execute(f"DELETE FROM prisotnost_na_intervencijah WHERE id_intervencije = {id}")
        cur.execute(f"DELETE FROM vozila_na_intervencijah WHERE id_intervencije = {id}")
        sql_niz = f"DELETE FROM intervencija WHERE id = {id}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()
        return "Done"

    # NIMAMO ZA POPRAVIT INTERVENCIJE
    # def popravi_intervencijo(self, nov_opis=None, nov_datum=None, nov_tip=None):
    #     # Filter
    #     if not nov_opis and not nov_datum and not nov_tip:
    #         return "Ni zahtevanih sprememb. Intervencija se ni spremenil."
        
    #     # Ustvarjanje povezave
    #     baza = psycopg2.connect(conn_string)
    #     cur = baza.cursor()
        
    #     sql_niz = "UPDATE clan SET"
    #     values = []

    #     if nov_opis:
    #         sql_niz += " opis = %s,"
    #         values.append(nov_opis)
        
    #     if nov_tip:
    #         sql_niz += " tip = %s,"
    #         values.append(nov_tip)
            
    #     if nov_datum:
    #         sql_niz += " datum = %s,"
    #         values.append(nov_datum)

    #     sql_niz = sql_niz.rstrip(',') + " WHERE id = %s;"
    #     values.append(self.id)

    #     cur.execute(sql_niz, tuple(values))
    #     print(f"Popravljena intervencija z id: {self.id}")
    
    #     baza.commit()
    #     cur.close()
    #     baza.close()
    
    @staticmethod
    def dodaj_clana_intervenciji(id_intervencije_za_dodat_clane,emso_clan_na_intervenciji):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz_za_dodajanje_posameznega_clana = "INSERT into prisotnost_na_intervencijah ( id_intervencije,emso_prisotnega) VALUES (%s, %s)"
                cur.execute(sql_niz_za_dodajanje_posameznega_clana,(id_intervencije_za_dodat_clane,emso_clan_na_intervenciji))
                baza.commit()
                
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
                baza.commit()
                
                return "Shranjeno"
            except ValueError:
                
                return "Napaka"


###############################################################################
# VAJE
###############################################################################

@dataclass_json
@dataclass
class Vaja:
    id: int= field(init=False)
    obvezna: bool
    tip_vaje: int
    vodja: int
    datum: date = field(metadata={"format": "date"}, default=None)

    def __str__(self):
        niz = f"Vaja tipa {self.tip_vaje} dne {self.datum}, ki jo vodi {self.vodja}"
        return niz
    
    # Metoda, s katero preko id dostopamo do vaje
    @classmethod
    def get_vaja(cls,id):
        # Povezava z bazo
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        query = f"SELECT * FROM vaja WHERE id = {id};"
        cursor.execute(query)
        fetched_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if fetched_data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, fetched_data))
            return cls(**data_dict)
        else:
            print("Take vaje ne najdem!")
            return None
        
    # POZOR! To ne dela z dekoratorji @staticmethod ali @classmethod
    def dodaj_vajo(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
       #SQL podatki
        sql_niz = "INSERT INTO vaja (obvezna, tip_vaje, vodja, datum) VALUES (%s, %s, %s, %s);"
        values = (self.obvezna,self.tip_vaje,self.vodjaself.datum)
        
        try:
            cur.execute(sql_niz, values)
            # Pridobiti želimo ustvarjen id!
            cur.execute("SELECT currval(pg_get_serial_sequence('vaja', 'id'));")
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
        
    @staticmethod     
    def odstrani_vajo(id):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()

        sql_niz = f"DELETE FROM vaja WHERE id = {id}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()

###############################################################################
# TEKMOVANJA
###############################################################################

@dataclass_json
@dataclass
class Tekomvanje:

    id: int= field(init=False)
    lokacija: str
    tip_tekmovanja: int
    datum: date = field(metadata={"format": "date"}, default=None)

    def __str__(self):
        niz = f"tekomvanje tipa {self.tip_tekmovanja} dne {self.datum} v  {self.lokacija}"
        return niz
    # Metoda, s katero preko id dostopamo do tekmovanja
    @classmethod
    def get_tekmovanje(cls,id):
        # Povezava z bazo
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        query = f"SELECT * FROM tekmovanje WHERE id = {id};"
        cursor.execute(query)
        fetched_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if fetched_data:
            column_names = [desc[0] for desc in cursor.description]
            data_dict = dict(zip(column_names, fetched_data))
            return cls(**data_dict)
        else:
            print("Takega tekmovanja ne najdem!")
            return None
        
    # POZOR! To ne dela z dekoratorji @staticmethod ali @classmethod
    def dodaj_tekmovanje(self):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()
        
       #SQL podatki
        sql_niz = "INSERT INTO tekmovanje (lokacija,tip_tekmovanja,datum) VALUES (%s, %s, %s);"
        values = (self.lokacija,self.tip_tekmovanja,self.datum)
        
        try:
            cur.execute(sql_niz, values)
            # Pridobiti želimo ustvarjen id!
            cur.execute("SELECT currval(pg_get_serial_sequence('tekmovanje', 'id'));")
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
        
    @staticmethod     
    def odstrani_tekmovanje(id):
        #Ustvarjanje povezave
        baza = psycopg2.connect(conn_string)
        cur = baza.cursor()

        sql_niz = f"DELETE FROM tekmovanje WHERE id = {id}"
        cur.execute(sql_niz)
    
        baza.commit()
        cur.close()
        baza.close()

