from flask import session, flash
import pickle

from app.db.database import GetWypozyczenieByID,MagazynGetByEAN, WypozyczeniePodmiana
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


class Podmiana:
    session_key = 'podmiana'

    def __init__(self, id):
        data = GetWypozyczenieByID(id)
        self.pozycje = {x['ean']: x['nazwa'] for x in data['pozycje']}
        self.pozycje_minus = {}
        self.pozycje_add = {}
        self.wypozyczenia_id = data['info']['wypozyczenie_id']
        self.info = {
            'klient_name': data['info']['klient_name'],
            'klient_dowod': data['info']['klient_dowod'],
            'price': data['info']['price']
        }

    def remove_poz(self, ean):
        self.pozycje_minus[ean] = self.pozycje[ean]
        #except IndexError:
            #flash("Nie możesz usunąć pozycji która nie była w tym wypożyczeniu! ")

    def add_poz(self, ean):
        if ean in self.pozycje:
            flash("Nie możesz dodać pozycji kóra już jest w tym wypożyczeniu")
        data = MagazynGetByEAN(ean)
        self.pozycje_add[ean] = data['nazwa']

    def make_switch(self):
        WypozyczeniePodmiana(self.pozycje_minus, self.pozycje_add, self.wypozyczenia_id)

    @staticmethod
    def get(id):
        try:
            return pickle.loads(session[Podmiana.session_key])
        except KeyError:
            if id:
                return Podmiana(id)

    @staticmethod
    def save(obj):
        session[Podmiana.session_key] = pickle.dumps(obj)
        session.modified = True

    @staticmethod
    def clear():
        session.pop(Podmiana.session_key, None)




