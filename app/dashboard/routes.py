import datetime
from decimal import Decimal


from flask import render_template, flash, redirect, url_for, request, jsonify, send_file

from app.dashboard import bp
from app.dashboard.forms import WypozyczenieDodaj, WypozyczeniePozycja, EANSearch, WypozyczenieOddajDoplata
from app.dashboard.models import Wypozyczenie, Podmiana

from app.db.database import MagazynGetByEAN, WypozyczenieAdd, GetWypozyczeniaAktywne
from app.db.database import GetWypozyczeniaWszystkie, GetAktywneWypoczyenieByEAN, IndexCountsGet
from app.db.database import GetWypozyczenieByID, GetItemsPriceByEANs, WypozyczenieOddajById

from app.pdf.generator import create_pdf


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


@bp.route('/umowa/<int:id>')
def get_pdf(id):
    try:
        return send_file('static/pdf/{}.pdf'.format(id))
    except FileNotFoundError:
        create_pdf(id)
        return send_file('static/pdf/{}.pdf'.format(id))

@bp.route('/')
def index():
    data = IndexCountsGet()
    return render_template('index.html', data = data)


@bp.route('/dodaj_wypozyczenie', methods=['POST', 'GET'])
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

@bp.route('/dodaj_wypozyczenie_dalej', methods=['POST', 'GET'])
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

    wyp_od = " ".join([wyp.wypozyczenie_od,wyp.wypozyczenie_godz_od])
    wyp_do = " ".join([wyp.wypozyczenie_do,wyp.wypozyczenie_godz_do])

    days_compare = datetime.datetime.strptime(wyp_do, '%Y-%m-%d %H:%M') - \
                   datetime.datetime.strptime(wyp_od, '%Y-%m-%d %H:%M')

    wyp_count_days = int(days_compare.days)
    wyp_count_hours = days_compare.seconds /3600

    for k, i in wyp.pozycje.items():
        poz = WypozyczeniePozycja()
        poz.key = k
        poz.nazwa = i['nazwa']
        poz.ean = k
        poz.rozmiar = i['rozmiar']

        if wyp_count_days > 0:
            cena = wyp_count_days * i['cena2'] + wyp_count_hours * i['cena1']
        else:
            if wyp_count_hours > i['stage2']:
                cena = i['cena2']
            else:
                cena = wyp_count_hours * i['cena1']

        poz.cena = cena
        wyp.pozycje[k]['cena'] = cena

        form.pozycje_form.append_entry(poz)

    wyp.CountThePrices()
    form.cena.data = int(wyp.cena)

    if request.method == 'POST':
        wyp.update(request.form)
        Wypozyczenie.save(wyp)

        data = WypozyczenieAdd(
            wyp.klient_name,
            wyp.klient_dowod,
            wyp.wypozyczenie_od,
            wyp.wypozyczenie_do,
            wyp.wypozyczenie_godz_od,
            wyp.wypozyczenie_godz_do,
            wyp.cena,
            wyp.pozycje,
            wyp.nr_tel
        )

        create_pdf(
            data #Id wypożyczenia
        )

        return redirect(url_for('dashboard.wypozyczenie', id=data))

    return render_template('dodaj_wypozyczenie_dalej.html', form=form)


@bp.route('/wypozyczenie/<int:id>')
def wypozyczenie(id):
    data = GetWypozyczenieByID(id)
    if data is None:
        flash('Nie ma takiego zlecenia')
        return redirect(url_for('dashboard.index'))
    return render_template('wypozyczenie.html', info=data['info'], pozycje=data['pozycje'])

@bp.route('/oddanie_wypozyczenia', methods=['POST', 'GET'])
def oddanie_wypozyczenia():
    form = EANSearch()

    if form.validate_on_submit():
        data = GetAktywneWypoczyenieByEAN(form.kod.data)
        if data is None:
            flash("Nie ma takiego kodu lub brak wypożyczenia z takim przedmiotem")
        else:
            return redirect(url_for('dashboard.oddanie_wypozyczenia_dalej', id=data['wypozyczenie_id']))
    return render_template('oddanie_wypozyczenia.html', form=form)

@bp.route('/oddanie_wypozyczenia_dalej/<int:id>', methods=['POST', 'GET'])
def oddanie_wypozyczenia_dalej(id):
    form = WypozyczenieOddajDoplata()
    data = GetWypozyczenieByID(id)
    info = data['info']
    pozycje = data['pozycje']

    if data is None:
        flash('Nie ma takiego zlecenia')
        return redirect(url_for('dashboard.index'))

    now = datetime.datetime.now()

    day_now = "%s-%s-%s %s:%s" % (now.year, now.month, now.day, now.hour, now.minute)
    day_do = " ".join([info['wypozyczenie_do'], info['wypozyczenie_godz_do']])

    days_compare = datetime.datetime.strptime(day_now, '%Y-%m-%d %H:%M') - datetime.datetime.strptime(
        day_do, '%Y-%m-%d %H:%M')


    if days_compare.days > 0:
        minutes_late = int(days_compare.days * 1440) + int(days_compare.seconds/60)
    else:
        minutes_late = days_compare.seconds / 60

    ret = ""

    if days_compare.days < 0:
        ret = "Brak dopłaty"
    else:
        if minutes_late < 30:
            ret = "Spóźnienie o %s minut"% minutes_late
        else:
            cena = 0
            cennik = GetItemsPriceByEANs(id)
            for x in cennik:
               cena += int(x['price1'] * minutes_late/60)
            form.doplata.data = cena
            if days_compare.days > 0:
                ret = "Spóźnienie o %s minut (%d dni)"% (minutes_late, minutes_late/1440)
            else:
                ret = "Spóźnienie o %s minut (%d godzin)" % (minutes_late, minutes_late / 60)

    if form.validate_on_submit():
        WypozyczenieOddajById(id, request.form.get('doplata'))
        return redirect(url_for('dashboard.index'))

    return render_template('oddanie_wypozyczenia_dalej.html', info=info, pozycje=pozycje, rozliczenie=ret, form=form)

@bp.route('/wypozyczenia_lista_aktywne')
def wypozyczenia_lista_aktywne():
    pozycje = GetWypozyczeniaAktywne()

    return render_template('wypozyczenia_lista_aktywne.html', pozycje=pozycje)

@bp.route('/wypozyczenia_lista_wszystkie')
def wypozyczenia_lista_wszystkie():
    pozycje = GetWypozyczeniaWszystkie()
    return render_template('wypozyczenia_lista_wszystkie.html', pozycje=pozycje)

#
# Endpoint dla podmiany
#

@bp.route('/podmiana/api/add', methods=['POST'])
def podmiana_sprzetu_api_add():
    pod = Podmiana.get(False)
    ean = list(request.form.to_dict().keys())[0]

    pod.add_poz(ean)
    Podmiana.save(pod)
    return jsonify(False)

@bp.route('/podmiana/api/rem', methods=['POST'])
def podmiana_sprzetu_api_rem():
    pod = Podmiana.get(False)
    ean = list(request.form.to_dict().keys())[0]

    pod.remove_poz(ean)
    Podmiana.save(pod)
    return jsonify(False)
#
#  Podmiana
#

@bp.route('/podmiana', methods=['POST','GET'])
def podmiana_sprzetu():
    form = EANSearch()

    if form.validate_on_submit():
        data = GetAktywneWypoczyenieByEAN(form.kod.data)
        if data is None:
            flash("Nie ma takiego kodu lub brak wypożyczenia z takim przedmiotem")
        else:
            return redirect(url_for('dashboard.podmiana_sprzetu_edycja', id=data['wypozyczenie_id']))

    return render_template('podmiana.html', form=form)

@bp.route('/podmiana/edycja/<int:id>', methods=['POST','GET'])
def podmiana_sprzetu_edycja(id):
    pod = Podmiana.get(id)
    form = EANSearch()

    if request.method == 'POST':
        pod.make_switch()
        pod.clear()

    Podmiana.save(pod)
    return render_template('podmiana_edycja.html', form=form, poz_add=pod.pozycje_add, poz_minus=pod.pozycje_minus, info=pod.info)