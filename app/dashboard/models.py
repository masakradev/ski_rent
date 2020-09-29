from flask import session
import pickle

from app.dashboard.forms import WypozyczenieDodaj

class Wypozyczenie:
    session_key = 'pb_wypozyczenie'

    def __init__(self):
        self.klient_name = None
        self.klient_dowod = None
        self.wypozyczenie_od = None
        self.wypozyczenie_do = None
        self.wypozyczenie_godz_od = None
        self.wypozyczenie_godz_do = None
        self.nr_tel = None
        self.cena = None
        self.pozycje = {}

    def CountThePrices(self):
        price = 0
        for key, item in self.pozycje.items():
            price += item['cena']
            print(item['cena'])
        self.cena = price

    def delete_from_pozycje(self, key):
        del self.pozycje[key]

    @staticmethod
    def get():
        try:
            return pickle.loads(session[Wypozyczenie.session_key])
        except KeyError:
            return Wypozyczenie()

    @staticmethod
    def save(obj):
        session[Wypozyczenie.session_key] = pickle.dumps(obj)
        session.modified = True

    @staticmethod
    def clear():
        session.pop(Wypozyczenie.session_key, None)

    def update(self, form):
        if isinstance(form, WypozyczenieDodaj):
            f = form.to_dict()
        else:
            f = form
        print(f)
        self.klient_name = f['klient_nazwa']
        self.klient_dowod = f['klient_dowod']
        self.wypozyczenie_od = f['wypozyczenie_od']
        self.wypozyczenie_do = f['wypozyczenie_do']
        self.wypozyczenie_godz_od = f['wypozyczenie_od_godz']
        self.wypozyczenie_godz_do = f['wypozyczenie_do_godz']
        self.nr_tel = f['klient_nr_tel']

        try:
            self.cena = f['cena']
        except KeyError:
            self.cena = None

        pointer = 0

        while True:
            key = f.getlist('pozycje_form-{}-key'.format(pointer))
            try:
                key = key[0]
            except IndexError:
                break

            pointer += 1





