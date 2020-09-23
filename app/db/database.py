import sqlite3

from config import Config

def GetConnection(row=False):
    conn = sqlite3.connect('database.db')
    if row:
        conn.row_factory = sqlite3.Row
    return conn


#
#   Obsługa cennika
#


def CennikAdd(nazwa, stage1, stage2, price1, price2):
    conn = GetConnection()
    c = conn.cursor()
    c.execute('''INSERT INTO cennik (nazwa, stage1, stage2, price1, price2) VALUES 
                    ('%s', %d, %d, %d, %d)'''% (nazwa, int(stage1), int(stage2), int(price1), int(price2)))

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