# Jedro aplikacije
import psycopg2
# podatki za dostop do postgreSQL baze
from auth import *

conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)

# dataclass Drustvo: ??????

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
    

class Vozila:
    def __init__(self, registerska_st, tip_vozila, potreben_izpit, st_potnikov,znamka,tehnicni):
            self.registerska_st = registerska_st
            self.tip_vozila = tip_vozila
            self.potreben_izpit = potreben_izpit
            self.st_potnikov = st_potnikov
            self.znamka = znamka
            self.tehnicni = tehnicni

    def __str__(self):
        niz = f"Vozilo tipa {self.tip_vozila} z registracijo {self.registerska_st}"

    
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
    




