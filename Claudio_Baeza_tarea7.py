# ============================================================
#  INTERFAZ GRÁFICA (GUI) - BIBLIOTECA SaberX
#  Programación Avanzada - Semana 7: Tkinter
#  Autor: Claudio Baeza Henríquez  - 2026
# ============================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Lista global en memoria para llevar el control de los libros y evitar duplicados
libros_registrados = []

# ---------------------------------------------------------
# FUNCIONES LÓGICAS (Manejo de eventos de los botones)
# ---------------------------------------------------------
def registrar_libro():
    """Recopila los datos de la interfaz, los valida y los imprime en consola."""
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    anio = entry_anio.get().strip()
    copias = entry_copias.get().strip()
    
    # --- VALIDACIÓN 1: Campos vacíos ---
    if not titulo or not autor or not anio or not copias:
        messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos de texto (Título, Autor, Año y Copias).")
        return

    # --- VALIDACIÓN 2: Reglas numéricas ---
    if not anio.isdigit() or len(anio) != 4:
        messagebox.showerror("Error en el Año", "El año de publicación debe contener exactamente 4 números (ej: 1998). No se aceptan letras.")
        return

    if not copias.isdigit():
        messagebox.showerror("Error en Inventario", "El número de copias debe ser un número. No se aceptan letras.")
        return

    # --- VALIDACIÓN 3: Evitar registros duplicados ---
    # Pasamos a minúsculas para que "Cien años" sea detectado igual a "CIEN AÑOS"
    titulo_normalizado = titulo.lower()
    autor_normalizado = autor.lower()
    
    for libro in libros_registrados:
        if libro['titulo'] == titulo_normalizado and libro['autor'] == autor_normalizado:
            messagebox.showerror("Registro Duplicado", f"El libro '{titulo}' del autor '{autor}' ya se encuentra registrado en el sistema.")
            return # Detenemos la ejecución
            
    # Si pasa la validación de duplicados, lo guardamos en nuestra lista en memoria
    libros_registrados.append({'titulo': titulo_normalizado, 'autor': autor_normalizado})
    # ----------------------------------------------------------------------------
    
    genero = var_genero.get()
    
    # Comprobamos los Checkbuttons activos
    categorias = []
    if var_cat_novela.get(): categorias.append("Novela")
    if var_cat_ciencia.get(): categorias.append("Ciencia")
    if var_cat_historia.get(): categorias.append("Historia")
    if var_cat_fantasia.get(): categorias.append("Fantasía")
    
    estado = var_estado.get()
    idioma = var_idioma.get()
    resumen = text_resumen.get("1.0", tk.END).strip()
    
    # Salida por el terminal de Visual Studio Code
    print("\n" + "="*40)
    print(" 📚 NUEVO LIBRO REGISTRADO (SaberX)")
    print("="*40)
    print(f"Título          : {titulo}")
    print(f"Autor           : {autor}")
    print(f"Año publicación : {anio}")
    print(f"Género          : {genero}")
    print(f"Categorías      : {', '.join(categorias) if categorias else 'Ninguna seleccionada'}")
    print(f"Estado          : {estado}")
    print(f"N° de copias    : {copias}")
    print(f"Idioma          : {idioma}")
    print(f"Resumen         : {resumen}")
    print("="*40)
    
    messagebox.showinfo("Registro Exitoso", f"El libro '{titulo}' se ha registrado correctamente.\nYa hay {len(libros_registrados)} libro(s) en la base de datos temporal.")
    
    # Opcional: Limpiar el formulario automáticamente después de un registro exitoso
    # limpiar_formulario()

def limpiar_formulario():
    """Reinicia todos los campos visuales a su estado original."""
    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_anio.delete(0, tk.END)
    
    var_genero.set("Ficción")
    var_cat_novela.set(False)
    var_cat_ciencia.set(False)
    var_cat_historia.set(False)
    var_cat_fantasia.set(False)
    
    var_estado.set("Disponible")
    entry_copias.delete(0, tk.END)
    var_idioma.set("Español")
    text_resumen.delete("1.0", tk.END)

# ---------------------------------------------------------
# CONSTRUCCIÓN DE LA INTERFAZ GRÁFICA (Widgets)
# ---------------------------------------------------------

# Ventana principal
root = tk.Tk()
root.title("SaberX - Sistema de Registro de Libros")
root.geometry("450x650")
root.resizable(False, False)

# 1. FRAME: Detalles del libro
frame_detalles = tk.LabelFrame(root, text="Detalles del Libro", padx=10, pady=10)
frame_detalles.pack(fill="x", padx=15, pady=5)

tk.Label(frame_detalles, text="Título:").grid(row=0, column=0, sticky="w", pady=2)
entry_titulo = tk.Entry(frame_detalles, width=45)
entry_titulo.grid(row=0, column=1, pady=2, padx=5)

tk.Label(frame_detalles, text="Autor:").grid(row=1, column=0, sticky="w", pady=2)
entry_autor = tk.Entry(frame_detalles, width=45)
entry_autor.grid(row=1, column=1, pady=2, padx=5)

tk.Label(frame_detalles, text="Año publicación:").grid(row=2, column=0, sticky="w", pady=2)
entry_anio = tk.Entry(frame_detalles, width=20)
entry_anio.grid(row=2, column=1, sticky="w", pady=2, padx=5)

# 2. FRAME: Género y Categoría
frame_cat = tk.LabelFrame(root, text="Género y Categoría", padx=10, pady=10)
frame_cat.pack(fill="x", padx=15, pady=5)

var_genero = tk.StringVar(value="Ficción")
tk.Label(frame_cat, text="Género:").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame_cat, text="Ficción", variable=var_genero, value="Ficción").grid(row=0, column=1, sticky="w")
tk.Radiobutton(frame_cat, text="No Ficción", variable=var_genero, value="No Ficción").grid(row=0, column=2, sticky="w")

tk.Label(frame_cat, text="Categorías:").grid(row=1, column=0, sticky="w", pady=(10,0))
var_cat_novela = tk.BooleanVar()
var_cat_ciencia = tk.BooleanVar()
var_cat_historia = tk.BooleanVar()
var_cat_fantasia = tk.BooleanVar()

tk.Checkbutton(frame_cat, text="Novela", variable=var_cat_novela).grid(row=1, column=1, sticky="w", pady=(10,0))
tk.Checkbutton(frame_cat, text="Ciencia", variable=var_cat_ciencia).grid(row=1, column=2, sticky="w", pady=(10,0))
tk.Checkbutton(frame_cat, text="Historia", variable=var_cat_historia).grid(row=2, column=1, sticky="w")
tk.Checkbutton(frame_cat, text="Fantasía", variable=var_cat_fantasia).grid(row=2, column=2, sticky="w")

# 3. FRAME: Estado de Disponibilidad y Copias
frame_estado = tk.LabelFrame(root, text="Disponibilidad e Inventario", padx=10, pady=10)
frame_estado.pack(fill="x", padx=15, pady=5)

var_estado = tk.StringVar(value="Disponible")
tk.Radiobutton(frame_estado, text="Disponible", variable=var_estado, value="Disponible").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame_estado, text="Prestado", variable=var_estado, value="Prestado").grid(row=0, column=1, sticky="w", padx=10)

tk.Label(frame_estado, text="Número de copias:").grid(row=1, column=0, sticky="w", pady=(10,0))
entry_copias = tk.Entry(frame_estado, width=10)
entry_copias.grid(row=1, column=1, sticky="w", pady=(10,0))

# 4. FRAME: Menú de Idioma y Resumen
frame_extra = tk.LabelFrame(root, text="Información Adicional", padx=10, pady=10)
frame_extra.pack(fill="x", padx=15, pady=5)

tk.Label(frame_extra, text="Idioma del libro:").grid(row=0, column=0, sticky="w")
var_idioma = tk.StringVar(value="Español")
# Menú desplegable usando Combobox
menu_idioma = ttk.Combobox(frame_extra, textvariable=var_idioma, values=["Español", "Inglés", "Otro"], state="readonly", width=15)
menu_idioma.grid(row=0, column=1, sticky="w", padx=5)

tk.Label(frame_extra, text="Resumen:").grid(row=1, column=0, sticky="nw", pady=(10,0))
text_resumen = tk.Text(frame_extra, height=4, width=32)
text_resumen.grid(row=1, column=1, pady=(10,0), padx=5)

# 5. BOTONES DE ACCIÓN
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

# El comando llama a nuestra función registrar_libro()
btn_registrar = tk.Button(frame_botones, text="Registrar Libro", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15, command=registrar_libro)
btn_registrar.grid(row=0, column=0, padx=10)

# El comando llama a nuestra función limpiar_formulario()
btn_limpiar = tk.Button(frame_botones, text="Limpiar", bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=15, command=limpiar_formulario)
btn_limpiar.grid(row=0, column=1, padx=10)

# Iniciar el bucle de la aplicación
root.mainloop()