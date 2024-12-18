import sqlite3
from colorama import Fore, Style, init

init(autoreset = True)

def inicializar_db():
    conexion = sqlite3.connect("TrabajoFinal/inventario.db")
    cursor = conexion.cursor()
    
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Codigo TEXT UNIQUE,
                Nombre TEXT NOT NULL,
                Descripcion TEXT,
                Cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
                Precio REAL NOT NULL CHECK(precio > 0),
                Categoria TEXT
            )
        ''')
    
    conexion.commit()
    conexion.close()
    
def validar_precio():
    while True:
            try:
                precio = float(input("Precio del producto: "))
                if precio >0:
                    return precio
                else:
                    print(Fore.RED +"Entrada invalida. ")
            except ValueError:
                print(Fore.RED +"Entrada invalida. ")
def validar_cantidad():
    while True:
            try:
                cantidad = int(input("Cantidad del producto: "))
                if cantidad >= 0:
                    return cantidad
                else:
                    print(Fore.RED +"Entrada invalida. ")
            except ValueError:
                print(Fore.RED +"Entrada invalida. ")
    
def mostrar_menu():
    print(Fore.GREEN + "\nMenu de gestion de productos \n")
    print("1. Registro: Alta de productos nuevos.")
    print("2. Buscar Producto: Consulta de datos de un producto.")
    print("3. Actualizacion: Modificar la cantidad en stock de un producto o su precio.")  #
    print("4. Eliminacion: Dar de baja productos.")                                        
    print("5. Listado: Listado completo de los productos en la base de datos.")
    print("6. Reporte de Bajo Stock: Lista de productos con cantidad bajo minimo.")        #
    print("7. Salir.") 
    
def registrar_producto():
    print(Fore.LIGHTGREEN_EX +"\n --- Registro de Producto ---")
    while True:
        nombre = input("Ingrese el nombre del producto: ")
        descripcion = input("Por favor de una breve descripcion: ")
        
        precio = validar_precio()
        cantidad = validar_cantidad()
                
        categoria = input("Categoria del producto:")
        
        conexion = sqlite3.connect("TrabajoFinal/prueba.db")
        cursor = conexion.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO productos (Codigo, Nombre, Descripcion, Cantidad, Precio, Categoria)
                Values (NULL,?,?,?,?,?)''',
                (nombre,descripcion,cantidad,precio,categoria)
            )
            id_producto = cursor.lastrowid #se posiciona en la ultima id
            codigo = f"PROD{id_producto}"
            
            cursor.execute('''
                UPDATE productos SET Codigo = ? WHERE id = ?''',
                (codigo,id_producto)
            )
            
            conexion.commit()
            print(Fore.GREEN + f"Producto registrado con exito. Codigo asignado: {codigo}")
            
        except sqlite3.IntegrityError:
            print(Fore.RED + "Error. No se pudo registrar el producto. ")    
        finally:
            conexion.close()
        seguir = input("Desea agregar otro producto? (s:si n:no): ").lower()
        if seguir != "s":
            break      

def buscar_producto():
    print(Fore.LIGHTGREEN_EX +"\n --- Busqueda de Producto ---")
    codigo = input("Ingrese el codigo del producto que desea buscar: ").upper() #Elimina los espacions en blanco
    
    conexion = sqlite3.connect("TrabajoFinal/prueba.db")
    cursor = conexion.cursor()
    
    cursor.execute('''SELECT * FROM productos WHERE Codigo = ?''',(codigo,))
    producto= cursor.fetchone()
    
    conexion.close()
    
    if producto:
        _,codigo,nombre,descripcion,cantidad,precio,categoria = producto
        print(f"\nProducto encontrado con el codigo: {codigo}")
        print(f"Nombre      :    {nombre}")
        print(f"Descripcion :    {descripcion}")
        print(f"Cantidad    :    {cantidad}")
        print(f"Precio      :    ${precio}")
        print(f"Categoria   :    {categoria}")
    else:
        print(Fore.RED + f"No se encontro el producto registrado bajo el codigo: {codigo} ")

def mostrar_productos():
    print(Fore.LIGHTGREEN_EX +"\n --- Todos los Productos ---")
    
    conexion = sqlite3.connect("TrabajoFinal/prueba.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    
    if not productos:
        print("El inventario esta vacio. No hay productos para mostrar")
    else:
        for _,codigo,nombre,descripcion,cantidad,precio,categoria in productos:
            print(f"Codigo      :    {codigo}")
            print(f"Nombre      :    {nombre}")
            print(f"Descripcion :    {descripcion}")
            print(f"Cantidad    :    {cantidad}")
            print(f"Precio      :    ${precio}")
            print(f"Categoria   :    {categoria}")

def eliminar_producto():
    print(Fore.LIGHTGREEN_EX +"\n --- Eliminacion de Producto ---")
    codigo = input("Ingrese el codigo del producto que desea eliminar: ").strip() #Elimina los espacions en blanco
    
    conexion = sqlite3.connect("TrabajoFinal/prueba.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM productos WHERE Codigo = ?", (codigo,))
    producto = cursor.fetchone()
    
    if producto:
        # Mostrar detalles del producto antes de eliminar
        _, codigo, nombre, descripcion, cantidad, precio, categoria = producto
        print(f"Producto encontrado con el código: {codigo}")
        print(f"Nombre      : {nombre}")
        print(f"Descripción : {descripcion}")
        print(f"Cantidad    : {cantidad}")
        print(f"Precio      : ${precio}")
        print(f"Categoría   : {categoria}")

        # Confirmar eliminación
        confirmacion = input("¿Está seguro de que desea eliminar este producto? (s:sí n:no): ").lower()
        if confirmacion == 's':
            cursor.execute("DELETE FROM productos WHERE Codigo = ?", (codigo,))
            conexion.commit()
            print(f"Producto con código {codigo} eliminado exitosamente.")
        else:
            print(Fore.RED + "Eliminación cancelada.")
    else:
        print(Fore.RED + f"No se encontró un producto con el código: {codigo}")

    conexion.close()

def actualizar_stock():
    print(Fore.LIGHTGREEN_EX +"\n --- Actualizacion de Stock ---")
    codigo = input("Ingrese el codigo del producto que desea modificar: ").upper()
    
    conexion = sqlite3.connect("TrabajoFinal/prueba.db")
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM productos WHERE Codigo = ?", (codigo,))
    producto = cursor.fetchone()

    if producto:
        # Mostrar detalles del producto antes de actualizar
        _, codigo, nombre, descripcion, cantidad_actual, precio, categoria = producto
        print(f"Producto encontrado con el código: {codigo}")
        print(f"Nombre      : {nombre}")
        print(f"Descripción : {descripcion}")
        print(f"Cantidad    : {cantidad_actual}")
        print(f"Precio      : ${precio}")
        print(f"Categoría   : {categoria}")

        # Solicitar nueva cantidad
        nueva_cantidad = validar_cantidad()  # Usamos la función de validación ya implementada

        # Actualizar el stock en la base de datos
        cursor.execute(
            "UPDATE productos SET Cantidad = ? WHERE Codigo = ?",
            (nueva_cantidad, codigo)
        )
        conexion.commit()
        print(f"El stock del producto con código {codigo} ha sido actualizado a {nueva_cantidad}.")
    else:
        print(f"No se encontró un producto con el código: {codigo}")

    conexion.close()
    
def reporte_bajo_stock():
    print(Fore.LIGHTGREEN_EX +"\n--- Reporte de Bajo Stock ---")
    try:
        # Solicitar al usuario el nivel mínimo de stock
        nivel_minimo = int(input("Ingrese el nivel mínimo de stock para generar el reporte: "))
        
        # Conexión a la base de datos
        conexion = sqlite3.connect("TrabajoFinal/prueba.db")
        cursor = conexion.cursor()

        # Buscar productos con stock inferior al nivel mínimo
        cursor.execute("SELECT Codigo, Nombre, Cantidad FROM productos WHERE Cantidad < ?", (nivel_minimo,))
        productos = cursor.fetchall()
        conexion.close()

        if productos:
            print(f"\nProductos con stock inferior a {nivel_minimo}:")
            print("-" * 50)
            for codigo, nombre, cantidad in productos:
                print(f"Código      : {codigo}")
                print(f"Nombre      : {nombre}")
                print(f"Cantidad    : {cantidad}")
                print("-" * 50)
        else:
            print(Fore.RED + f"\nNo se encontraron productos con stock inferior a {nivel_minimo}.")
    except ValueError:
        print(Fore.RED +"Entrada inválida. Asegúrese de ingresar un número entero válido.")


def main():
    inicializar_db()
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("Seleccione una opcion: "))
            print(Fore.GREEN +"Usted selecciono la opcion Nro: ",opcion)
            
            if opcion == 1:
                registrar_producto()
            elif opcion == 2:
                buscar_producto()
            elif opcion == 3:
                actualizar_stock()
            elif opcion == 4:
                eliminar_producto()
            elif opcion == 5:
                mostrar_productos()
            elif opcion == 6:
                reporte_bajo_stock()
            elif opcion == 7:
                break
            else:
                print(Fore.RED +"Opcion no valida. Ingrese un valor del 1 al 7")
        except ValueError:
            print(Fore.RED + "Opcion no valida. Ingrese un valor numerico")
            
main()

