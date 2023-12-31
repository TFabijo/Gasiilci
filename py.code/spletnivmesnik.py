# Struktura spletne aplikacije
from bottle import *
import psycopg2
from auth import *
from mod import *

# Database dostop
conn_string = "host = '{0}' dbname = '{1}' user = '{2}' password = '{3}'".format(host, dbname, user, password)


@get('/')
def osnovna_stran():
    return template('osnovna_stran.html')

@get('/clani/') 
def prikaz_clanov():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            clani = cur.execute("""SELECT * FROM clan""")
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
def odstrani_c():
    emso = request.forms.getunicode('emso')
    Clan.odstrani_clana(int(emso))
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
            vozila = cur.execute("""SELECT * FROM vozilo""")
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
    nov = Vozila(reg,tip_id[0][0],izpit_id[0][0],int(potniki),znamka,tehnicni)
    nov.dodaj_vozilo()
    redirect('/vozila/')

@post('/odstrani_vozilo/')
def odstrani_c():
    reg = request.forms.getunicode('reg')
    Vozila.odstrani_vozilo(reg)
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
    Vozila.popravi_vozilo(reg,tip_id[0][0],izpit_id[0][0],int(potniki),znamka,tehnicni)
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
    nov = Intervencije(opis,datum,tip_id[0][0])
    nov.dodaj_intervencijo()
    redirect('/dodaj_clane_na_int/')

@get('/dodaj_clane_na_int/')
def dodaj_clane_int():
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        clani = cur.execute("""SELECT * FROM clan ORDER BY priimek,ime""")
        clani = cur.fetchall()
        vozila = cur.execute("""SELECT * FROM vozilo ORDER BY tip_vozila""")
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
        clani = cur.execute("""SELECT emso FROM clan ORDER BY priimek,ime""")
        clani = cur.fetchall()
        vozila = cur.execute("""SELECT * FROM vozilo ORDER BY tip_vozila""")
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
        Intervencije.dodaj_clana_intervenciji(int(id_intervencije),cl_emso)

    for v_reg in za_dodat_vozila:
        Intervencije.dodaj_vozilo_intervenciji(int(id_intervencije),v_reg)

    redirect("/intervencije/")


@route("/prikaz_int/", method='POST')
def prikaz_intervencije():
    id_za_prikaz = request.forms.getunicode('id')    
    return f"{id_za_prikaz}"


      
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
    nov = Tekomvanje(datum,lokacija,tip_id[0][0])
    nov.dodaj_tekmovanje()
    redirect('/tekmovanja/')

@route('/odstrani_tek/', method='POST')
def odstrani_tekmovanje():
    id = request.forms.getunicode('id_tek')
    Tekomvanje.odstrani_tekmovanje(int(id))
    redirect('/tekmovanja/')

######################################################################
@get("/vaje/")
def vaje():
    with psycopg2.connect(conn_string) as baza:
            cur = baza.cursor()
            vaje = cur.execute("""SELECT * FROM vaja""")
            vaje = cur.fetchall()
            tip_vaje = cur.execute("""SELECT * FROM tip_intervencije""")
            tip_vaje = cur.fetchall()
    return template("prikaz_vaj.html",vaje=vaje, tip_vaje=tip_vaje)   

@get("/dodaj_vajo/")
def dodaj_vajo():
    with psycopg2.connect(conn_string) as baza:
        cur = baza.cursor()
        tip_vaje = cur.execute("""SELECT * FROM tip_intervencije""")
        tip_vaje = cur.fetchall()
        vodaja = cur.execute("""SELECT * FROM clan""")
        vodaja = cur.fetchall()
    return template('nova_vaja.html',tip_vaje=tip_vaje,vodja=vodaja) 

@route('/dodaj_vajo/', method='POST')
def post_dodaj_tekmovanje():
    datum = request.forms.getunicode('datum')
    obvezna = request.forms.getunicode('obvezna')
    tip_vaje = request.forms.getunicode('tip_vaje')
    vodja = request.forms.getunicode('vodja')
    return f"{datum},{obvezna},{tip_vaje} in še {vodja}"


###########################################################################
# Priklop na bazo
baza = psycopg2.connect(conn_string)

# Poženemo strežnik
run(host='localhost', port=8080, reloader=True) 

## vaja git hahahaha