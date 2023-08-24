# Struktura spletne aplikacije
from bottle import *
from auth import *
from model import *
from datetime import date 
from psycopg2 import *
import bcrypt
import os

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # Znebimo se problemov s šumniki

#PRIVZETE NASTAVITVE 
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Database dostop
conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)


###############################################################################
# REGISTRACIJA IN PRIJAVA
###############################################################################
# connection za uporabnika
def conn_string_user(uporabnik):
    conn_str = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, uporabnik.uporabnisko_ime, uporabnik.geslo)
    return conn_str

# Na začetku preveri uporabnika
def uporabnik_zacetek():
    uporabnisko_ime = request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        try:
            baza = psycopg2.connect(conn_string)
            cur = baza.cursor()
            uporabnik = Uporabnik(uporabnisko_ime, cur)
            #return psycopg2.callback(uporabnik, cur, *psycopg2.largs, **psycopg2.kwargs)
            return uporabnik
        except:
            ValueError("Takega uporabnika ni!")
            redirect("/registracija")
        finally:
            cur.close()
    else:
        redirect("/prijava/")

@get("/registracija/")
def registracija_get():
    return template("registracija.html", napake={}, polja={}, uporabnisko_ime=None)


@post("/registracija/")
def registracija_post():
    uporabnisko_ime = request.forms.getunicode("uporabnisko_ime")
    if os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime že obstaja."}
        return template("registracija.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        Model().shrani_v_datoteko(uporabnisko_ime)
        redirect("/")


@get("/prijava/")
def prijava_get():
    return template("prijava.html", napake={}, polja={}, uporabnisko_ime=None)


@post("/prijava/")
def prijava_post():
    uporabnisko_ime = request.forms.getunicode("uporabnisko_ime")
    if not os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime ne obstaja."}
        return template("prijava.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        redirect("/")


@post("/odjava/")
def odjava_post():
    response.delete_cookie("uporabnisko_ime", path="/")
    redirect("/")
    
@get('/')
def osnovna_stran(uporabnik, cur):      
    return template('osnovna_stran.html')