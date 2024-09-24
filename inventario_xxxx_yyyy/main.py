from db import Database
from operaciones import Operaciones
from menu import Menu

def main():
    # Inicializar la base de datos
    db = Database('inventario.db')
    
    # Crear instancias de Operaciones y Menu
    operaciones = Operaciones(db)
    menu = Menu(operaciones)
    
    # Insertar algunos datos de ejemplo
    operaciones.agregar_producto("Laptop", 5, 1500, 1800)
    operaciones.agregar_producto("Smartphone", 10, 800, 1000)
    operaciones.agregar_producto("Tableta", 7, 600, 750)
    
    # Ejecutar el menú principal
    while True:
        menu.mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            menu.agregar_producto()
        elif opcion == "2":
            menu.eliminar_producto()
        elif opcion == "3":
            menu.modificar_producto()
        elif opcion == "4":
            menu.listar_productos()
        elif opcion == "5":
            menu.vender_producto()
        elif opcion == "6":
            menu.comprar_producto()
        elif opcion == "7":
            estadisticas = operaciones.generar_estadisticas()
            print("\nEstadísticas del inventario:")
            print(f"Total de productos: {estadisticas[0]}")
            print(f"Total de unidades: {estadisticas[1]}")
            print(f"Precio promedio de compra: ${estadisticas[2]:.2f}")
            print(f"Precio promedio de venta: ${estadisticas[3]:.2f}")
            print(f"Valor total del inventario: ${estadisticas[4]:.2f}")
            print(f"Total de ventas: {estadisticas[5]}")
            print(f"Ingresos totales: ${estadisticas[6]:.2f}")
            print(f"Total de compras: {estadisticas[7]}")
            print(f"Gastos totales: ${estadisticas[8]:.2f}")
        elif opcion == "8":
            print("Gracias por usar el sistema de inventario.")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
