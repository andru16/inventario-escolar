from db import Database
from operaciones import Operaciones
from menu import Menu

def main():
    # Inicializar la base de datos
    db = Database('inventario.db')
    
    # Crear instancias de Operaciones y Menu
    operaciones = Operaciones(db)
    menu = Menu(operaciones)
    
    # Ejecutar el menú principal
    menu.run()

if __name__ == "__main__":
    main()
