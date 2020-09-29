import sqlite3
from datetime import datetime
from config import Config


def GetConnection(row=False):
    conn = sqlite3.connect('database.db')
    if row:
        conn.row_factory = sqlite3.Row
    return conn

#
# Daty
#

def gettms():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

#
#   Obsługa cennika
#


def CennikAdd(nazwa, stage1, stage2, price1, price2):
    conn = GetConnection()
    c = conn.cursor()
    c.execute('''INSERT INTO cennik (nazwa, stage1, stage2, price1, price2) VALUES 
                    ('%s', %d, %d, %d, %d)''' % (nazwa, int(stage1), int(stage2), int(price1), int(price2)))

    conn.commit()
    conn.close()


def CennikGet():
    conn = GetConnection(True)
    c = conn.cursor()

    c.execute(''' SELECT cennik_id, nazwa, stage1, stage2, price1, price2 FROM cennik''')
    data = c.fetchall()
    conn.close()

    return data


def CennikGetById(id):
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute(" SELECT cennik_id, nazwa, stage1, stage2, price1, price2 FROM cennik WHERE cennik_id = '%s'" % id)
    data = c.fetchone()
    conn.close()

    return data


def CennikUpdate(id, nazwa, stage1, stage2, price1, price2):
    conn = GetConnection(True)
    c = conn.cursor()

    c.execute("UPDATE cennik SET nazwa= '%s', stage1= %d, stage2= %d, price1= %d, price2= %d WHERE cennik_id = %d" %
              (nazwa, int(stage1), int(stage2), int(price1), int(price2), int(id)))
    conn.commit()
    conn.close()


#
#   Magazyn
#

def MagazynAdd(nazwa, typ, ean, rozmiar, price):
    conn = GetConnection()
    c = conn.cursor()
    c.execute('''INSERT INTO items (nazwa, typ, ean, rozmiar, price) VALUES 
                    ('%s', '%s', '%s', '%s', %d)''' % (nazwa, typ, ean, rozmiar, int(price)))

    conn.commit()
    conn.close()


def MagazynGet():
    conn = GetConnection(True)
    c = conn.cursor()

    c.execute(''' SELECT    i.item_id,
                            i.nazwa, 
                            i.typ, 
                            i.ean, 
                            i.rozmiar, 
                            i.price,
                            c.nazwa AS cennik_nazwa,
                            c.cennik_id AS cennik_id
                            FROM items AS i
                            LEFT JOIN cennik AS c ON i.price = c.cennik_id''')
    data = c.fetchall()
    conn.close()

    return data


def MagazynGetById(id):
    conn = GetConnection(True)
    c = conn.cursor()

    c.execute(''' SELECT item_id, nazwa, typ, ean, rozmiar, price FROM items WHERE item_id = %d ''' % int(id))
    data = c.fetchone()
    conn.close()

    return data


def MagazynGetByEAN(ean):
    conn = GetConnection(True)
    c = conn.cursor()

    c.execute(''' SELECT    i.item_id,
                            i.nazwa, 
                            i.typ,
                            i.ean, 
                            i.rozmiar, 
                            i.price,
                            c.stage1,
                            c.stage2,
                            c.price1,
                            c.price2 
                            FROM items as i
                            LEFT JOIN cennik AS c ON i.price = c.cennik_id
                            WHERE ean = '%s' ''' % ean)
    data = c.fetchone()
    conn.close()

    return data


def MagazynUpdate(id, nazwa, typ, ean, rozmiar, price):
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute("UPDATE items SET nazwa= '%s', typ= '%s', ean= '%s', rozmiar= '%s', price= %d WHERE item_id = %d" %
              (nazwa, typ, ean, rozmiar, int(price), int(id)))
    conn.commit()
    conn.close()


def WypozyczenieAdd(klient_name, klient_dowod, wypozyczenie_od, wypozyczenie_do, wypozyczenie_godz_od,
                    wypozyczenie_godz_do, price, pozycje):

    conn = GetConnection()
    c = conn.cursor()
    c.execute('''INSERT INTO wypozyczenia (klient_name, klient_dowod, wypozyczenie_od, wypozyczenie_do, wypozyczenie_godz_od, 
                    wypozyczenie_godz_do, price, oddano, data_utworzenia) VALUES 
                    ('%s', '%s', '%s', '%s', '%s', '%s', %d, 0, '%s')''' % (klient_name, klient_dowod, wypozyczenie_od,
                                                                      wypozyczenie_do, wypozyczenie_godz_od,
                                                                       wypozyczenie_godz_do, int(price), str(gettms())))

    wyp_id = c.lastrowid
    poz = []
    for key, item in pozycje.items():
        temp = (item['item_id'], wyp_id, item['ean'], item['nazwa'], item['cena'])
        poz.append(temp)

    c.executemany('INSERT INTO wypozyczeniaitemsactive (item_id, wypozyczenie_id, ean, nazwa, cena) VALUES (?,?,?,?,?)', poz)
    conn.commit()
    conn.close()


def CREATE_WYPOZYCZENIE_RZECZY_AKTYWNE():
    pass


def CREATE_WYPOZYCZENIE_RZECZY():
    pass


def CREATE_WYPOZYCZENIE_RZECZY_TERAZ():
    pass
