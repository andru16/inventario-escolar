from db import Database
from datetime import datetime

class Operaciones:
    def __init__(self, db):
        self.db = db

    def agregar_categoria(self, nombre_categoria):
        query = "INSERT OR IGNORE INTO categorias (nombre) VALUES (?)"
        self.db.execute_query(query, (nombre_categoria,))

    def categoria_existe(self, nombre_categoria):
        query = "SELECT id FROM categorias WHERE nombre = ?"
        self.db.cursor.execute(query, (nombre_categoria,))
        return self.db.cursor.fetchone() is not None

    def seleccionar_categoria(self):
        query = "SELECT id, nombre FROM categorias ORDER BY nombre"
        self.db.cursor.execute(query)
        
        print("Seleccione una categoría:")
        categorias = self.db.cursor.fetchall()

        if not categorias:
            print("No existen categorías en la base de datos.")
            return None
    

        for i, (id, nombre) in enumerate(categorias, 1):
            print(f"{i}. {nombre}")
        
        while True:
            try:
                opcion = int(input("Ingrese el número de la categoría: "))
                if 1 <= opcion <= len(categorias):
                    selected_category = next((cat for cat in categorias if cat[0] == opcion ), None)
                    if selected_category:
                        return selected_category[0]
                    
                    break
                else:
                    print("Opción inválida. Por favor, ingrese un número válido.")
            except ValueError:
                print("Por favor, ingrese un número entero.")
                
    def listar_categorias(self):
        query = """
            SELECT c.id, c.nombre
            FROM categorias c
        """
        
        self.db.cursor.execute(query)
        categorias = self.db.cursor.fetchall()

        return categorias


    def producto_existe(self, id_producto):
        query = "SELECT id FROM productos WHERE id = ?"
        self.db.cursor.execute(query, (id_producto,))
        return self.db.cursor.fetchone()
    
    def obtener_precio_unitario(self, id_producto):
        query = "SELECT precio_venta FROM productos WHERE id = ?"
        self.db.cursor.execute(query, (id_producto,))
        return self.db.cursor.fetchone()

    def agregar_producto(self, nombre, categoria, cantidad, precio_compra, precio_venta):
        
        query_producto = """
            INSERT INTO productos (
                nombre,
                id_categoria,
                cantidad,
                precio_compra,
                precio_venta
            ) VALUES (?, ?, ?, ?, ?)
        """
        self.db.cursor.execute(query_producto, (
            nombre,
            categoria,
            cantidad,
            precio_compra,
            precio_venta
        ))
        self.db.conn.commit()

    def eliminar_producto(self, id_producto):
        
        query = "SELECT COUNT(*) FROM productos WHERE id = ?"
        self.db.cursor.execute(query, (id_producto,))
        resultado = self.db.cursor.fetchone()
        
        if resultado[0] == 0:
            print(f"El producto con ID {id_producto} no existe.")
            return
        
        # Si el producto existe, procedemos a eliminarlo
        delete_query = "DELETE FROM productos WHERE id = ?"
        self.db.cursor.execute(delete_query, (id_producto,))
        self.db.conn.commit()
    
        print(f"Producto con ID {id_producto} eliminado correctamente.")

    def modificar_producto(self, id_producto, nuevo_nombre=None, nuevo_id_categoria=None, nueva_cantidad=None, nuevo_precio_compra=None, nuevo_precio_venta=None):
        query = """
            UPDATE productos SET
                nombre = COALESCE(?, nombre),
                id_categoria = COALESCE(?, id_categoria),
                cantidad = COALESCE(?, cantidad),
                precio_compra = COALESCE(?, precio_compra),
                precio_venta = COALESCE(?, precio_venta)
            WHERE id = ?
        """
        self.db.cursor.execute(query, (
            nuevo_nombre,
            nuevo_id_categoria,
            nueva_cantidad,
            nuevo_precio_compra,
            nuevo_precio_venta,
            id_producto
        ))
        self.db.conn.commit()

    def listar_productos(self):
        query = """
            SELECT p.id, p.nombre, p.cantidad, p.precio_compra, p.precio_venta,
                   c.nombre AS categoria_nombre
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id
        """
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def vender_producto(self, id_producto, cantidad_a_vender):
        query_stock = "SELECT cantidad FROM productos WHERE id = ?"
        self.db.cursor.execute(query_stock, (id_producto,))
        stock_actual = self.db.cursor.fetchone()[0]
        
        if stock_actual < cantidad_a_vender:
            raise ValueError("No hay suficiente stock para realizar la venta")
        
        nueva_cantidad = stock_actual - cantidad_a_vender
        query_update_stock = "UPDATE productos SET cantidad = ? WHERE id = ?"
        self.db.cursor.execute(query_update_stock, (nueva_cantidad, id_producto))
        
        fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_registro_venta = """
            INSERT INTO ventas (
                producto_id,
                fecha,
                cantidad,
                precio_unitario
            ) VALUES (?, ?, ?, ?)
        """
        self.db.cursor.execute(query_registro_venta, (id_producto, fecha_venta, cantidad_a_vender, self.db.cursor.execute("SELECT precio_venta FROM productos WHERE id = ?", (id_producto,)).fetchone()[0]))

    def comprar_producto(self, id_producto, cantidad_a_comprar):
        query_update_stock = """
            UPDATE productos
            SET cantidad = cantidad + ?
            WHERE id = ?
        """
        self.db.cursor.execute(query_update_stock, (cantidad_a_comprar, id_producto))
        
        fecha_compra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_registro_compra = """
            INSERT INTO compras (
                producto_id,
                fecha,
                cantidad,
                precio_unitario
            ) VALUES (?, ?, ?, ?)
        """
        self.db.cursor.execute(query_registro_compra, (id_producto, fecha_compra, cantidad_a_comprar, self.db.cursor.execute("SELECT precio_compra FROM productos WHERE id = ?", (id_producto,)).fetchone()[0]))

    def generar_estadisticas(self):
        total_productos = self.db.cursor.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
        total_unidades = self.db.cursor.execute('SELECT SUM(cantidad) FROM productos').fetchone()[0] or 0
        promedio_compra = self.db.cursor.execute('SELECT AVG(precio_compra) FROM productos').fetchone()[0] or 0
        promedio_venta = self.db.cursor.execute('SELECT AVG(precio_venta) FROM productos').fetchone()[0] or 0
        valor_inventario = self.db.cursor.execute('SELECT SUM(cantidad * precio_compra) FROM productos').fetchone()[0] or 0
        total_ventas = self.db.cursor.execute('SELECT COUNT(*) FROM ventas').fetchone()[0]
        ingresos_totales = self.db.cursor.execute('''
            SELECT COALESCE(SUM(v.cantidad * v.precio_unitario), 0)
            FROM ventas v
            JOIN productos p ON v.producto_id = p.id
        ''').fetchone()[0] or 0
        total_compras = self.db.cursor.execute('SELECT COUNT(*) FROM compras').fetchone()[0]
        gastos_totales = self.db.cursor.execute('''
            SELECT COALESCE(SUM(c.cantidad * c.precio_unitario), 0)
            FROM compras c
            JOIN productos p ON c.producto_id = p.id
        ''').fetchone()[0] or 0
        
        return [
            total_productos,
            total_unidades,
            promedio_compra,
            promedio_venta,
            valor_inventario,
            total_ventas,
            ingresos_totales,
            total_compras,
            gastos_totales
        ]
