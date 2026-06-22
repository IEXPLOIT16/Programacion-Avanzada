# ============================================================
#  SISTEMA DE INVENTARIO - SUPERMERCADO "FRESCURA NATURAL"
#  Programación Avanzada - Manejo de Excepciones
#  Autor: Claudio Baeza Henríquez  - 2026
# ============================================================


# ------------------------------------------------------------------
# FUNCIÓN 1: Solicita y valida la cantidad en existencia
# Maneja excepción ValueError y lógica de negativos
# ------------------------------------------------------------------
def obtener_existencia():
    """Solicita al usuario la cantidad en existencia y la valida."""
    while True:
        try:
            existencia = int(input("Ingrese la cantidad actual de frutas y verduras en existencia: "))
            
            # Validamos que no sea negativa (error de lógica de negocio)
            if existencia < 0:
                print("[ERROR] La cantidad en existencia no puede ser negativa. Intente nuevamente.\n")
                continue  # Vuelve al inicio del bucle
                
            return existencia  # Si es válida, la retorna
        
        except ValueError:
            # Capturamos el error si el usuario escribe texto en lugar de número
            print("[ERROR] Valor no válido. Debe ingresar un número entero (ej: 150). Intente nuevamente.\n")


# ------------------------------------------------------------------
# FUNCIÓN 2: Solicita y valida la cantidad vendida
# Maneja excepción ValueError, negativos y exceso de existencia
# ------------------------------------------------------------------
def obtener_vendidos(existencia):
    """Solicita al usuario la cantidad vendida y la valida frente a la existencia."""
    while True:
        try:
            vendidos = int(input("Ingrese la cantidad de productos vendidos durante el día: "))
            
            # Validamos que no sea negativa
            if vendidos < 0:
                print("[ERROR] La cantidad vendida no puede ser negativa. Intente nuevamente.\n")
                continue
            
            # Validamos que no supere la existencia (error de lógica de negocio)
            if vendidos > existencia:
                print(f"[ERROR] La cantidad vendida ({vendidos}) no puede exceder")
                print(f"        la cantidad en inventario ({existencia}). Intente nuevamente.\n")
                continue
                
            return vendidos  # Si es válida, la retorna
        
        except ValueError:
            print("[ERROR] Valor no válido. Debe ingresar un número entero (ej: 30). Intente nuevamente.\n")


# ------------------------------------------------------------------
# FUNCIÓN 3: Calcula y muestra el resumen del inventario
# ------------------------------------------------------------------
def mostrar_resumen(existencia, vendidos):
    """Calcula el stock restante y muestra el reporte final."""
    stock_restante = existencia - vendidos
    
    # Determinamos el estado del inventario
    if stock_restante == 0:
        estado = "⚠️  SIN STOCK - Requiere reposición urgente"
    elif stock_restante <= existencia * 0.20:
        estado = "⚠️  STOCK BAJO - Considere reabastecer pronto"
    else:
        estado = "✅  STOCK NORMAL"
    
    print("\n" + "="*50)
    print("   REPORTE DE INVENTARIO - FRESCURA NATURAL")
    print("="*50)
    print(f"   Cantidad inicial en existencia : {existencia} unidades")
    print(f"   Cantidad vendida durante el día: {vendidos} unidades")
    print(f"   Stock restante al cierre       : {stock_restante} unidades")
    print(f"   Estado del inventario          : {estado}")
    print("="*50)


# ------------------------------------------------------------------
# FUNCIÓN PRINCIPAL: Orquesta el flujo del programa
# ------------------------------------------------------------------
def main():
    print("="*50)
    print("   BIENVENIDO AL SISTEMA DE INVENTARIO")
    print("   Supermercado Frescura Natural")
    print("="*50 + "\n")

    while True:
        # Llamamos a cada función modular
        existencia = obtener_existencia()
        vendidos   = obtener_vendidos(existencia)
        
        # Mostramos el resumen
        mostrar_resumen(existencia, vendidos)
        
        # Preguntamos si desea registrar otro producto
        print()
        continuar = input("¿Desea registrar otro producto? (s/n): ").strip().lower()
        if continuar != 's':
            print("\nCerrando el sistema. ¡Hasta pronto, Frescura Natural!")
            break
        print()


# Punto de entrada del programa
if __name__ == "__main__":
    main()