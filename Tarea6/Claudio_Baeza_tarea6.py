# ============================================================
#  SISTEMA DE GESTIÓN DE LIBROS Y AUTORES - IACC
#  Programación Avanzada - Semana 6: Ficheros y JSON
#  Autor: Claudio Baeza Henríquez  - 2026
# ============================================================

import json
import os

# Nombres constantes de los archivos
ARCHIVO_LIBROS = 'libros.json'
ARCHIVO_AUTORES = 'autores.json'

def cargar_datos(nombre_archivo):
    """Carga los datos de un archivo JSON o retorna una lista vacía si no existe."""
    # Paso 2: Verificar si el archivo ya existe
    if os.path.exists(nombre_archivo):
        # Paso 3: Abrir en lectura ('r') y cargar datos
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    else:
        # paso 4: Si el archivo no existe, lo creamos con una lista vacía
        guardar_datos(nombre_archivo, [])
        return []

def guardar_datos(nombre_archivo, datos):
    """Guarda la lista de diccionarios en un archivo JSON."""
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

def agregar_libro():
    """Solicita datos al usuario con validaciones y agrega un libro al JSON."""
    libros = cargar_datos(ARCHIVO_LIBROS)
    print("\n--- Agregar Nuevo Libro ---")
    
    # 1. Validación del título: no vacío y no repetido
    while True:
        titulo = input("Ingrese el título del libro: ").strip()
        if not titulo:
            print("[ERROR] El título no puede estar vacío.")
        else:
            # Verificamos si el título ya existe (ignorando mayúsculas/minúsculas)
            existe = False
            for libro in libros:
                if libro['titulo'].lower() == titulo.lower():
                    existe = True
                    break
            
            if existe:
                print(f"[ERROR] El libro '{titulo}' ya se encuentra registrado en el sistema.")
            else:
                break # Pasa la validación

    # 2. Validación del género: no vacío y sin números
    while True:
        genero = input("Ingrese el género: ").strip()
        if not genero:
            print("[ERROR] El género no puede estar vacío.")
        elif any(char.isdigit() for char in genero):
            print("[ERROR] El género no debe contener números.")
        else:
            break

    # 3. Validación del año: exactamente 4 dígitos
    while True:
        anio = input("Ingrese el año de publicación (ej: 1998): ").strip()
        if anio.isdigit() and len(anio) == 4:
            break
        print("[ERROR] El año debe contener exactamente 4 números (ej: 1998).")

    # 4. Validación del autor: no vacío y sin números
    while True:
        autor = input("Ingrese el nombre del autor asociado: ").strip()
        if not autor:
            print("[ERROR] El nombre del autor no puede estar vacío.")
        elif any(char.isdigit() for char in autor):
            print("[ERROR] El nombre del autor no debe contener números.")
        else:
            break
    
    nuevo_libro = {
        "titulo": titulo,
        "genero": genero,
        "anio": anio,
        "autor": autor
    }
    libros.append(nuevo_libro)
    guardar_datos(ARCHIVO_LIBROS, libros)
    print("\n✅ ¡Éxito! El libro se ha agregado correctamente al archivo.")

def agregar_autor():
    """Solicita datos al usuario con validaciones y agrega un autor al JSON."""
    autores = cargar_datos(ARCHIVO_AUTORES)
    print("\n--- Agregar Nuevo Autor ---")
    
    # Validación del nombre: no vacío, sin números y NO repetido
    while True:
        nombre = input("Ingrese el nombre del autor: ").strip()
        if not nombre:
            print("[ERROR] El nombre no puede estar vacío.")
        elif any(char.isdigit() for char in nombre):
            print("[ERROR] El nombre no debe contener números.")
        else:
            # Verificamos si el autor ya existe (ignorando mayúsculas/minúsculas)
            existe = False
            for autor in autores:
                if autor['nombre'].lower() == nombre.lower():
                    existe = True
                    break
            
            if existe:
                print(f"[ERROR] El autor '{nombre}' ya está registrado en el sistema.")
            else:
                break # Pasa la validación

    # Validación de la nacionalidad: no vacío y sin números
    while True:
        nacionalidad = input("Ingrese la nacionalidad: ").strip()
        if not nacionalidad:
            print("[ERROR] La nacionalidad no puede estar vacía.")
        elif any(char.isdigit() for char in nacionalidad):
            print("[ERROR] La nacionalidad no debe contener números.")
        else:
            break
    
    nuevo_autor = {
        "nombre": nombre,
        "nacionalidad": nacionalidad
    }
    autores.append(nuevo_autor)
    guardar_datos(ARCHIVO_AUTORES, autores)
    print("\n✅ ¡Éxito! El autor se ha agregado correctamente al archivo.")

def mostrar_informacion():
    """Muestra la información de los archivos en formato legible con indentación."""
    print("\n" + "="*50)
    print("      INFORMACIÓN ALMACENADA EN EL SISTEMA")
    print("="*50)
    
    print("\n📚 AUTORES REGISTRADOS:")
    if os.path.exists(ARCHIVO_AUTORES):
        with open(ARCHIVO_AUTORES, 'r', encoding='utf-8') as f:
            datos_autores = json.load(f)
            print(json.dumps(datos_autores, indent=4, ensure_ascii=False))
    else:
        print("  No hay datos de autores registrados.")
        
    print("\n📖 LIBROS REGISTRADOS:")
    if os.path.exists(ARCHIVO_LIBROS):
        with open(ARCHIVO_LIBROS, 'r', encoding='utf-8') as f:
            datos_libros = json.load(f)
            print(json.dumps(datos_libros, indent=4, ensure_ascii=False))
    else:
        print("  No hay datos de libros registrados.")
    print("="*50)

def main():
    while True:
        print("\n" + "="*45)
        print("    SISTEMA DE GESTIÓN IACC - BIBLIOTECA")
        print("="*45)
        print("  1. Agregar libro")
        print("  2. Agregar autor")
        print("  3. Mostrar información almacenada")
        print("  4. Salir del programa")
        print("="*45)
        
        opcion = input("  Seleccione una opción (1-4): ")
        
        if opcion == '1':
            agregar_libro()
        elif opcion == '2':
            agregar_autor()
        elif opcion == '3':
            mostrar_informacion()
        elif opcion == '4':
            print("\nCerrando el sistema. ¡Gracias por utilizar la plataforma IACC!")
            break
        else:
            print("\n[ERROR] Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()