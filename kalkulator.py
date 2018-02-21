from flask import Flask
from flask import render_template, request, flash, redirect, url_for
import os
import psycopg2
from urllib.parse import urlparse
import forms
import insert
import update
from polacz import polacz
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET', 'POST'])
def kalkulator():
    form = forms.OkregZaloguj(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        kursor.execute("""SELECT idokreg_wyborczy FROM okreg_wyborczy;""")
        okregi = kursor.fetchall() #lista jednoelementowych krotek
        numery = [numer[0] for numer in okregi] # lista = [element 0 krotki dla elementu w liscie]
        if form.numer.data in numery:
            return redirect(url_for('menu_komisarz',numer=form.numer.data))

    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("""SELECT * FROM okw;""")
    okw = kursor.fetchall()
    kursor.execute("SELECT * FROM okreg_wyborczy ORDER BY idokreg_wyborczy;")
    okregi = kursor.fetchall()
    kursor.execute("SELECT * FROM okw;")
    okw = kursor.fetchall()
    conn.close()
    return render_template('kalkulator.html', form=form, okregi=okregi, okw=okw)

@app.route('/wyniki')
def wyniki():
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM okreg_wyborczy ORDER BY idokreg_wyborczy;")
    okregi = kursor.fetchall()
    kursor.execute("select sum(sum) from frekwencja_w_obwodach;")
    frekwencja = kursor.fetchone()
    conn.close()
    return render_template('wyniki.html',okregi=okregi, frekwencja=frekwencja)


@app.route('/menu_obwod/<numer>')
def menu_obwod(numer):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okw WHERE idobwod_wyborczy = (%s);""", (numer,))
    obwod= kursor.fetchone()
    conn.close()
    return render_template('menu_obwod.html', numer=numer, obwod=obwod)

@app.route('/dodaj_wyniki_obwod/<numer>', methods=['GET', 'POST'])
def dodaj_wyniki_obwod(numer):
    form = forms.DodajGlosy(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        insert.kandydat_w_obwodzie(kursor, form.id.data, numer, form.glosy.data)
        conn.commit()
        conn.close()
        flash("Dodano!")
        return redirect(url_for('dodaj_wyniki_obwod',numer=numer))
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okw WHERE idobwod_wyborczy = (%s);""", (numer,))
    obwod= kursor.fetchone()
    kursor.execute("""SELECT * FROM protokol_w_obwodzie WHERE idobwod_wyborczy = (%s);""", (numer,))
    protokol = kursor.fetchall()
    conn.close()
    return render_template('dodaj_wyniki_obwod.html', form=form, numer=numer, obwod=obwod, protokol=protokol)

#http://samorzad2014.pkw.gov.pl/321_protokol_komisji_obwodowej/22942/rdw_3
@app.route('/protokol_obwod/<numer>')
def protokol_obwod(numer):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okw WHERE idobwod_wyborczy = (%s);""", (numer,))
    obwod= kursor.fetchone()
    kursor.execute("""SELECT * FROM protokol_w_obwodzie WHERE idobwod_wyborczy = (%s);""", (numer,))
    protokol = kursor.fetchall()
    kursor.execute("""select * from frekwencja_w_obwodach where idobwod_wyborczy = (%s);""",(numer,))
    frekwencja = kursor.fetchone()
    kursor.execute("""SELECT idkomitet, nazwa_komitetu, sum(liczba_glosow) FROM protokol_w_obwodzie where idobwod_wyborczy = (%s)
     GROUP BY idkomitet, nazwa_komitetu ORDER BY idkomitet;""",(numer,))
    komitety = kursor.fetchall()
    wyniki = {element[1]: element[5]/frekwencja[1]*100 for element in protokol}
    conn.close()
    return render_template('protokol_obwod.html', numer=numer, obwod=obwod,
     protokol=protokol, frekwencja=frekwencja[1], komitety=komitety, wyniki=wyniki)


@app.route('/menu_pkw')
def menu_pkw():
    return render_template('menu_pkw.html')

@app.route('/okregi',methods=['GET', 'POST'])
def okregi():
    form = forms.DodajOkreg(request.form)
    if request.method == 'POST' and form.validate():
        Okreg = {"lokalizacja":form.lokalizacja.data, "komisarz":form.komisarz.data}
        
        conn = polacz()
        kursor = conn.cursor()
        insert.okreg_wyborczy(kursor, Okreg["lokalizacja"],Okreg["komisarz"])
        conn.commit()
        conn.close()
        flash('Dodano')
        return redirect('okregi')
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM okreg_wyborczy ORDER BY idokreg_wyborczy;")
    okregi = kursor.fetchall()
    conn.close()
    return render_template('okregi.html', form=form, okregi=okregi)


@app.route('/menu_okregi')
def menu_okregi():
    return render_template('menu_okregi.html')


@app.route('/zobacz_okregi')
def zobacz_okregi():
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM okreg_wyborczy ORDER BY idokreg_wyborczy;")
    okregi = kursor.fetchall()
    conn.close()
    return render_template('zobacz_okregi.html',okregi=okregi)



@app.route('/edytuj_okreg',methods=['GET', 'POST'])
def edytuj_okreg():
    form = forms.EdytujOkreg(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s) """,(form.idokregu.data,))
        stary_okreg = kursor.fetchone()
        if not form.lokalizacja.data:
            form.lokalizacja.data = stary_okreg[1]
        if not form.komisarz.data:
            form.komisarz.data = stary_okreg[2]
        update.okreg_wyborczy(kursor, form.idokregu.data, form.lokalizacja.data, form.komisarz.data)
        if form.noweidokregu.data is not None:
            kursor.execute("""UPDATE okreg_wyborczy set idokreg_wyborczy = (%s) where idokreg_wyborczy =(%s);""",(999,form.noweidokregu.data))
            kursor.execute("""UPDATE okreg_wyborczy set idokreg_wyborczy = (%s) where idokreg_wyborczy =(%s);""",(form.noweidokregu.data,form.idokregu.data))
            kursor.execute("""UPDATE okreg_wyborczy set idokreg_wyborczy = (%s) where idokreg_wyborczy =(%s);""",(form.idokregu.data,999))
        conn.commit()
        conn.close()
        return redirect('zobacz_okregi')
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM okreg_wyborczy ORDER BY idokreg_wyborczy;")
    okregi = kursor.fetchall()
    conn.close() 
    return render_template('edytuj_okreg.html', form=form, okregi=okregi)



@app.route('/kandydaci')
def kandydat_menu():
    return render_template('kandydaci.html')

@app.route('/menu_kandydaci/<numer>')
def menu_kandydaci(numer):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(numer,))
    okreg = kursor.fetchone()
    conn.close()
    return render_template('menu_kandydaci.html', numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])

@app.route('/komitet_menu')
def komitet_menu():
    return render_template('komitet_menu.html')

@app.route('/dodaj_komitet', methods=['GET', 'POST'])
def dodaj_komitet():
    form = forms.DodajKomitet(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        insert.komitet(kursor, form.nazwa.data)
        conn.commit()
        conn.close()
        flash("Dodano!")
        return redirect('dodaj_komitet')
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM komitet ORDER BY idkomitet;")
    komitety = kursor.fetchall()
    conn.close()
    return render_template('dodaj_komitet.html', form=form, komitety=komitety)

@app.route('/zobacz_komitet')
def zobacz_komitet():
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM komitet ORDER BY idkomitet;")
    komitety = kursor.fetchall()
    conn.close()
    return render_template('zobacz_komitet.html', komitety=komitety)


@app.route('/edytuj_komitet',methods=['GET', 'POST'])
def edytuj_komitet():
    form = forms.EdytujKomitet(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        update.komitet(kursor, form.id.data, form.noweid.data, form.nazwa.data)
        conn.commit()
        conn.close()
        flash('Dokonano zmiany!')
        return redirect('zobacz_komitet')
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("SELECT * FROM komitet ORDER BY idkomitet;")
    komitety = kursor.fetchall()
    conn.close()
    return render_template('edytuj_komitet.html', form=form, komitety=komitety)

@app.route('/dodaj_kandydata/<numer>', methods=['GET', 'POST'])
def dodaj_kandydata(numer):
    form = forms.DodajKandydata(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        insert.kandydat(kursor, form.numer_listy.data, form.imie.data, form.nazwisko.data, numer)
        conn.commit()
        conn.close()
        flash("Dodano!")
        return redirect(url_for('dodaj_kandydata',numer=numer))
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("""SELECT kom.nazwa_komitetu, k.idkandydat, k.imie, k.nazwisko from kandydat k
    inner join lista l on k.idkandydat=l.idkandydat
    inner join komitet kom on kom.idkomitet=l.idkomitet
    inner join kandydat_w_okregu kwo on kwo.idkandydat=k.idkandydat
    where kwo.idokreg_wyborczy = (%s)
    order by kom.idkomitet;""",(numer,))
    kandydaci = kursor.fetchall()
    kursor.execute("SELECT * FROM komitet ORDER BY idkomitet;")
    komitety = kursor.fetchall()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(numer,))
    okreg = kursor.fetchone()
    conn.close()
    print(okreg)
    return render_template('dodaj_kandydata.html', form=form, komitety=komitety, kandydaci=kandydaci, numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])


@app.route('/zobacz_kandydata/<numer>')
def zobacz_kandydata_okreg(numer):
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("""SELECT kom.nazwa_komitetu, k.idkandydat, k.imie, k.nazwisko from kandydat k
    inner join lista l on k.idkandydat=l.idkandydat
    inner join komitet kom on kom.idkomitet=l.idkomitet
    inner join kandydat_w_okregu kwo on kwo.idkandydat=k.idkandydat
    where kwo.idokreg_wyborczy = (%s)
    order by kom.idkomitet;""",(numer,))
    kandydaci = kursor.fetchall()
    kursor.execute("SELECT * FROM komitet ORDER BY idkomitet;")
    komitety = kursor.fetchall()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(numer,))
    okreg = kursor.fetchone()
    conn.close()
    return render_template('zobacz_kandydata_okreg.html', kandydaci=kandydaci, numer=okreg[0], lokalizacja=okreg[1])

@app.route('/zobacz_kandydata')
def zobacz_kandydata():
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("""SELECT kom.nazwa_komitetu, k.idkandydat, k.imie, k.nazwisko from kandydat k
    inner join lista l on k.idkandydat=l.idkandydat
    inner join komitet kom on kom.idkomitet=l.idkomitet
    order by kom.idkomitet;""")
    kandydaci = kursor.fetchall()
    conn.close()
    return render_template('zobacz_kandydata.html', kandydaci=kandydaci)

@app.route('/edytuj_kandydata/<numer>',methods=['GET', 'POST'])
def edytuj_kandydata(numer):
    form = forms.EdytujKandydata(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        update.kandydat(kursor, form.numer_listy.data, form.id.data, form.noweid.data, form.imie.data, form.nazwisko.data) 
        conn.commit()
        conn.close()
        flash('Dokonano zmiany!')
        return redirect(url_for('zobacz_kandydata_okreg',numer=numer))
    conn = polacz()
    kursor = conn.cursor()
    kursor.execute("""SELECT kom.nazwa_komitetu, k.idkandydat, k.imie, k.nazwisko from kandydat k
    inner join lista l on k.idkandydat=l.idkandydat
    inner join komitet kom on kom.idkomitet=l.idkomitet
    inner join kandydat_w_okregu kwo on kwo.idkandydat=k.idkandydat
    where kwo.idokreg_wyborczy = (%s)
    order by kom.idkomitet;""",(numer,))
    kandydaci = kursor.fetchall()
    kursor.execute("SELECT * FROM komitet ORDER BY idkomitet;")
    komitety = kursor.fetchall()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(numer,))
    okreg = kursor.fetchone()
    conn.close()
    return render_template('edytuj_kandydata.html', form=form, komitety=komitety, kandydaci=kandydaci, numer=okreg[0], lokalizacja=okreg[1])

@app.route('/menu_komisarz/<numer>')
def menu_komisarz(numer):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(numer,))
    okreg = kursor.fetchone()
    conn.close()
    return render_template('menu_komisarz.html', numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])

#http://samorzad2014.pkw.gov.pl/357_rady_woj/0/2604
@app.route('/protokol_okreg/<numer>')
def protokol_okreg(numer):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM policz_glosy_w_okregu(%s)""",(numer,))
    conn.commit()
    kursor.execute("""SELECT * FROM protokol_w_okregu WHERE idokreg_wyborczy = (%s);""", (numer,))
    protokol = kursor.fetchall()
    kursor.execute("""SELECT * FROM frekwencja_w_obwodach WHERE idokreg_wyborczy = (%s);""",(numer,))
    frekwencja = kursor.fetchall()
    kursor.execute("""SELECT sum(sum) FROM frekwencja_w_obwodach WHERE idokreg_wyborczy = (%s);""",(numer,))
    frekwencja_w_okregu = kursor.fetchone()
    kursor.execute("""SELECT idkomitet, nazwa_komitetu, sum(liczba_glosow) FROM protokol_w_okregu where idokreg_wyborczy = (%s)
     GROUP BY idkomitet, nazwa_komitetu ORDER BY idkomitet;""",(numer,))
    komitety = kursor.fetchall()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(numer,))
    okreg = kursor.fetchone()
    wyniki = {element[1]: element[5]/frekwencja_w_okregu[0]*100 for element in protokol}
    print(frekwencja)
    conn.close()
    return render_template('protokol_okreg.html', numer=numer,
     protokol=protokol, frekwencja=frekwencja, komitety=komitety, frekwencja_w_okregu=frekwencja_w_okregu[0],
     komisarz=okreg[2], lokalizacja=okreg[1], wyniki = wyniki)

@app.route('/obwody_menu/<idokregu>')
def obwody_menu(idokregu):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(idokregu,))
    okreg = kursor.fetchone()
    conn.close()
    return render_template('obwody_menu.html', numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])

@app.route('/dodaj_obwod/<idokregu>', methods=['GET', 'POST'])
def dodaj_obwod(idokregu):
    form = forms.DodajObwod(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        insert.obwod_wyborczy_komisja(kursor, idokregu, form.lokalizacja.data,
            form.imie.data, form.nazwisko.data, form.afiliacja.data)
        conn.commit()
        conn.close()
        flash("Dodano!")
        return redirect(url_for('dodaj_obwod', idokregu=idokregu))
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(idokregu,))
    okreg = kursor.fetchone()
    # kursor.execute("""SELECT * FROM obwod_wyborczy WHERE idokreg_wyborczy = (%s) ORDER BY idobwod_wyborczy;""",(idokregu,))
    # obwody = kursor.fetchall()
    kursor.execute("""SELECT obw.idobwod_wyborczy, obw.lokalizacja, czk.idczlonek_komisji, 
        czk.imie, czk.nazwisko, czk.afiliacja FROM czlonek_komisji czk
        inner join  komisja k on k.idczlonek_komisji=czk.idczlonek_komisji
        inner join  obwod_wyborczy obw on obw.idobwod_wyborczy=k.idobwod_wyborczy
        WHERE obw.idokreg_wyborczy = (%s)
        ORDER BY obw.idobwod_wyborczy;""", (idokregu,))
    obwody= kursor.fetchall()
    conn.close()
    return render_template('dodaj_obwod.html',form=form, obwody=obwody, numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])

@app.route('/zobacz_obwod/<idokregu>')
def zobacz_obwod(idokregu):
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(idokregu,))
    okreg = kursor.fetchone()
    kursor.execute("""SELECT obw.idobwod_wyborczy, obw.lokalizacja, czk.idczlonek_komisji, 
        czk.imie, czk.nazwisko, czk.afiliacja FROM czlonek_komisji czk
        inner join  komisja k on k.idczlonek_komisji=czk.idczlonek_komisji
        inner join  obwod_wyborczy obw on obw.idobwod_wyborczy=k.idobwod_wyborczy
        WHERE obw.idokreg_wyborczy = (%s)
        ORDER BY obw.idobwod_wyborczy;""", (idokregu,))
    obwody= kursor.fetchall()
    conn.close()
    return render_template('zobacz_obwod.html', obwody=obwody, numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])



@app.route('/edytuj_obwod/<idokregu>', methods=['GET', 'POST'])
def edytuj_obwod(idokregu):
    form = forms.EdytujObwod(request.form)
    if request.method == 'POST' and form.validate():
        conn = polacz()
        kursor = conn.cursor()
        update.obwod_wyborczy_komisja(kursor, form.id.data, form.noweid.data, form.noweidokregu.data, form.lokalizacja.data,
            form.imie.data, form.nazwisko.data, form.afiliacja.data)
        conn.commit()
        conn.close()
        flash("Dokonano zmiany!")
        return redirect(url_for('zobacz_obwod', idokregu=idokregu))
    conn=polacz()
    kursor=conn.cursor()
    kursor.execute("""SELECT * FROM okreg_wyborczy WHERE idokreg_wyborczy = (%s);""",(idokregu,))
    okreg = kursor.fetchone()
    kursor.execute("""SELECT obw.idobwod_wyborczy, obw.lokalizacja, czk.idczlonek_komisji, 
        czk.imie, czk.nazwisko, czk.afiliacja FROM czlonek_komisji czk
        inner join  komisja k on k.idczlonek_komisji=czk.idczlonek_komisji
        inner join  obwod_wyborczy obw on obw.idobwod_wyborczy=k.idobwod_wyborczy
        WHERE obw.idokreg_wyborczy = (%s)
        ORDER BY obw.idobwod_wyborczy;""", (idokregu,))
    obwody= kursor.fetchall()
    conn.close()
    return render_template('edytuj_obwod.html', form=form, obwody=obwody, numer=okreg[0], komisarz=okreg[2], lokalizacja=okreg[1])
