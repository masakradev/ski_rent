from flask import render_template, flash
from app.dashboard import bp

from app.db.database import *

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/dodaj_wypozyczenie')
def dodaj_wypozyczenie():
    return render_template('dodaj_wypozyczenie.html')

@bp.route('/oddanie_wypozyczenia')
def oddanie_wypozyczenia():
    return render_template('oddanie_wypozyczenia.html')

@bp.route('/wypozyczenia_lista_dzisiaj')
def wypozyczenia_lista_dzisiaj():
    return render_template('wypozyczenia_lista_dzisiaj.html')

@bp.route('/wypozyczenia_lista_wszystkie')
def wypozyczenia_lista_wszystkie():
    return render_template('wypozyczenia_lista_wszystkie.html')