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

def MagazynAdd(nazwa, typ, ean, rozmiar, price, wartosc):
    conn = GetConnection()
    c = conn.cursor()
    c.execute('''INSERT INTO items (nazwa, typ, ean, rozmiar, price, wartosc) VALUES 
                    ('%s', '%s', '%s', '%s', %d, '%s')''' % (nazwa, typ, ean, rozmiar, int(price), wartosc))

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

    c.execute(''' SELECT item_id, nazwa, typ, ean, rozmiar, price, wartosc FROM items WHERE item_id = %d ''' % int(id))
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


def MagazynUpdate(id, nazwa, typ, ean, rozmiar, price, wartosc):
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute("UPDATE items SET nazwa= '%s', typ= '%s', ean= '%s', rozmiar= '%s', price= %d, wartosc= '%s' WHERE item_id = %d" %
              (nazwa, typ, ean, rozmiar, int(price), wartosc, int(id)))
    conn.commit()
    conn.close()


def WypozyczenieAdd(klient_name, klient_dowod, wypozyczenie_od, wypozyczenie_do, wypozyczenie_godz_od,
                    wypozyczenie_godz_do, price, pozycje, klient_tel):

    conn = GetConnection()
    c = conn.cursor()
    c.execute('''INSERT INTO wypozyczenia (klient_name, klient_dowod, wypozyczenie_od, wypozyczenie_do, wypozyczenie_godz_od, 
                    wypozyczenie_godz_do, price, oddano, data_utworzenia, klient_tel) VALUES 
                    ('%s', '%s', '%s', '%s', '%s', '%s', %d, 0, '%s', '%s')''' % (klient_name, klient_dowod, wypozyczenie_od,
                                                                      wypozyczenie_do, wypozyczenie_godz_od,
                                                                       wypozyczenie_godz_do, int(price), str(gettms()), klient_tel))

    wyp_id = c.lastrowid
    poz = []
    for key, item in pozycje.items():
        temp = (item['item_id'], wyp_id, item['ean'], item['nazwa'], item['cena'])
        poz.append(temp)

    c.executemany('INSERT INTO wypozyczeniaitemsactive (item_id, wypozyczenie_id, ean, nazwa, cena) VALUES (?,?,?,?,?)', poz)
    conn.commit()
    conn.close()

    return wyp_id


def GetWypozyczeniaAktywne():
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute('SELECT * FROM wypozyczenia WHERE oddano = 0')
    data = c.fetchall()

    conn.close()
    return data

def GetWypozyczeniaWszystkie():
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute('SELECT * FROM wypozyczenia')
    data = c.fetchall()

    conn.close()
    return data

def GetWypoczyenieByEAN(ean):
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute("SELECT * FROM wypozyczeniaitemsactive WHERE ean = '%s'"% ean)
    data = c.fetchone()

    conn.close()
    return data

def GetWypozyczenieByID(id):
    return_data = {}
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute("SELECT * FROM wypozyczenia WHERE wypozyczenie_id = %s" % id)
    data = c.fetchone()

    return_data['info'] = data

    if data['oddano'] == 0:
        c.execute("""SELECT wyp.item_id,
                            wyp.nazwa,
                            wyp.cena,
                            i.wartosc
                     FROM wypozyczeniaitemsactive AS wyp
                     LEFT JOIN items AS i ON wyp.item_id = i.item_id
                     WHERE wypozyczenie_id = %s""" % id)
    else:
        c.execute("""SELECT wyp.item_id,
                            wyp.nazwa,
                            wyp.cena,
                            i.wartosc
                     FROM wypozyczeniaitems AS wyp
                     LEFT JOIN items AS i ON wyp.item_id = i.item_id
                     WHERE wypozyczenie_id = %s""" % id)

    data = c.fetchall()
    return_data['pozycje'] = data
    return return_data

def GetItemsPriceByEANs(id):
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute("""SELECT wia.item_id,
                        wia.wypozyczenie_id, 
                        i.price,
                        c.price1
                FROM wypozyczeniaitemsactive as wia 
                LEFT JOIN items AS i ON wia.item_id = i.item_id
                LEFT JOIN cennik AS c ON i.price = c.cennik_id
                WHERE wia.wypozyczenie_id = %s"""% id)
    data = c.fetchall()
    conn.close()
    return data

def WypozyczenieOddajById(id, doplata):
    conn = GetConnection(True)
    c = conn.cursor()
    c.execute("""UPDATE wypozyczenia SET oddano = 1 WHERE wypozyczenie_id = %d """% id)
    c.execute("""SELECT price FROM wypozyczenia WHERE wypozyczenie_id = %d"""% id)
    data = c.fetchone()
    price = int(data['price']) + int(doplata)
    c.execute("""UPDATE wypozyczenia SET price = %d WHERE wypozyczenie_id = %d """% (price, id))
    c.execute("""INSERT INTO wypozyczeniaitems SELECT * FROM wypozyczeniaitemsactive WHERE wypozyczenie_id = %d"""% id)
    c.execute("""DELETE FROM wypozyczeniaitemsactive WHERE wypozyczenie_id = %d """% id)

    conn.commit()
    conn.close()
