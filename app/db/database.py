import sqlite3

from config import Config

def GetConnection():
    conn = sqlite3.connect('database.db')
    return conn.cursor()

def test():
    pass

if __name__ = "__main__":
    test()