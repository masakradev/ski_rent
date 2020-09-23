from flask import render_template, redirect, url_for, request, flash

from app.admin import bp
from app.admin.forms import CennikEdit
from app.db.database import CennikGet, CennikGetById, CennikUpdate, CennikAdd


@bp.route('/cennik')
def cennik():
    pozycje = CennikGet()
    return render_template('cennik.html', pozycje=pozycje)

@bp.route('/cennik/edycja/<int:id>', methods=['POST','GET'])
def cennik_edycja(id):
    data = CennikGetById(id)
    form = CennikEdit()

    form.nazwa.data = data['nazwa']
    form.cena1.data = data['price1']
    form.cena2.data = data['price2']
    form.przedzial1.data = data['stage1']
    form.przedzial2.data = data['stage2']

    if form.validate_on_submit():

        CennikUpdate(
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

        CennikAdd(
            request.form['nazwa'],
            request.form['przedzial1'],
            request.form['przedzial2'],
            request.form['cena1'],
            request.form['cena2'],
        )

        flash('Dodano pozycje cennika o nazwie %s'% request.form['nazwa'])
        return redirect(url_for('admin.cennik'))

    return render_template('cennik_edycja.html', form=form, site_name="Dodanie pozycji cennika")