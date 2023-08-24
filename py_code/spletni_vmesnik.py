# Struktura spletne aplikacije
from bottle import *
from auth import *
from model import *
from datetime import date 

import os

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # Znebimo se problemov s šumniki

#PRIVZETE NASTAVITVE 
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# Database dostop
conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)


@get('/')
def osnovna_stran():
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
@get('/clani/') 
def prikaz_clanov():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            clani = cur.execute("""SELECT * FROM clan WHERE aktiven = true  ORDER BY ime""")
            clani = cur.fetchall()
            fun = cur.execute("""SELECT * FROM funkcija""")
            fun = cur.fetchall()
            c = cur.execute("""SELECT * FROM cin""")
            c = cur.fetchall()
    return template('prikaz_clanov.html',clani=clani,fun = fun, c=c)

@get('/dodaj_clana/')
def nov_clan():
     with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            funkcija= cur.execute("""SELECT * FROM funkcija""")
            funkcija = cur.fetchall()
            cin = cur.execute("""SELECT * FROM cin""")
            cin = cur.fetchall()
     return template('n_clan',funkcije = funkcija, cin=cin)
    
@post('/dodaj_clana/')
def nov_clan_post():
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
    nov = Clan(int(emso),ime,priimek,funkcija_id[0][0],cin_id[0][0],zdravniski)
    nov.dodaj_clana()
    redirect('/clani/')

@post('/odstrani_clana/')
def odstrani_clana():
    emso = request.forms.getunicode('emso')
    Clan.spremeni_aktivnost(int(emso))
    redirect('/clani/')

@post('/preusmeritev_popravi_clan/')
def popravi_clana():
    emso = request.forms.getunicode('emso')
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clan = cur.execute(f"""SELECT * FROM clan WHERE emso ={emso} """)
        clan = cur.fetchall()
        fun = cur.execute("""SELECT * FROM funkcija""")
        fun = cur.fetchall()
        c = cur.execute("""SELECT * FROM cin""")
        c = cur.fetchall()
    return template('popravi_clana.html',clan=clan,fun=fun,c=c)

@post('/popravi_clana/')
def popravi_clana_dokonco():
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
    Clan.popravi_clana(emso,ime,priimek,funkcija_id[0][0],cin_id[0][0],zd)
    redirect('/clani/')
###################################################################################################     


@get('/vozila/') 
def prikaz_vozil():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            vozila = cur.execute("""SELECT * FROM vozilo WHERE aktivno = true""")
            vozila = cur.fetchall()
            tip = cur.execute("""SELECT * FROM tip_vozila""")
            tip = cur.fetchall()
            izpit = cur.execute("""SELECT * FROM kategorija_vozniskega_dovoljenja""")
            izpit = cur.fetchall()
    return template('prikaz_vozil.html',vozila=vozila,tip=tip,izpit=izpit)

@get('/dodaj_vozilo/')
def novo_vozilo():
     with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_v = cur.execute("""SELECT * FROM tip_vozila""")
            tip_v = cur.fetchall()
            izpit = cur.execute("""SELECT * FROM kategorija_vozniskega_dovoljenja""")
            izpit = cur.fetchall()
     return template('novo_vozilo.html',tip_v=tip_v,izpit=izpit)

@post('/dodaj_vozilo/')
def novo_vozilo_post():
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
    nov = Vozilo(reg,tip_id[0][0],izpit_id[0][0],int(potniki),znamka,tehnicni)
    nov.dodaj_vozilo()
    redirect('/vozila/')

@post('/odstrani_vozilo/')
def odstrani_vozilo():
    reg = request.forms.getunicode('reg')
    Vozilo.spremeni_aktivnost(reg)
    redirect('/vozila/')

@post('/preusmeritev_popravi_vozilo/')
def popravi_vozilo():
    reg = request.forms.getunicode('reg')
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        vozilo = cur.execute(f"""SELECT * FROM vozilo WHERE registrska_st ='{reg}' """)
        vozilo = cur.fetchall()
        tip_v = cur.execute("""SELECT * FROM tip_vozila""")
        tip_v = cur.fetchall()
        izpit = cur.execute("""SELECT * FROM kategorija_vozniskega_dovoljenja""")
        izpit = cur.fetchall()
    return template('popravi_vozilo.html',vozilo=vozilo,tip_v=tip_v,izpit=izpit)

@post('/popravi_vozilo/')
def popravi_clana_dokonco():
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
    Vozilo.popravi_vozilo(reg,tip_id[0][0],izpit_id[0][0],int(potniki),znamka,tehnicni)
    redirect('/vozila/')

#######################################################################################

@get("/intervencije/")
def intervencije():
      with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            inte = cur.execute("""SELECT * FROM intervencija""")
            inte = cur.fetchall()
            tip_int = cur.execute("""SELECT * FROM tip_intervencije""")
            tip_int = cur.fetchall()
      return template("prikaz_int.html",inte=inte, tip_int=tip_int)

@get("/dodaj_int/")
def dodaj_intervencijo():
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_int = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_int = cur.fetchall()
    return template('nova_intrvencija.html',tip_int=tip_int)

@post("/dodaj_int/")
def post_dodaj_int():
    tip = request.forms.getunicode('tip_int')
    datum = request.forms.getunicode('datum')
    opis = request.forms.getunicode('opis')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_id = cur.execute(f"""SELECT id_tipa_intervencije FROM tip_intervencije WHERE tip  = %s""",[tip])
            tip_id = cur.fetchall()
    nov = Intervencija(opis,datum,tip_id[0][0])
    nov.dodaj_intervencijo()
    redirect('/dodaj_clane_na_int/')

@get('/dodaj_clane_na_int/')
def dodaj_clane_int():
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clani = cur.execute("""SELECT * FROM clan WHERE aktiven=true ORDER BY priimek,ime """)
        clani = cur.fetchall()
        vozila = cur.execute("""SELECT * FROM vozilo WHERE aktivno=true ORDER BY tip_vozila """)
        vozila = cur.fetchall()
        id_int = cur.execute("""SELECT id FROM intervencija""")
        id_int = cur.fetchall()
        tip_v = cur.execute("""SELECT * FROM tip_vozila""")
        tip_v = cur.fetchall()
    return template('dodaj_clane_int.html',clani=clani, id_int=id_int,vozila=vozila,tip_v=tip_v)

@post('/dodaj_clane_na_int/')
def post():
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

    for cl_emso in za_dodat_clane:
        Intervencija.dodaj_clana_intervenciji(int(id_intervencije),cl_emso)

    for v_reg in za_dodat_vozila:
        Intervencija.dodaj_vozilo_intervenciji(int(id_intervencije),v_reg)

    redirect("/intervencije/")


@route("/prikaz_int/", method='POST')
def prikaz_intervencije():
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
    
    return template('podroben_prikaz_int.html',int=int,tip_v=tip_v,tip_int=tip_int,clani_na_int=clani_na_int,vozila_na_int=vozila_na_int)

@route('/odstrani_int/', method='POST')
def odstrani_intervencijo():
    id = request.forms.getunicode('id')
    Intervencija.odstrani_intervencijo(int(id))
    redirect('/intervencije/')
      
##################################################################
@get("/tekmovanja/")
def tekmovanje():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tek = cur.execute("""SELECT * FROM tekmovanje""")
            tek = cur.fetchall()
            tip_tek = cur.execute("""SELECT * FROM tip_tekmovanja""")
            tip_tek = cur.fetchall()
    return template("prikaz_tek.html",tek=tek, tip_tek=tip_tek)

@get('/dodaj_tekmovanje/')
def dodaj_tekmovanje():
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_tekmo = cur.execute("""SELECT * FROM tip_tekmovanja""")
        tip_tekmo = cur.fetchall()
    return template('novo_tekmovanje.html',tip_tekmo=tip_tekmo)

@route('/dodaj_tekekmovanje/', method='POST')
def post_dodaj_tekmovanje():
    datum = request.forms.getunicode('datum')
    tip = request.forms.getunicode('tip_tek')
    lokacija = request.forms.getunicode('lokacija')
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            tip_id = cur.execute(f"""SELECT id_tip FROM tip_tekmovanja WHERE tip = %s""",[tip])
            tip_id = cur.fetchall()
    nov = Tekomvanje(lokacija,tip_id[0][0],datum)
    nov.dodaj_tekmovanje()
    redirect('/tekmovanja/')

@route('/odstrani_tek/', method='POST')
def odstrani_tekmovanje():
    id = request.forms.getunicode('id_tek')
    Tekomvanje.odstrani_tekmovanje(int(id))
    redirect('/tekmovanja/')

###############################################################################
# VAJE
###############################################################################

@get("/vaje/")
def vaje():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            vaje = cur.execute("""SELECT id,obvezna,tip_vaje,datum,ime,priimek FROM vaja JOIN clan ON vodja=emso""")
            vaje = cur.fetchall()
            tip = cur.execute("""SELECT * FROM tip_intervencije""")
            tip= cur.fetchall()
    return template("prikaz_vaj.html",vaje=vaje, tip=tip)   

@get("/dodaj_vajo/")
def dodaj_vajo():
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_vaje = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_vaje = cur.fetchall()
        vodaja = cur.execute("""SELECT * FROM clan""")
        vodaja = cur.fetchall()
        vaje = cur.execute("""SELECT * FROM vaja""")
        vaje = cur.fetchall()
    return template('nova_vaja.html',tip_vaje=tip_vaje,vodja=vodaja,vaje=vaje) 

@route('/dodaj_vajo/', method='POST')
def post_dodaj_vajo():
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

    nov = Vaja(u,tip_id[0][0],int(vodja), datum)
    nov.dodaj_vajo()
    redirect('/vaje/')

@route('/odstrani_vajo/', method='POST')
def odstrani_vajo():
     id = request.forms.getunicode('id_vaje')
     Vaja.odstrani_vajo(int(id))
     redirect("/vaje/")

###########################################################################
@get("/oprema/")
def oprema():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            clani = cur.execute("""SELECT emso,ime,priimek FROM clan WHERE aktiven=true ORDER BY priimek,ime""")
            clani = cur.fetchall()
    return template("prikaz_clanov_oprema.html",clani=clani)

@get("/preusmeritev_pregled_opreme/<emso_za_prikaz>/")
def prikaz_opreme(emso_za_prikaz):
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        oprema_clana = cur.execute(f"""SELECT * FROM osebna_oprema WHERE emso_clana = {emso_za_prikaz} """)
        oprema_clana = cur.fetchall()
        clan = cur.execute(f"""SELECT emso,ime,priimek FROM clan WHERE emso ={emso_za_prikaz} """)
        clan = cur.fetchall()
    
    return template('podroben_prikaz_opreme.html',oprema_clana=oprema_clana,clan=clan)


@route("/dodaj_opremo/", method='POST')
def dodaj_opremo_clanau():
    emso_za_dodajo = request.forms.getunicode('emso')
    oprema = request.forms.getunicode('oprema')
    nov = Oprema(int(emso_za_dodajo),oprema)
    nov.dodaj_opremo()
    redirect(f'/preusmeritev_pregled_opreme/{emso_za_dodajo}/')


@route("/odstrani_opremo/", method='POST')
def prikaz_opreme():
    id_opreme = request.forms.getunicode('id_opreme')
    emso =request.forms.getunicode('emso')
    Oprema.odstrani_opremo(int(id_opreme))
    redirect(f"/preusmeritev_pregled_opreme/{emso}/")





###################################################################################33
# Priklop na bazo
baza = psycopg2.connect(conn_string)

# Poženemo strežnik
run(host='localhost', port=8080, reloader=True) 
