from flask import render_template, redirect, url_for, request, flash

from app.admin import bp
from app.admin.forms import CennikEdit, MagazynEdit
from app.db.database import cennik_get, cennik_get_by_id, cennik_update, MagazynUpdate
from app.db.database import cennik_add, MagazynAdd, MagazynGet, MagazynGetById




@bp.route('/cennik')
def cennik():
    pozycje = cennik_get()
    return render_template('cennik.html', pozycje=pozycje)

@bp.route('/cennik/edycja/<int:id>', methods=['POST', 'GET'])
def cennik_edycja(id):
    data = cennik_get_by_id(id)
    form = CennikEdit()

    form.nazwa.data = data['nazwa']
    form.cena1.data = data['price1']
    form.cena2.data = data['price2']
    form.przedzial1.data = data['stage1']
    form.przedzial2.data = data['stage2']

    if form.validate_on_submit():

        cennik_update(
            id,
            request.form['nazwa'],
            request.form['przedzial1'],
            request.form['przedzial2'],
            request.form['cena1'],
            request.form['cena2'],
        )

        flash('Zaktulizowano cennik o nazwie %s'% request.form['nazwa'])
        return redirect(url_for('admin.cennik'))

    return render_template('cennik_edycja.html', form=form, site_name="Edycja cennika")

@bp.route('/cennik/dodaj', methods=['POST','GET'])
def cennik_dodaj():
    form = CennikEdit()

    if form.validate_on_submit():

        cennik_add(
            request.form['nazwa'],
            request.form['przedzial1'],
            request.form['przedzial2'],
            request.form['cena1'],
            request.form['cena2'],
        )

        flash('Dodano pozycje cennika o nazwie %s'% request.form['nazwa'])
        return redirect(url_for('admin.cennik'))

    return render_template('cennik_edycja.html', form=form, site_name="Dodanie pozycji cennika")

@bp.route('/magazyn/')
def magazyn():
    pozycje = MagazynGet()

    return render_template('magazyn.html', pozycje=pozycje)

@bp.route('/magazyn/dodaj', methods=['POST', 'GET'])
def magazyn_dodaj():
    cennik = cennik_get()
    form = MagazynEdit()

    cennik_choices = [(i['cennik_id'], i['nazwa']) for i in cennik]

    form.price.choices = cennik_choices

    if form.validate_on_submit():
        MagazynAdd(
            request.form['nazwa'],
            request.form['typ'],
            request.form['ean'],
            request.form['rozmiar'],
            request.form['price'],
            request.form['wartosc']
        )

        flash('Dodano pozycje do magazynu o nazwie %s'% request.form['nazwa'])
        return redirect(url_for('admin.magazyn'))


    return render_template('magazyn_form.html', form=form)

@bp.route('/magazyn/edytuj/<item_id>', methods=['POST', 'GET'])
def magazyn_edytuj(item_id):
    cennik = cennik_get()
    form = MagazynEdit()
    data = MagazynGetById(item_id)

    cennik_choices = [(i['cennik_id'], i['nazwa']) for i in cennik]
    form.price.choices = cennik_choices

    form.price.default = data['price']
    form.typ.default = data['typ']
    form.process()

    form.nazwa.data = data['nazwa']
    form.ean.data = data['ean']
    form.rozmiar.data = data['rozmiar']
    form.wartosc.data = data['wartosc']

    if request.method == 'POST':
        MagazynUpdate(
            item_id,
            request.form['nazwa'],
            request.form['typ'],
            request.form['ean'],
            request.form['rozmiar'],
            request.form['price'],
            request.form['wartosc']
        )
        flash('Zapisano zmiany w pozycji: %s' % request.form['nazwa'])
        return redirect(url_for('admin.magazyn'))

    return render_template('magazyn_form.html', form=form)
