import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              nombre TEXT NOT NULL,
                              cantidad INTEGER NOT NULL,
                              precio_compra REAL NOT NULL,
                              precio_venta REAL NOT NULL)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS ventas
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              producto_id INTEGER NOT NULL,
                              fecha DATE NOT NULL,
                              cantidad INTEGER NOT NULL,
                              precio_unitario REAL NOT NULL,
                              FOREIGN KEY(producto_id) REFERENCES productos(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS compras
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              producto_id INTEGER NOT NULL,
                              fecha DATE NOT NULL,
                              cantidad INTEGER NOT NULL,
                              precio_unitario REAL NOT NULL,
                              FOREIGN KEY(producto_id) REFERENCES productos(id))''')
        self.conn.commit()

    def execute_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    def fetch_all(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()
