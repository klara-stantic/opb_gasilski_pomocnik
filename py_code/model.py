# Jedro aplikacije
import psycopg2
# podatki za dostop do postgreSQL baze
from auth import *

conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)

# dataclass Drustvo: ??????

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


