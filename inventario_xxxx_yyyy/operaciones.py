from db import Database
from datetime import datetime

class Operaciones:
    def __init__(self, db):
        self.db = db

    def agregar_producto(self, nombre, cantidad, precio_compra, precio_venta):
        query = "INSERT INTO productos (nombre, cantidad, precio_compra, precio_venta) VALUES (?, ?, ?, ?)"
        self.db.execute_query(query, (nombre, cantidad, precio_compra, precio_venta))

    def eliminar_producto(self, id_producto):
        query = "DELETE FROM productos WHERE id = ?"
        self.db.execute_query(query, (id_producto,))

    def modificar_producto(self, id_producto, nuevo_nombre=None, nueva_cantidad=None, nuevo_precio_compra=None, nuevo_precio_venta=None):
        campos_actualizados = []
        valores = []

        if nuevo_nombre:
            campos_actualizados.append("nombre = ?")
            valores.append(nuevo_nombre)
        if nueva_cantidad:
            campos_actualizados.append("cantidad = ?")
            valores.append(nueva_cantidad)
        if nuevo_precio_compra:
            campos_actualizados.append("precio_compra = ?")
            valores.append(nuevo_precio_compra)
        if nuevo_precio_venta:
            campos_actualizados.append("precio_venta = ?")
            valores.append(nuevo_precio_venta)

        if campos_actualizados:
            set_clause = ", ".join(campos_actualizados)
            query = f"UPDATE productos SET {set_clause} WHERE id = ?"
            valores.append(id_producto)
            self.db.execute_query(query, tuple(valores))

    def listar_productos(self):
        query = "SELECT * FROM productos ORDER BY id ASC"
        return self.db.fetch_all(query)

    def vender_producto(self, id_producto, cantidad_a_vender):
        query = "SELECT * FROM productos WHERE id = ?"
        producto = self.db.fetch_all(query, (id_producto,))
        
        if producto:
            query = "INSERT INTO ventas (producto_id, fecha, cantidad, precio_unitario) VALUES (?, ?, ?, ?)"
            self.db.execute_query(query, (id_producto, datetime.now().strftime("%Y-%m-%d"), cantidad_a_vender, producto[0][4]))
            
            query = "UPDATE productos SET cantidad = cantidad - ? WHERE id = ?"
            self.db.execute_query(query, (cantidad_a_vender, id_producto))
        else:
            raise ValueError("Producto no encontrado")

    def comprar_producto(self, id_producto, cantidad_a_comprar):
        query = "SELECT * FROM productos WHERE id = ?"
        producto = self.db.fetch_all(query, (id_producto,))
        
        if producto:
            query = "INSERT INTO compras (producto_id, fecha, cantidad, precio_unitario) VALUES (?, ?, ?, ?)"
            self.db.execute_query(query, (id_producto, datetime.now().strftime("%Y-%m-%d"), cantidad_a_comprar, producto[0][3]))
            
            query = "UPDATE productos SET cantidad = cantidad + ? WHERE id = ?"
            self.db.execute_query(query, (cantidad_a_comprar, id_producto))
        else:
            raise ValueError("Producto no encontrado")

    def generar_estadisticas(self):
        queries = [
            ("COUNT(*)", "productos"),
            ("SUM(cantidad)", "productos"),
            ("AVG(precio_compra)", "productos"),
            ("AVG(precio_venta)", "productos"),
            ("SUM(cantidad * precio_venta)", "productos"),
            ("COUNT(*)", "ventas"),
            ("SUM(cantidad * precio_unitario)", "ventas"),
            ("COUNT(*)", "compras"),
            ("SUM(cantidad * precio_unitario)", "compras")
        ]

        resultados = []
        for query, table in queries:
            q = f"SELECT {query} FROM {table}"
            resultado = self.db.fetch_all(q)[0][0]
            resultados.append(resultado if resultado is not None else 0)

        return resultados
