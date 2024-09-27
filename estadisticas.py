from datetime import datetime
from db import Database
import matplotlib.pyplot as plt

class Estadisticas:
    def __init__(self, db):
        self.db = db

    def total_ventas(self):
        query = """SELECT SUM(cantidad * precio_unitario) FROM ventas"""
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchone()[0]
        return result if result is not None else 0

    def total_compras(self):
        query = """SELECT SUM(cantidad * precio_unitario) FROM compras"""
        self.db.cursor.execute(query)
        result = self.db.cursor.fetchone()[0]
        return result if result is not None else 0

    def productos_mas_vendidos(self, top_n=5):
        query = """
            SELECT p.nombre, COUNT(v.producto_id) AS veces_vendido
            FROM productos p
            JOIN ventas v ON p.id = v.producto_id
            GROUP BY p.id, p.nombre
            ORDER BY veces_vendido DESC
            LIMIT ?
        """
        self.db.cursor.execute(query, (top_n,))
        return self.db.cursor.fetchall()

    def ventas_por_mes(self):
        query = """
            SELECT STRFTIME('%Y-%m', fecha) AS mes, 
                   SUM(cantidad * precio_unitario) AS total
            FROM ventas
            GROUP BY mes
            ORDER BY mes
        """
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def compras_por_mes(self):
        query = """
            SELECT STRFTIME('%Y-%m', fecha) AS mes, 
                   SUM(cantidad * precio_unitario) AS total
            FROM compras
            GROUP BY mes
            ORDER BY mes
        """
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def generar_grafico_barras_ventas_compras(self, ventas_mensuales, compras_mensuales):
        meses = sorted(set([mes[0] for mes in ventas_mensuales + compras_mensuales]))
        ventas = [next((v[1] for v in ventas_mensuales if v[0] == mes), 0) for mes in meses]
        compras = [next((c[1] for c in compras_mensuales if c[0] == mes), 0) for mes in meses]

        plt.figure(figsize=(12, 6))
        plt.bar(meses, ventas, label='Ventas')
        plt.bar(meses, compras, bottom=ventas, label='Compras')
        plt.xlabel('Mes')
        plt.ylabel('Monto ($)')
        plt.title('Ventas vs Compras por Mes')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def generar_grafico_pie_productos_mas_vendidos(self, productos_top):
        labels = [nombre for nombre, _ in productos_top]
        sizes = [veces_vendido for _, veces_vendido in productos_top]

        plt.figure(figsize=(10, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Productos Más Vendidos')
        plt.axis('equal')  
        plt.show()

