# ============================================================
#  SISTEMA DE GESTIÓN DE EMPLEADOS - ORANGE SOLUTIONS
#  Programación Avanzada - Semana 5: Módulos en Python
#  Autor: Claudio Baeza Henríquez  - 2026
# ============================================================

from datetime import datetime
from collections import namedtuple

# MÓDULO collections: namedtuple para estructurar datos del empleado
Empleado = namedtuple('Empleado', ['nombre', 'salario', 'fecha_ingreso'])

# Registro global de empleados
registro_empleados = []


# ---------------------------------------------------------------
# FUNCIÓN 1: Registrar un nuevo empleado
# ---------------------------------------------------------------
def agregar_empleado(nombre, salario, fecha_ingreso):
    """Crea un empleado con namedtuple y lo agrega al registro."""
    empleado = Empleado(nombre=nombre, salario=salario, fecha_ingreso=fecha_ingreso)
    registro_empleados.append(empleado)
    return empleado


# ---------------------------------------------------------------
# FUNCIÓN 2: Calcular antigüedad en años
# MÓDULO datetime: datetime.now() obtiene la fecha actual del sistema
# ---------------------------------------------------------------
def calcular_antiguedad(fecha_ingreso):
    """Calcula los años de antigüedad desde la fecha de ingreso hasta hoy."""
    fecha_actual = datetime.now()
    diferencia   = fecha_actual - fecha_ingreso
    antiguedad   = diferencia.days // 365
    return antiguedad


# ---------------------------------------------------------------
# FUNCIÓN 3: Determinar beneficios según antigüedad
# ---------------------------------------------------------------
def determinar_beneficios(antiguedad):
    """Retorna los beneficios asignados según los años de antigüedad."""
    if antiguedad >= 5:
        return "Bono anual"
    elif antiguedad >= 3:
        return "5 días adicionales de vacaciones"
    else:
        return "Sin beneficios adicionales"


# ---------------------------------------------------------------
# FUNCIÓN 4: Mostrar datos de un empleado
# ---------------------------------------------------------------
def mostrar_empleado(empleado):
    """Calcula y muestra los datos completos de un empleado."""
    antiguedad = calcular_antiguedad(empleado.fecha_ingreso)
    beneficios = determinar_beneficios(antiguedad)

    print("-" * 55)
    print(f"  Empleado          : {empleado.nombre}")
    print(f"  Salario           : ${empleado.salario:,}")
    print(f"  Fecha de ingreso  : {empleado.fecha_ingreso.strftime('%d/%m/%Y')}")
    print(f"  Antigüedad        : {antiguedad} año(s)")
    print(f"  Beneficios        : {beneficios}")
    print("-" * 55)


# ---------------------------------------------------------------
# FUNCIÓN 5: Mostrar reporte de todos los empleados
# ---------------------------------------------------------------
def mostrar_reporte():
    """Muestra el reporte completo de todos los empleados registrados."""
    print("\n" + "=" * 55)
    print("      REPORTE DE EMPLEADOS - ORANGE SOLUTIONS")
    print("=" * 55)

    if not registro_empleados:
        print("  No hay empleados registrados en el sistema.")
        return

    for empleado in registro_empleados:
        mostrar_empleado(empleado)

    print(f"\n  Total de empleados registrados: {len(registro_empleados)}")
    print("=" * 55)


# ---------------------------------------------------------------
# FUNCIÓN 6: Ingresar empleado de forma interactiva CON VALIDACIONES
# ---------------------------------------------------------------
def ingresar_empleado_manual():
    """Solicita al usuario los datos de un nuevo empleado con validaciones."""
    print("\n--- Ingresar Nuevo Empleado ---")

    # --- VALIDACIÓN DEL NOMBRE ---
    # No puede estar vacío ni contener números
    while True:
        nombre = input("Nombre del empleado       : ").strip()
        if not nombre:
            print("[ERROR] El nombre no puede estar vacío. Intente nuevamente.")
        elif any(caracter.isdigit() for caracter in nombre):
            print("[ERROR] El nombre no puede contener números. Intente nuevamente.")
        else:
            break  # Nombre válido, sale del bucle

    # --- VALIDACIÓN DEL SALARIO ---
    # Debe ser un número entero positivo
    while True:
        try:
            salario = int(input("Salario del empleado      : $"))
            if salario <= 0:
                print("[ERROR] El salario debe ser un número mayor a cero. Intente nuevamente.")
            else:
                break  # Salario válido, sale del bucle
        except ValueError:
            print("[ERROR] El salario debe ser un número entero (ej: 60000). Intente nuevamente.")

    # --- VALIDACIÓN DE LA FECHA ---
    # Debe ser una fecha real (día, mes y año correctos)
    while True:
        try:
            anio = int(input("Año de ingreso            : "))
            mes  = int(input("Mes de ingreso (1-12)     : "))
            dia  = int(input("Día de ingreso            : "))

            # datetime valida automáticamente si la fecha existe
            # (ej: 30 de febrero o mes 13 lanzará ValueError)
            fecha = datetime(anio, mes, dia)

            # Validamos que la fecha no sea futura
            if fecha > datetime.now():
                print("[ERROR] La fecha de ingreso no puede ser una fecha futura. Intente nuevamente.\n")
            else:
                break  # Fecha válida, sale del bucle

        except ValueError:
            print("[ERROR] Fecha inválida. Verifique que el día, mes y año sean correctos. Intente nuevamente.\n")

    # Si todo es válido, se agrega el empleado
    agregar_empleado(nombre, salario, fecha)
    print(f"\n✅ Empleado '{nombre}' registrado exitosamente.")

# ---------------------------------------------------------------
# FUNCIÓN PRINCIPAL CON MENÚ
# ---------------------------------------------------------------
def main():
    # Carga de datos de prueba (como indica el enunciado)
    agregar_empleado("María García", 60000, datetime(2019, 3, 20))
    agregar_empleado("Carlos López", 75000, datetime(2017, 6, 15))
    agregar_empleado("Ana Martínez", 55000, datetime(2023, 1, 10))
    agregar_empleado("Pedro Rojas",  80000, datetime(2015, 9, 5))

    while True:
        print("\n" + "=" * 55)
        print("   SISTEMA DE GESTIÓN DE EMPLEADOS")
        print("   Orange Solutions")
        print("=" * 55)
        print("  1. Ver reporte de todos los empleados")
        print("  2. Agregar nuevo empleado")
        print("  3. Salir del sistema")
        print("=" * 55)

        opcion = input("Seleccione una opción (1, 2 o 3): ")

        if opcion == '1':
            mostrar_reporte()
        elif opcion == '2':
            ingresar_empleado_manual()
        elif opcion == '3':
            print("\nCerrando el sistema. ¡Hasta pronto, Orange Solutions!")
            break
        else:
            print("[ERROR] Opción no válida. Ingrese solo 1, 2 o 3.")


if __name__ == "__main__":
    main()