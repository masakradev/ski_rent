import datetime
from decimal import Decimal


from flask import render_template, flash, redirect, url_for, request, jsonify

from app.dashboard import bp
from app.dashboard.forms import WypozyczenieDodaj, WypozyczeniePozycja
from app.dashboard.models import Wypozyczenie
from app.db.database import MagazynGetByEAN, WypozyczenieAdd


@bp.route('/api/add', methods=['POST'])
def api_add():
    wyp = Wypozyczenie.get()
    ean = list(request.form.to_dict().keys())[0]
    data = MagazynGetByEAN(ean)

    wyp.pozycje[ean] = {
                    'nazwa': data['nazwa'],
                    'rozmiar': data['rozmiar'],
                    'ean': ean,
                    'item_id':data['item_id'],
                    'stage1': data['stage1'],
                    'stage2': data['stage2'],
                    'cena1': data['price1'],
                    'cena2': data['price2'],
                    'cena': 0
                }

    Wypozyczenie.save(wyp)
    return jsonify('true')

@bp.route('/api/remove_poz', methods=['POST'])
def api_remove_poz():
    wyp = Wypozyczenie.get()
    ean = list(request.form.to_dict().keys())[0]
    wyp.delete_from_pozycje(ean)

    Wypozyczenie.save(wyp)
    return jsonify('true')

@bp.route('/api/clear')
def api_clear():
    wyp = Wypozyczenie.get()
    wyp.clear()

    return redirect(url_for('dashboard.dodaj_wypozyczenie'))

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/dodaj_wypozyczenie', methods=['POST','GET'])
def dodaj_wypozyczenie():
    form = WypozyczenieDodaj()
    wyp = Wypozyczenie.get()

    form.klient_nazwa.data = wyp.klient_name
    form.klient_dowod.data = wyp.klient_dowod
    form.klient_nr_tel.data = wyp.nr_tel
    if wyp.wypozyczenie_od not in (None, ''):
        form.wypozyczenie_od.data = datetime.datetime.strptime(wyp.wypozyczenie_od, '%Y-%m-%d')
    if wyp.wypozyczenie_do not in (None, ''):
        form.wypozyczenie_do.data = datetime.datetime.strptime(wyp.wypozyczenie_do, '%Y-%m-%d')
    if wyp.wypozyczenie_godz_do not in (None, ''):
        form.wypozyczenie_do_godz.data = datetime.datetime.strptime(wyp.wypozyczenie_godz_do, '%H:%M')
    if wyp.wypozyczenie_godz_od not in (None, ''):
        form.wypozyczenie_od_godz.data = datetime.datetime.strptime(wyp.wypozyczenie_godz_od, '%H:%M')

    if request.method == 'POST':
        wyp.update(request.form)
        Wypozyczenie.save(wyp)
        return redirect(url_for('dashboard.dodaj_wypozyczenie_dalej'))

    return render_template('dodaj_wypozyczenie.html', form=form)

@bp.route('/dodaj_wypozyczenie_dalej', methods=['POST','GET'])
def dodaj_wypozyczenie_dalej():
    form = WypozyczenieDodaj()
    wyp = Wypozyczenie.get()

    form.klient_nazwa.data = wyp.klient_name
    form.klient_dowod.data = wyp.klient_dowod
    form.klient_nr_tel.data = wyp.nr_tel
    if wyp.wypozyczenie_od not in (None, ''):
        form.wypozyczenie_od.data = datetime.datetime.strptime(wyp.wypozyczenie_od, '%Y-%m-%d')
    if wyp.wypozyczenie_do not in (None, ''):
        form.wypozyczenie_do.data = datetime.datetime.strptime(wyp.wypozyczenie_do, '%Y-%m-%d')
    if wyp.wypozyczenie_godz_do not in (None, ''):
        form.wypozyczenie_do_godz.data = datetime.datetime.strptime(wyp.wypozyczenie_godz_do, '%H:%M')
    if wyp.wypozyczenie_godz_od not in (None, ''):
        form.wypozyczenie_od_godz.data = datetime.datetime.strptime(wyp.wypozyczenie_godz_od, '%H:%M')


    days_compare = datetime.datetime.strptime(wyp.wypozyczenie_do, '%Y-%m-%d') - datetime.datetime.strptime(wyp.wypozyczenie_od, '%Y-%m-%d')
    days = days_compare.days
    hours_compare = datetime.datetime.strptime(wyp.wypozyczenie_godz_do, '%H:%M') - datetime.datetime.strptime(wyp.wypozyczenie_godz_od, '%H:%M')
    hours = int(hours_compare.seconds)/3600

    for k, i in wyp.pozycje.items():
        poz = WypozyczeniePozycja()
        poz.key = k
        poz.nazwa = i['nazwa']
        poz.ean = k
        poz.rozmiar = i['rozmiar']
        #print(days * i['cena1'] + hours * i['cena2'])
        if hours < i['stage2'] and hours > 0:
            cena = days * i['cena2'] + hours * i['cena1']
        else:
            cena = 20

        poz.cena = cena
        wyp.pozycje[k]['cena'] = cena

        form.pozycje_form.append_entry(poz)

    wyp.CountThePrices()
    form.cena.data = int(wyp.cena)

    if request.method == 'POST':
        wyp.update(request.form)
        Wypozyczenie.save(wyp)

        WypozyczenieAdd(
            wyp.klient_name,
            wyp.klient_dowod,
            wyp.wypozyczenie_od,
            wyp.wypozyczenie_do,
            wyp.wypozyczenie_godz_od,
            wyp.wypozyczenie_godz_do,
            wyp.cena,
            wyp.pozycje
        )

        return redirect(url_for('dashboard.index'))

    return render_template('dodaj_wypozyczenie_dalej.html', form=form)

@bp.route('/oddanie_wypozyczenia')
def oddanie_wypozyczenia():
    return render_template('oddanie_wypozyczenia.html')

@bp.route('/wypozyczenia_lista_dzisiaj')
def wypozyczenia_lista_dzisiaj():
    return render_template('wypozyczenia_lista_dzisiaj.html')

@bp.route('/wypozyczenia_lista_wszystkie')
def wypozyczenia_lista_wszystkie():
    return render_template('wypozyczenia_lista_wszystkie.html')