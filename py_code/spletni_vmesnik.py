# Struktura spletne aplikacije
from bottle import *
from auth import *
from model import *
from datetime import date 
from psycopg2 import *
import hashlib

import os

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # Znebimo se problemov s šumniki

#PRIVZETE NASTAVITVE 
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Database dostop
conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)
baza = psycopg2.connect(conn_string)
cur = baza.cursor()
# cur.execute("PRAGMA foreign_keys = ON;") nevem kaj ta rec dela

###############################################################################
# Osnovna stran
############################################################################### 
# Mapa za statične vire (slike, css, ...)
static_dir = "./static"

skrivnost = "rODX3ulHw3ZYRdbIVcp1IfJTDn8iQTH6TFaNBgrSkjIulrklaraintinestakul"
# streženje statičnih datotek

def nastaviSporocilo(sporocilo = None):
    # global napakaSporocilo
    staro = request.get_cookie("sporocilo", secret=skrivnost)
    if sporocilo is None:
        response.delete_cookie('sporocilo', path="/",secret=skrivnost)
    else:
        response.set_cookie('sporocilo', sporocilo, path="/", secret=skrivnost)
    return staro 


def preveriUporabnika(): 
    uporabnisko_ime = request.get_cookie("uporabnisko_ime", secret=skrivnost)
    with psycopg2.connect(conn_string) as baza:
        if uporabnisko_ime:
            cur = baza.cursor()    
            uporabnik = None
    
            try: 
                uporabnik = cur.execute("SELECT * FROM clan WHERE uporabnisko_ime = %s", (uporabnisko_ime, ))
                uporabnik = cur.fetchone()
            except:
                uporabnik = None
            if uporabnik: 
                return uporabnik
    redirect('/prijava')

@route("/static/<filename:path>")
def static(filename):
    return static_file(filename, root=static_dir)

@get('/')
def osnovna_stran():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            clani = cur.execute("""SELECT ime,priimek FROM clan WHERE aktiven = true AND (CURRENT_DATE-zdravniski) >=630 ORDER BY priimek""")
            clani = cur.fetchall()
            clani_n = cur.execute("""SELECT ime,priimek FROM clan WHERE aktiven = true AND zdravniski IS NULL ORDER BY priimek""")
            clani_n = cur.fetchall()
            vozila = cur.execute("""SELECT tip_vozila,znamka FROM vozilo WHERE aktivno = true AND (CURRENT_DATE-tehnicni) >=325""")
            vozila = cur.fetchall()
            vozila_n = cur.execute("""SELECT tip_vozila,znamka FROM vozilo WHERE aktivno = true AND tehnicni IS NULL""")
            vozila_n = cur.fetchall()
            tek = cur.execute("""SELECT * FROM tekmovanje WHERE (datum - CURRENT_DATE) BETWEEN 0 AND 60""")
            tek = cur.fetchall()
            vaje = cur.execute("""SELECT * FROM vaja WHERE (datum - CURRENT_DATE) BETWEEN 0 AND 60 """)
            vaje = cur.fetchall()
            tip_vaje = cur.execute("""SELECT * FROM tip_intervencije""")
            tip_vaje = cur.fetchall()
            tip_tek = cur.execute("""SELECT * FROM tip_tekmovanja""")
            tip_tek = cur.fetchall()
            tip_v = cur.execute("""SELECT * FROM tip_vozila""")
            tip_v = cur.fetchall()
    return template('osnovna_stran.html',clani_n=clani_n,vozila_n=vozila_n,tip_v=tip_v,clani=clani,vozila=vozila,tek=tek,vaje=vaje,tip_tek=tip_tek,tip_vaje=tip_vaje)


###############################################################################
# Člani
############################################################################### 

@get('/clani/') 
def prikaz_clanov():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            clani = cur.execute("""SELECT emso,ime,priimek,funkcija,cin,zdravniski,aktiven FROM clan WHERE aktiven = true  ORDER BY ime""")
            clani = cur.fetchall()
            fun = cur.execute("""SELECT * FROM funkcija""")
            fun = cur.fetchall()
            c = cur.execute("""SELECT * FROM cin""")
            c = cur.fetchall()
    return template('prikaz_clanov.html',napaka=napaka,clani=clani,fun = fun, c=c)

@get('/dodaj_clana/')
def nov_clan():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            funkcija= cur.execute("""SELECT * FROM funkcija""")
            funkcija = cur.fetchall()
            cin = cur.execute("""SELECT * FROM cin""")
            cin = cur.fetchall()
    return template('n_clan',napaka=napaka,funkcije = funkcija, cin=cin)
    
@post('/dodaj_clana/')
def nov_clan_post():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    ime = request.forms.getunicode('ime')
    priimek = request.forms.getunicode('priimek')
    emso = request.forms.getunicode('emso')
    funkcija = request.forms.getunicode('funkcija')
    cin = request.forms.getunicode('cin')
    zdravniski = request.forms.getunicode('zd')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            funkcija_id = cur.execute(f"""SELECT id_funkcija FROM funkcija WHERE naziv = %s""",[funkcija])
            funkcija_id = cur.fetchall()
            cin_id = cur.execute(f"""SELECT id_cin FROM cin WHERE cin = %s""",[cin])
            cin_id = cur.fetchall()
    try:
        nov = Clan(emso=int(emso),ime=ime,priimek=priimek,funkcija=funkcija_id[0][0],cin=cin_id[0][0],zdravniski=zdravniski)
        nov.dodaj_clana()
    except:
          nastaviSporocilo("ta emšo že obstaja")
    redirect('/clani/')

@post('/odstrani_clana/')
def odstrani_clana():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    emso = request.forms.getunicode('emso')
    try:
        Clan.spremeni_aktivnost(int(emso))
    except:
         nastaviSporocilo("Izbris člana ni uspel")
    redirect('/clani/')

@post('/preusmeritev_popravi_clan/')
def popravi_clana():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    emso = request.forms.getunicode('emso')
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clan = cur.execute(f"""SELECT * FROM clan WHERE emso ={emso} """)
        clan = cur.fetchall()
        fun = cur.execute("""SELECT * FROM funkcija""")
        fun = cur.fetchall()
        c = cur.execute("""SELECT * FROM cin""")
        c = cur.fetchall()
    return template('popravi_clana.html',napaka=napaka,clan=clan,fun=fun,c=c)

@post('/popravi_clana/')
def popravi_clana_dokonco():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    emso = request.forms.getunicode('emso')
    ime = request.forms.getunicode('ime')
    priimek = request.forms.getunicode('priimek')
    funkcija = request.forms.getunicode('funkcija')
    cin = request.forms.getunicode('cin')
    zd = request.forms.getunicode('zd')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            funkcija_id = cur.execute(f"""SELECT id_funkcija FROM funkcija WHERE naziv = %s""",[funkcija])
            funkcija_id = cur.fetchall()
            cin_id = cur.execute(f"""SELECT id_cin FROM cin WHERE cin = %s""",[cin])
            cin_id = cur.fetchall()
    #try:
    Clan.popravi_clana(int(emso),ime,priimek,funkcija_id[0][0],cin_id[0][0],zd)
    #except:
         #nastaviSporocilo("popravljanje podatkov ni uspelo")
    redirect('/clani/')
###################################################################################################     


@get('/vozila/') 
def prikaz_vozil():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            vozila = cur.execute("""SELECT * FROM vozilo WHERE aktivno = true""")
            vozila = cur.fetchall()
            tip = cur.execute("""SELECT * FROM tip_vozila""")
            tip = cur.fetchall()
            izpit = cur.execute("""SELECT * FROM kategorija_vozniskega_dovoljenja""")
            izpit = cur.fetchall()
    return template('prikaz_vozil.html',napaka = napaka,vozila=vozila,tip=tip,izpit=izpit)

@get('/dodaj_vozilo/')
def novo_vozilo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_v = cur.execute("""SELECT * FROM tip_vozila""")
            tip_v = cur.fetchall()
            izpit = cur.execute("""SELECT * FROM kategorija_vozniskega_dovoljenja""")
            izpit = cur.fetchall()
    return template('novo_vozilo.html',napaka=napaka,tip_v=tip_v,izpit=izpit)

@post('/dodaj_vozilo/')
def novo_vozilo_post():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    reg = request.forms.getunicode('reg')
    izpit = request.forms.getunicode('izpit')
    tip = request.forms.getunicode('tip_vozila')
    potniki = request.forms.getunicode('st_potnikov')
    znamka = request.forms.getunicode('znamka')
    tehnicni = request.forms.getunicode('tehnicni')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            izpit_id = cur.execute(f"""SELECT id_kategorije FROM kategorija_vozniskega_dovoljenja WHERE kategorija = %s""",[izpit])
            izpit_id = cur.fetchall()
            tip_id = cur.execute(f"""SELECT id_vozilo FROM tip_vozila WHERE tip_vozila  = %s""",[tip])
            tip_id = cur.fetchall()
    try:
        nov = Vozilo(reg,tip_id[0][0],izpit_id[0][0],int(potniki),znamka,tehnicni)
        nov.dodaj_vozilo()
    except:
        nastaviSporocilo("Ta registerska številka že obstaja")
    redirect('/vozila/')

@post('/odstrani_vozilo/')
def odstrani_vozilo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    reg = request.forms.getunicode('reg')
    try:
        Vozilo.spremeni_aktivnost(reg)
    except:
         nastaviSporocilo("izbris vozila ni uspel")
    redirect('/vozila/')

@post('/preusmeritev_popravi_vozilo/')
def popravi_vozilo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    reg = request.forms.getunicode('reg')
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        vozilo = cur.execute(f"""SELECT * FROM vozilo WHERE registrska_st ='{reg}' """)
        vozilo = cur.fetchall()
        tip_v = cur.execute("""SELECT * FROM tip_vozila""")
        tip_v = cur.fetchall()
        izpit = cur.execute("""SELECT * FROM kategorija_vozniskega_dovoljenja""")
        izpit = cur.fetchall()
    return template('popravi_vozilo.html',napaka=napaka,vozilo=vozilo,tip_v=tip_v,izpit=izpit)

@post('/popravi_vozilo/')
def popravi_clana_dokonco():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    reg = request.forms.getunicode('reg')
    izpit = request.forms.getunicode('izpit')
    tip = request.forms.getunicode('tip_vozila')
    potniki = request.forms.getunicode('st_potnikov')
    znamka = request.forms.getunicode('znamka')
    tehnicni = request.forms.getunicode('tehnicni')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            izpit_id = cur.execute(f"""SELECT id_kategorije FROM kategorija_vozniskega_dovoljenja WHERE kategorija = %s""",[izpit])
            izpit_id = cur.fetchall()
            tip_id = cur.execute(f"""SELECT id_vozilo FROM tip_vozila WHERE tip_vozila  = %s""",[tip])
            tip_id = cur.fetchall()
    try:        
        Vozilo.popravi_vozilo(reg,tip_id[0][0],izpit_id[0][0],int(potniki),znamka,tehnicni)
    except:
        nastaviSporocilo("Popravljanje podatkov ni uspelo")
    redirect('/vozila/')

#######################################################################################

@get("/intervencije/")
def intervencije():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        inte = cur.execute("""SELECT * FROM intervencija""")
        inte = cur.fetchall()
        tip_int = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_int = cur.fetchall()
    return template("prikaz_int.html",napaka=napaka,inte=inte,tip_int=tip_int)

@get("/dodaj_int/")
def dodaj_intervencijo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_int = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_int = cur.fetchall()
    return template('nova_intrvencija.html',tip_int=tip_int, napaka=napaka)

@post("/dodaj_int/")
def post_dodaj_int():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    tip = request.forms.getunicode('tip_int')
    datum = request.forms.getunicode('datum')
    opis = request.forms.getunicode('opis')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_id = cur.execute(f"""SELECT id_tipa_intervencije FROM tip_intervencije WHERE tip  = %s""",[tip])
            tip_id = cur.fetchall()
    try:
        nov = Intervencija(opis,datum,tip_id[0][0])
        nov.dodaj_intervencijo()
        redirect('/dodaj_clane_na_int/')
    except:
         nastaviSporocilo("Dodajanje intervencije ni uspelo")

@get('/dodaj_clane_na_int/')
def dodaj_clane_int():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clani = cur.execute("""SELECT emso,ime,priimek,funkcija,cin,zdravniski,aktiven FROM clan WHERE aktiven=true ORDER BY priimek,ime """)
        clani = cur.fetchall()
        vozila = cur.execute("""SELECT * FROM vozilo WHERE aktivno=true ORDER BY tip_vozila """)
        vozila = cur.fetchall()
        id_int = cur.execute("""SELECT id FROM intervencija""")
        id_int = cur.fetchall()
        tip_v = cur.execute("""SELECT * FROM tip_vozila""")
        tip_v = cur.fetchall()
    return template('dodaj_clane_int.html',napaka=napaka,clani=clani, id_int=id_int,vozila=vozila,tip_v=tip_v)

@post('/dodaj_clane_na_int/')
def post():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    id_intervencije = request.forms.getunicode('id_int')
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clani = cur.execute("""SELECT emso FROM clan WHERE aktiven=true ORDER BY priimek,ime """)
        clani = cur.fetchall()
        vozila = cur.execute("""SELECT * FROM vozilo WHERE aktivno=true ORDER BY tip_vozila """)
        vozila = cur.fetchall()
    za_dodat_clane = []
    za_dodat_vozila = []
    for emso in clani:
        c = request.forms.getunicode(f'{emso[0]}')
        if c is not None:
            za_dodat_clane.append(emso[0])

    for reg in vozila:
        r = request.forms.getunicode(reg[0])
        if r is not None:
            za_dodat_vozila.append(reg[0])    

    try:
        for cl_emso in za_dodat_clane:
            Intervencija.dodaj_clana_intervenciji(int(id_intervencije),cl_emso)

        for v_reg in za_dodat_vozila:
            Intervencija.dodaj_vozilo_intervenciji(int(id_intervencije),v_reg)
    except:
         nastaviSporocilo("dodajane članov in vozil ni dokočno uspelo, izbriši intervencijo in jo ustvari na novo")

    redirect("/intervencije/")


@route("/prikaz_int/", method='POST')
def prikaz_intervencije():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    id_za_prikaz = request.forms.getunicode('id')
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clani_na_int = cur.execute(f"""SELECT ime,priimek FROM prisotnost_na_intervencijah JOIN clan  ON emso_prisotnega = emso WHERE id_intervencije = {id_za_prikaz} """)
        clani_na_int = cur.fetchall()
        vozila_na_int  = cur.execute(f"""SELECT tip_vozila,znamka FROM vozila_na_intervencijah JOIN vozilo ON registracija_vozila = registrska_st WHERE id_intervencije = {id_za_prikaz}""")
        vozila_na_int  = cur.fetchall()
        int = cur.execute(f"""SELECT * FROM intervencija WHERE id = {id_za_prikaz}""")
        int = cur.fetchall()
        tip_v = cur.execute("""SELECT * FROM tip_vozila""")
        tip_v = cur.fetchall()
        tip_int = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_int = cur.fetchall()
    
    return template('podroben_prikaz_int.html',napaka=napaka,int=int,tip_v=tip_v,tip_int=tip_int,clani_na_int=clani_na_int,vozila_na_int=vozila_na_int)

@route('/odstrani_int/', method='POST')
def odstrani_intervencijo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    id = request.forms.getunicode('id')
    try:
        Intervencija.odstrani_intervencijo(int(id))
    except:
        nastaviSporocilo("Izbris intervencije ni uspel")
    redirect('/intervencije/')
      
###############################################################################
# TEKMOVANJA
###############################################################################

@get("/tekmovanja/")
def tekmovanje():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tek = cur.execute("""SELECT * FROM tekmovanje""")
            tek = cur.fetchall()
            tip_tek = cur.execute("""SELECT * FROM tip_tekmovanja""")
            tip_tek = cur.fetchall()
    return template("prikaz_tek.html",napaka=napaka,tek=tek, tip_tek=tip_tek)

@get('/dodaj_tekmovanje/')
def dodaj_tekmovanje():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_tekmo = cur.execute("""SELECT * FROM tip_tekmovanja""")
        tip_tekmo = cur.fetchall()
    return template('novo_tekmovanje.html',napaka=napaka,tip_tekmo=tip_tekmo)

@route('/dodaj_tekekmovanje/', method='POST')
def post_dodaj_tekmovanje():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    datum = request.forms.getunicode('datum')
    tip = request.forms.getunicode('tip_tek')
    lokacija = request.forms.getunicode('lokacija')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_id = cur.execute(f"""SELECT id_tip FROM tip_tekmovanja WHERE tip = %s""",[tip])
            tip_id = cur.fetchall()
    try:
        nov = Tekomvanje(lokacija,tip_id[0][0],datum)
        nov.dodaj_tekmovanje()
    except:
        nastaviSporocilo("Dodajane tekmovanja ni uspelo")
    redirect('/tekmovanja/')

@route('/odstrani_tek/', method='POST')
def odstrani_tekmovanje():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    id = request.forms.getunicode('id_tek')
    try:
        Tekomvanje.odstrani_tekmovanje(int(id))
    except:
        nastaviSporocilo("Izbris tekmovanja ni uspel")
    redirect('/tekmovanja/')

###############################################################################
# VAJE
###############################################################################

@get("/vaje/")
def vaje():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            vaje = cur.execute("""SELECT id,obvezna,tip_vaje,datum,ime,priimek FROM vaja JOIN clan ON vodja=emso""")
            vaje = cur.fetchall()
            tip = cur.execute("""SELECT * FROM tip_intervencije""")
            tip= cur.fetchall()
    return template("prikaz_vaj.html",napaka=napaka,vaje=vaje, tip=tip)   

@get("/dodaj_vajo/")
def dodaj_vajo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_vaje = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_vaje = cur.fetchall()
        vodaja = cur.execute("""SELECT * FROM clan""")
        vodaja = cur.fetchall()
        vaje = cur.execute("""SELECT * FROM vaja""")
        vaje = cur.fetchall()
    return template('nova_vaja.html',napaka=napaka,tip_vaje=tip_vaje,vodja=vodaja,vaje=vaje) 

@route('/dodaj_vajo/', method='POST')
def post_dodaj_vajo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    datum = request.forms.getunicode('datum')
    udeležba = request.forms.getunicode('obvezna')
    tip_vaje = request.forms.getunicode('tip_vaje')
    vodja = request.forms.getunicode('vodja')
    if udeležba == 'obvezna':
         u = 'true'
    else:
         u = 'false'
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_id = cur.execute(f"""SELECT id_tipa_intervencije FROM tip_intervencije WHERE tip  = %s""",[tip_vaje])
            tip_id = cur.fetchall()
    try:
        nov = Vaja(u,tip_id[0][0],int(vodja), datum)
        nov.dodaj_vajo()
    except:
         nastaviSporocilo("Dodajane vaje ni uspelo")
    redirect('/vaje/')

@route('/odstrani_vajo/', method='POST')
def odstrani_vajo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    id = request.forms.getunicode('id_vaje')
    try:
        Vaja.odstrani_vajo(int(id))
    except:
        nastaviSporocilo("Izbris vaje ni uspel")
    redirect("/vaje/")

###########################################################################
@get("/oprema/")
def oprema():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka = nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            clani = cur.execute("""SELECT emso,ime,priimek FROM clan WHERE aktiven=true ORDER BY priimek,ime""")
            clani = cur.fetchall()
    return template("prikaz_clanov_oprema.html",napaka=napaka,clani=clani)

@get("/preusmeritev_pregled_opreme/<emso_za_prikaz>/")
def prikaz_opreme(emso_za_prikaz):
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    napaka= nastaviSporocilo()
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        oprema_clana = cur.execute(f"""SELECT * FROM osebna_oprema WHERE emso_clana = {emso_za_prikaz} """)
        oprema_clana = cur.fetchall()
        clan = cur.execute(f"""SELECT emso,ime,priimek FROM clan WHERE emso ={emso_za_prikaz} """)
        clan = cur.fetchall()
    
    return template('podroben_prikaz_opreme.html',napaka=napaka,oprema_clana=oprema_clana,clan=clan)


@route("/dodaj_opremo/", method='POST')
def dodaj_opremo_clanu():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    emso_za_dodajo = request.forms.getunicode('emso')
    oprema = request.forms.getunicode('oprema')
    try:
        nov = Oprema(int(emso_za_dodajo),oprema)
        nov.dodaj_opremo()
    except:
         nastaviSporocilo("Dodajanje opreme ni uspelo")
    redirect(f'/preusmeritev_pregled_opreme/{emso_za_dodajo}/')


@route("/odstrani_opremo/", method='POST')
def odstrani_opremo():
    uporabnik = preveriUporabnika()
    if uporabnik is None: 
        return
    id_opreme = request.forms.getunicode('id_opreme')
    emso =request.forms.getunicode('emso')
    try:
        Oprema.odstrani_opremo(int(id_opreme))
    except:
        nastaviSporocilo("Odstranitev opreme ni uspelo")
    redirect(f"/preusmeritev_pregled_opreme/{emso}/")


###############################################################################
# Registracija, prijava, odjava
############################################################################### 

def hashGesla(s):
    m = hashlib.sha256()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

@get('/registracija')
def registracija_get():
    napaka = nastaviSporocilo()
    return template('registracija.html', napaka=napaka)

@route('/registracija', method='POST')
def registracija_post():
    emso = request.forms.getunicode('emso')
    uporabnisko_ime = request.forms.getunicode('uporabnisko_ime')
    geslo = request.forms.getunicode('geslo')
    geslo2 = request.forms.getunicode('geslo2')
    if emso is None or uporabnisko_ime is None or geslo is None or geslo2 is None:
        nastaviSporocilo('Registracija ni možna! Prosim, nastavi vsa obvezna polja.') 
        redirect('/registracija')
        return
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()    
        uporabnik = Clan.get_clan(emso)
        if uporabnik is None:
            nastaviSporocilo('Registracija ni možna! Člana s to EMŠO ni v bazi.') 
            redirect('/registracija')
            return
        if len(geslo) < 4:
            nastaviSporocilo('Geslo mora imeti vsaj 4 znake.') 
            redirect('/registracija')
            return
        if geslo != geslo2:
            nastaviSporocilo('Gesli se ne ujemata.') 
            redirect('/registracija')
            return
        #try:
        #    zgostitev = hashGesla(geslo)
        #    cur.execute(f"UPDATE clan SET uporabnisko_ime = %s, geslo = %s WHERE emso = %s", (uporabnisko_ime, zgostitev, int(emso)))
        #    response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
        #except:
        #    nastaviSporocilo("To uporabniško ime je že zasedeno.")
        #    redirect('/registracija')
        if Clan.validate_username(uporabnisko_ime) == False:
            nastaviSporocilo("To uporabniško ime je že zasedeno.")
            redirect('/registracija')
            return
        zgostitev = hashGesla(geslo)
        cur.execute(f"UPDATE clan SET uporabnisko_ime = %s, geslo = %s WHERE emso = %s", (uporabnisko_ime, zgostitev, int(emso)))
        response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
    redirect('/')


@get('/prijava')
def prijava_get():
    napaka = nastaviSporocilo()
    return template('prijava.html', napaka=napaka)

@route('/prijava', method='POST')
def prijava_post():
    uporabnisko_ime = request.forms.uporabnisko_ime
    geslo = request.forms.geslo
    if uporabnisko_ime is None or geslo is None:
        nastaviSporocilo('Uporabniško ime in geslo morata biti neprazna') 
        redirect('/prijava')
        return
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()    
        hashBaza = None
        try: 
            hashBaza = cur.execute("SELECT geslo FROM clan WHERE uporabnisko_ime = %s", (uporabnisko_ime, ))
            hashBaza = cur.fetchone()
            hashBaza = hashBaza[0]
        except:
            hashBaza = None
    if hashBaza is None:
        nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
        redirect('/prijava')
        return
    if hashGesla(geslo) != hashBaza:
        nastaviSporocilo('Uporabniško geslo ali ime nista ustrezni') 
        redirect('/prijava')
        return
    response.set_cookie('uporabnisko_ime', uporabnisko_ime, secret=skrivnost)
    redirect('/')
    
@get('/odjava')
def odjava_get():
    response.delete_cookie('uporabnisko_ime')
    redirect('/prijava')



###################################################################################33
# Poženemo strežnik
run(host='localhost', port=8080, reloader=True) 
