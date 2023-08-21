# Jedro aplikacije
import psycopg2
# podatki za dostop do postgreSQL baze
from auth import *

conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)

# dataclass Drustvo: ??????

class Član:
    def __init__(self, emso, ime, priimek, funkcija, čin):
        ## bi mogla dodat še kdaj je opravil zdravniški pregled (tudi v osnovno tabelo v SQL)
        self.emso = emso
        self.ime = ime
        self.priimek = priimek
        self.funkcija = funkcija
        self.čin = čin

    def __str__(self):
        niz = f"Član {self.ime} {self.priimek}"

    @classmethod
    def dodaj_člana(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO vozilo (emso, ime, priimek, funkcija,čin) VALUES (%s, %s, %s, %s,%s);"
                cur.execute(sql_niz, (self.emso, self.ime, self.priimek, self.funkcija,self.čin))
                return "Shranjeno"
            except ValueError:
                return "Napaka"
            
    @classmethod
    def odstrani_člana(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM vozilo WHERE emso = {self.emso}"
            cur.execute(sql_niz)
    

class Vozila:
    def __init__(self, registerska_st, tip_vozila, potreben_izpit, st_potnikov):
        if isinstance(registerska_st, str):
            self.registerska_st = registerska_st
        else:
            raise TypeError
        self.tip_vozila = tip_vozila
        self.potreben_izpit = potreben_izpit
        self.st_potnikov = st_potnikov

    def __str__(self):
        niz = f"Vozilo tipa {self.tip_vozila} z registracijo {self.registerska_st}"

    
    @classmethod
    def dodaj_vozilo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO vozilo (registerska_st, tip_vozila, potreben_izpit, st_potnikov) VALUES (%s, %s, %s, %s);"
                cur.execute(sql_niz, (self.registerska_st, self.tip_vozila, self.potreben_izpit, self.st_potnikov))
                return "Shranjeno"
            except ValueError:
                return "Napaka"

    @classmethod
    def odstrani_vozilo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM vozilo WHERE registrska_st = {self.registrska_st}"
            cur.execute(sql_niz)


### prvotno sa mislia dodat še kraj ma ni pa nič kritičnega če to spustimo in je kako to itak v opisu
class Intervencije:
    def __init__(self,id, opis, datum, tip):
        self.id = id
        self.opis = opis
        self.datum = datum
        self.tip = tip

    def __str__(self):
        niz = f"Intervencija tipa {self.tip} dne {self.datum} z opisom: {self.opis}"

    @classmethod
    def dodaj_intervencijo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO intervencija (opis,datum,tip) VALUES (%s, %s, %s);"
                cur.execute(sql_niz, (self.opis, self.datum, self.tip))
                ## ko dadoamo intervencijo bi mogli potem pot self.id skranit id intervencija
                ## ker jo potem potrebujemo za izpris ali bilo kaj
                return "Shranjeno"
            except ValueError:
                return "Napaka"
    @classmethod
    def odstrani_intervencijo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM intervencija WHERE id = {self.id}"
            cur.execute(sql_niz)

class Vaja:
    def __init__(self,id,datum,obvezna,tip_vaje,vodja):
        self.id = id
        self.datum = datum
        self.obvezna = obvezna
        self.tip_vaje = tip_vaje
        self.vodja = vodja

    def __str__(self):
        niz = f"vaja tipa {self.tip_vaje} dne {self.datum}, ki jo vodi: {self.vodja}"
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
    def odstrani_intervencijo(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM intervencija WHERE id = {self.id}"
            cur.execute(sql_niz)    

class Tekomvanje:
    def __init__(self,id,datum,lokacija,tip_tekmovanja):
        self.id = id
        self.datum = datum
        self.lokacija = lokacija
        self.tip_tekomvanja = tip_tekmovanja

    def __str__(self):
        niz = f"tekomvanje tipa {self.tip_tekomvanja} dne {self.datum} v  {self.lokacija}"
    def dodaj_tekmovanje(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            try:
                sql_niz = "INSERT INTO tekomanje (datum,lokacija,tip_tekomvanja) VALUES (%s, %s, %s);"
                cur.execute(sql_niz, ( self.datum,self.lokacija, self.tip_tekomvanja))
                ## ko dadoamo tekmovanja bi mogli potem pot self.id shranit id tekomvanja
                ## ker jo potem potrebujemo za izpris ali bilo kaj
                return "Shranjeno"
            except ValueError:
                return "Napaka"
    def odstrani_tekmovanje(self):
        with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            sql_niz = "DELETE FROM tekmovanje WHERE id = {self.id}"
            cur.execute(sql_niz)  
