from operaciones import Operaciones

class Menu:
    def __init__(self, operaciones):
        self.operaciones = operaciones

    def mostrar_menu_principal(self):
        print("\nMenú principal:")
        print("1. Gestionar productos")
        print("2. Gestionar ventas")
        print("3. Gestionar compras")
        print("4. Ver informes")
        print("5. Salir")

    def mostrar_menu_gestionar_productos(self):
        print("\nMenú de gestión de productos:")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Modificar producto")
        print("4. Listar productos")
        print("5. Gestionar categoriasd")
        print("6. Volver al menú principal")

    def mostrar_menu_ventas(self):
        print("\nMenú de ventas:")
        print("1. Vender producto")
        print("2. Listar ventas")
        print("3. Volver al menú principal")
    
    def mostrar_menu_compras(self):
        print("\nMenú de compras:")
        print("1. comprar producto")
        print("2. Listar compras")
        print("3. Volver al menú principal")

    def mostrar_menu_ver_informes(self):
        print("\nMenú de informes:")
        print("1. Estadísticas generales")
        print("2. Volver al menú principal")

    def mostrar_menu_categorias(self):
        print("\nMenú de gestión de categorías:")
        print("1. Agregar categoría")
        print("2. Eliminar categoría")
        print("3. Listar categorías")
        print("4. Volver al menú de productos")

    def agregar_categoria(self):
        nombre = input("Ingrese el nombre de la nueva categoría: ")
        try:
            self.operaciones.agregar_categoria(nombre)
            print(f"Categoría '{nombre}' agregada correctamente.")
        except ValueError:
            print("Error: La categoría ya existe.")

    def eliminar_categoria(self):
        nombre = input("Ingrese el nombre de la categoría a eliminar: ")
        try:
            self.operaciones.eliminar_categoria(nombre)
            print(f"Categoría '{nombre}' eliminada correctamente.")
        except ValueError:
            print("Error: La categoría no existe.")

    def listar_categorias(self):
        categorias = self.operaciones.listar_categorias()
        
        if not categorias:
            print("No hay categorías en el sistema.")
        else:
            print(f"{'ID':^5} | {'Nombre':^30}")
            print("-" * 35)
        
            for categoria in categorias:
                print(f"{categoria[0]:^5} | {categoria[1]:^30}")

    def run(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.menu_gestionar_productos()
            elif opcion == "2":
                self.menu_gestionar_ventas()
            elif opcion == "3":
                self.menu_gestionar_compras()
            elif opcion == "4":
                self.menu_ver_informes()
            elif opcion == "5":
                print("Gracias por usar el sistema de inventario de productos escolares.")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

    def menu_gestionar_productos(self):
        while True:
            self.mostrar_menu_gestionar_productos()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.agregar_producto()
            elif opcion == "2":
                self.eliminar_producto()
            elif opcion == "3":
                self.modificar_producto()
            elif opcion == "4":
                self.listar_productos()
            elif opcion == "5":
                self.menu_gestionar_categorias()
            elif opcion == "6":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

    def menu_gestionar_categorias(self):
        while True:
            self.mostrar_menu_categorias()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.agregar_categoria()
            elif opcion == "2":
                self.eliminar_categoria()
            elif opcion == "3":
                self.listar_categorias()
            elif opcion == "4":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

    def menu_gestionar_ventas(self):
        while True:
            self.mostrar_menu_ventas()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.vender_producto()
            elif opcion == "2":
                self.listar_ventas()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
    
    def menu_gestionar_compras(self):
        while True:
            self.mostrar_menu_compras()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.comprar_producto()
            elif opcion == "2":
                self.listar_compras()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

    def menu_ver_informes(self):
        while True:
            self.mostrar_menu_ver_informes()
            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self.ver_estadisticas()
            elif opcion == "2":
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

    def agregar_producto(self):

        nombre = input("Nombre de producto: ")
        categoria = self.operaciones.seleccionar_categoria()
        cantidad = int(input("Cantidad en stock: "))
        precio_compra = float(input("Precio de compra: $"))
        precio_venta = float(input("Precio de venta: $"))

        try:
            self.operaciones.agregar_producto(
            nombre = nombre, 
            categoria = categoria, 
            cantidad = cantidad, 
            precio_compra = precio_compra, 
            precio_venta = precio_venta
            )
            print(f"Producto '{nombre}' Agregado correctamente.")
        except ValueError:
            print("Error: No se pudo agregar el producto.")


    def eliminar_producto(self):

        producto_id = input('Ingresa el id del producto que desea eliminar: ')

        self.operaciones.eliminar_producto(producto_id)
        print(f"Eliminado correctamente.")
       
    def modificar_producto(self):

        producto_id = input('Ingresa el id del producto que desea actualizar: ')
       
        verificar_producto = self.operaciones.producto_existe(producto_id)

        if (verificar_producto):

            nombre = input("Nuevo nombre de producto: ")
            categoria = self.operaciones.seleccionar_categoria()
            cantidad = int(input("Nueva cantidad en stock: "))
            precio_compra = float(input("Nuevo precio de compra: $"))
            precio_venta = float(input("Nuevo precio de venta: $"))

            try:
                self.operaciones.modificar_producto(
                    id_producto = producto_id, 
                    nuevo_nombre=nombre, 
                    nuevo_id_categoria=categoria, 
                    nueva_cantidad=cantidad, 
                    nuevo_precio_compra=precio_compra, 
                    nuevo_precio_venta=precio_venta
                )
                print(f"Producto '{nombre}' Actualizado correctamente.")
            except ValueError:
                print("Error: No se pudo actualizar el producto.")
        else:
            print(f"El producto con id '{producto_id}' no existe!")

    def listar_productos(self):
        productos = self.operaciones.listar_productos()

        if not productos:
            print("No hay categorías en el sistema.")
        else:
            print(f"{'ID':^5} | {'Producto':^30} | {'Categoria':^20} | {'Cantidad':^10} | {'Costo':^10} | {'Venta':^10}")
            print("-" * 105)
        
            for producto in productos:
                print(f"{producto[0]:^5} | {producto[1]:^30} | {producto[5]:^20} | {producto[2]:^10} | {producto[3]:^10} | {producto[4]:^10}")
    
    def vender_producto(self):
        productos = []
        total_ventas = 0
        
        while True:
            print("\n------------------- Ventas -------------------")
            print("1. Agregar producto a la venta")
            print("2. Finalizar venta")
            
            opcion = input("Ingrese su opción: ")
            
            if opcion == "1":
                id_producto = input("Ingrese el ID del producto: ")
                cantidad = int(input("Ingrese la cantidad a vender: "))
                
                try:
                    self.operaciones.vender_producto(id_producto, cantidad)
                    productos.append((id_producto, cantidad))
                    total_ventas += cantidad * self.operaciones.obtener_precio_unitario(id_producto)
                    print(f"Producto añadido a la venta. Total: ${total_ventas:.2f}")
                except ValueError as e:
                    print(f"Error al agregar producto: {str(e)}")
            elif opcion == "2":
                self.confirmar_venta(productos, total_ventas)
                break
            else:
                print("Opción inválida. Por favor, intente nuevamente.")

    def comprar_producto(self):
        id_producto = input("Ingrese el ID del producto a comprar: ")
        cantidad_a_comprar = int(input("Ingrese la cantidad a comprar: "))
        
        try:
            self.operaciones.comprar_producto(id_producto, cantidad_a_comprar)
            print("Compra realizada con éxito.")
        except ValueError as e:
            print(f"Error al realizar la compra: {str(e)}")
