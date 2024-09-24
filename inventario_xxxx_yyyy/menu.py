from operaciones import Operaciones

class Menu:
    def __init__(self, operaciones):
        self.operaciones = operaciones

    def mostrar_menu(self):
        print("\nMenú principal:")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Modificar producto")
        print("4. Listar productos")
        print("5. Vender producto")
        print("6. Comprar producto")
        print("7. Generar estadísticas")
        print("8. Salir")

    def agregar_producto(self):
        nombre = input("Ingrese el nombre del producto: ")
        try:
            cantidad = int(input("Ingrese la cantidad inicial: "))
            precio_compra = float(input("Ingrese el precio de compra: "))
            precio_venta = float(input("Ingrese el precio de venta: "))
            self.operaciones.agregar_producto(nombre, cantidad, precio_compra, precio_venta)
            print("Producto agregado correctamente.")
        except ValueError:
            print("Error: La cantidad y los precios deben ser números.")

    def eliminar_producto(self):
        id_producto = input("Ingrese el ID del producto a eliminar: ")
        try:
            id_producto = int(id_producto)
            self.operaciones.eliminar_producto(id_producto)
            print("Producto eliminado correctamente.")
        except ValueError:
            print("Error: El ID debe ser un número entero.")

    def modificar_producto(self):
        id_producto = input("Ingrese el ID del producto a modificar: ")
        try:
            id_producto = int(id_producto)
            print(f"Nombre actual: {self.operaciones.listar_productos()[id_producto-1][1]}")
            nuevo_nombre = input("Ingrese el nuevo nombre (presione Enter para mantener): ") or self.operaciones.listar_productos()[id_producto-1][1]
            
            print(f"Cantidad actual: {self.operaciones.listar_productos()[id_producto-1][2]}")
            while True:
                try:
                    nueva_cantidad = int(input("Ingrese la nueva cantidad (presione Enter para mantener): ") or self.operaciones.listar_productos()[id_producto-1][2])
                    break
                except ValueError:
                    print("La cantidad debe ser un número entero.")
                    
            print(f"Precio de compra actual: ${self.operaciones.listar_productos()[id_producto-1][3]:.2f}")
            while True:
                try:
                    nuevo_precio_compra = float(input("Ingrese el nuevo precio de compra (presione Enter para mantener): ") or self.operaciones.listar_productos()[id_producto-1][3])
                    break
                except ValueError:
                    print("El precio debe ser un número.")
            
            print(f"Precio de venta actual: ${self.operaciones.listar_productos()[id_producto-1][4]:.2f}")
            while True:
                try:
                    nuevo_precio_venta = float(input("Ingrese el nuevo precio de venta (presione Enter para mantener): ") or self.operaciones.listar_productos()[id_producto-1][4])
                    break
                except ValueError:
                    print("El precio debe ser un número.")
            
            self.operaciones.modificar_producto(id_producto, nuevo_nombre, nueva_cantidad, nuevo_precio_compra, nuevo_precio_venta)
            print("Producto modificado correctamente.")
        except (ValueError, IndexError):
            print("Error: El ID debe ser un número entero válido.")

    def listar_productos(self):
        productos = self.operaciones.listar_productos()
        
        if not productos:
            print("No hay productos en el inventario.")
        else:
            print("\nListado de productos:")
            for producto in productos:
                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Precio Compra: ${producto[3]:.2f}, Precio Venta: ${producto[4]:.2f}")

    def vender_producto(self):
        productos = self.operaciones.listar_productos()
        
        if not productos:
            print("No hay productos en el inventario para vender.")
            return
        
        print("\nProductos disponibles para vender:")
        for i, producto in enumerate(productos, start=1):
            print(f"{i}. ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Precio de venta: ${producto[4]:.2f}")
        
        while True:
            try:
                opcion = int(input("Ingrese el número del producto que desea vender: "))
                if 1 <= opcion <= len(productos):
                    id_producto = productos[opcion-1][0]
                    cantidad_disponible = productos[opcion-1][2]
                    
                    while True:
                        try:
                            cantidad_a_vender = int(input(f"Ingrese la cantidad a vender (máximo {cantidad_disponible}): "))
                            if 0 < cantidad_a_vender <= cantidad_disponible:
                                break
                            else:
                                print("La cantidad a vender debe ser mayor que cero y no exceder la cantidad disponible.")
                        except ValueError:
                            print("La cantidad debe ser un número entero.")
                    
                    self.operaciones.vender_producto(id_producto, cantidad_a_vender)
                    print(f"Se vendieron {cantidad_a_vender} unidades de {productos[opcion-1][1]} por ${cantidad_a_vender * productos[opcion-1][4]:.2f}.")
                    break
                else:
                    print("Opción inválida. Por favor, seleccione un número válido.")
            except ValueError:
                print("Por favor, ingrese un número válido.")

    def comprar_producto(self):
        productos = self.operaciones.listar_productos()
        
        if not productos:
            print("No hay productos en el inventario para comprar.")
            return
        
        print("\nProductos disponibles para comprar:")
        for i, producto in enumerate(productos, start=1):
            print(f"{i}. ID: {producto[0]}, Nombre: {producto[1]}, Cantidad: {producto[2]}, Precio de compra: ${producto[3]:.2f}")
        
        while True:
            try:
                opcion = int(input("Ingrese el número del producto que desea comprar: "))
                if 1 <= opcion <= len(productos):
                    id_producto = productos[opcion-1][0]
                    
                    while True:
                        try:
                            cantidad_a_comprar = int(input("Ingrese la cantidad a comprar: "))
                            if cantidad_a_comprar > 0:
                                break
                            else:
                                print("La cantidad a comprar debe ser mayor que cero.")
                        except ValueError:
                            print("La cantidad debe ser un número entero.")
                    
                    self.operaciones.comprar_producto(id_producto, cantidad_a_comprar)
                    print(f"Se compraron {cantidad_a_comprar} unidades de {productos[opcion-1][1]} por ${cantidad_a_comprar * productos[opcion-1][3]:.2f}.")
                    break
                else:
                    print("Opción inválida. Por favor, seleccione un número válido.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
