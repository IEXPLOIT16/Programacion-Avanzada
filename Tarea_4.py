#Asignatura: Programación Avanzada
#Semana 4: Colecciones de datos típicas de Python
#Caso Práctico: Registro de Visitantes del Museo en París
#Autor: Claudio Baeza Henríquez  - 2026


def normalizar_nombre(nombre):
    
    #Aplica operaciones avanzadas de strings para limpiar y estandarizar.
    #Ejemplo: '  juan   perez  ' -> 'Juan Perez'
    
    palabras_limpias = [palabra.capitalize() for palabra in nombre.split()]
    return " ".join(palabras_limpias)

def registrar_visitantes():
    
    #Función principal. Usa un Diccionario para mapear salas con Conjuntos (Sets).
    #Incluye un Diccionario auxiliar para control de homónimos y manejo de excepciones.
    
    museo = {
        "Sala 1": set(),
        "Sala 2": set(),
        "Sala 3": set()
    }
    # Diccionario para controlar homónimos (Clave: Nombre, Valor: Cantidad de veces que ingresa)
    control_homonimos = {} 
    
    print("="*60)
    print("   SISTEMA DE REGISTRO DE VISITANTES - MUSEO DE PARÍS   ")
    print("="*60)
    
    while True:
        print("\nSeleccione la sala para registrar visitantes:")
        print("1. Sala 1")
        print("2. Sala 2")
        print("3. Sala 3")
        print("4. Finalizar registro y generar reporte global")
        
        opcion = input("Ingrese una opción (1-4): ").strip()
        
        if opcion == '4':
            break
        elif opcion not in ['1', '2', '3']:
            print("[Error] Opción no válida. Por favor ingrese un número del 1 al 4.")
            continue
            
        sala_key = f"Sala {opcion}"
        print(f"\n--- Registrando visitantes para {sala_key} ---")
        
        while True:
            # USO DE TRY / EXCEPT / ELSE (Refuerzo de Semana 3 + Semana 4)
            try:
                nombre = input("Ingrese el nombre del visitante (o '0' para terminar sala): ").strip()
                
                if nombre == '0':
                    break
                    
                # REGLAS DE NEGOCIO CON RAISE (Invocación explícita de excepciones)
                if not nombre:
                    raise ValueError("El nombre no puede estar vacío.")
                    
                if not all(c.isalpha() or c.isspace() for c in nombre):
                    raise ValueError("El nombre solo debe contener caracteres alfabéticos.")
                
                # Normalización del string
                nombre_normalizado = normalizar_nombre(nombre)
                
                # LÓGICA DE HOMÓNIMOS (Uso avanzado de Diccionarios)
                if nombre_normalizado in control_homonimos:
                    control_homonimos[nombre_normalizado] += 1
                    identificador_unico = f"{nombre_normalizado} ({control_homonimos[nombre_normalizado]})"
                    print(f"[Aviso] Nombre repetido detectado. Registrado como homónimo: {identificador_unico}")
                else:
                    control_homonimos[nombre_normalizado] = 1
                    identificador_unico = nombre_normalizado
                    
            except ValueError as ve:
                # Captura las excepciones lanzadas por 'raise' o errores de conversión
                print(f"[!] Error de validación: {ve}")
            except Exception as e:
                # Captura cualquier otro error inesperado del sistema
                print(f"[!] Error inesperado del sistema: {e}")
            else:
                # El bloque 'else' solo se ejecuta si NO hubo ninguna excepción (Error-free)
                museo[sala_key].add(identificador_unico)
                print(f"-> Visitante '{identificador_unico}' guardado exitosamente en {sala_key}.")
            
    return museo

def generar_reporte(museo):
    
    #Genera la lista única global usando operaciones matemáticas de Sets 
    #y calcula estadísticas de afluencia.
    
    print("\n" + "="*60)
    print("               RESUMEN DE VISITANTES POR SALA             ")
    print("="*60)
    
    for sala, visitantes in museo.items():
        lista_ordenada_sala = sorted(list(visitantes))
        if lista_ordenada_sala:
            print(f"{sala}: {', '.join(lista_ordenada_sala)}")
        else:
            print(f"{sala}: Sin visitantes registrados.")
            
    # OPERACIÓN AVANZADA DE SETS: Unión
    visitantes_globales = set().union(*museo.values())
    lista_unica_final = sorted(list(visitantes_globales))
    
    # Estadísticas
    total_visitantes_unicos = len(lista_unica_final)
    total_visitas_registradas = sum(len(v) for v in museo.values())
    
    print("\n" + "="*60)
    print("                     RESULTADO FINAL                      ")
    print("="*60)
    
    # Salida requerida por la tarea
    print(f"Lista Única de Visitantes: {' '.join(lista_unica_final)}")
    
    print(f"\n[Estadísticas del Administrador]")
    print(f"-> Total de personas reales (únicas) en el museo: {total_visitantes_unicos}")
    print(f"-> Total de visitas (afluencia) registradas en salas: {total_visitas_registradas}")
    
    if total_visitas_registradas > total_visitantes_unicos:
        print("-> Nota: Se detectaron visitantes que recorrieron múltiples salas.")

def main():
    datos_museo = registrar_visitantes()
    generar_reporte(datos_museo)

if __name__ == "__main__":
    main()