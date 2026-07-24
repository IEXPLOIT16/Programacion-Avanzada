# ============================================================
#  PROGRAMACION AVANZADA - SEMANA 8
#  Tema: Python + Tkinter + MySQL 
#  Sistema de Gestion de Videojuegos - IACC
#  Autor: Claudio Baeza Henríquez  - 2026
# ============================================================

# Importar Tkinter para la interfaz gráfica
import tkinter as tk
from tkinter import ttk, messagebox

# Importar mysql.connector para la conexión con MySQL
import mysql.connector
from mysql.connector import Error

# ============================================================
# CONFIGURACION DE LA BASE DE DATOS
# ============================================================
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': '',          # Contrasena de MySQL (XAMPP por defecto es vacia)
    'database': 'iacc_videojuegos'
}

# ============================================================
# FUNCIONES DE CONEXION Y CONSULTAS SQL
# ============================================================

def crear_conexion():
    """Establece y retorna una conexion a la base de datos MySQL."""
    try:
        # Crear la conexión usando las credenciales definidas en DB_CONFIG
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except Error as e:
         #Mostrar mensaje de error si no se puede conectar
        messagebox.showerror(
            "Error de Conexion",
            f"No se pudo conectar a MySQL.\n\n"
            f"Verifica que XAMPP este corriendo y la BD exista.\n\n"
            f"Error: {e}"
        )
        return None


def obtener_todos_videojuegos(busqueda=""):
    """Retorna todos los videojuegos de la base de datos, opcionalmente filtrados por titulo."""
    conn = crear_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        if busqueda:
            sql = "SELECT ID, Titulo, Genero, Clasificacion, Plataforma FROM Videojuegos WHERE LOWER(Titulo) LIKE LOWER(%s) ORDER BY ID"
            cursor.execute(sql, (f"%{busqueda}%",))
        else:
            cursor.execute("SELECT ID, Titulo, Genero, Clasificacion, Plataforma FROM Videojuegos ORDER BY ID")
        registros = cursor.fetchall()
        return registros
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al obtener datos:\n{e}")
        return []
    finally:
        conn.close()


def existe_videojuego(titulo):
    """
    Verifica si ya existe un videojuego con ese titulo en la BD.
    (Validacion implementada para evitar registros duplicados).
    """
    conn = crear_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Videojuegos WHERE LOWER(Titulo) = LOWER(%s)", (titulo,))
        cantidad = cursor.fetchone()[0]
        return cantidad > 0
    except Error as e: # Manejo de excepciones SQL
        print(f"Error al verificar duplicado: {e}")
        return False
    finally:
        conn.close()

def agregar_videojuego(titulo, genero, clasificacion, plataforma):
    """Inserta un nuevo videojuego en la base de datos (Maneja Excepciones)."""
    conn = crear_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Obtener el proximo ID automaticamente
        cursor.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM Videojuegos")
        nuevo_id = cursor.fetchone()[0]

        sql = "INSERT INTO Videojuegos (ID, Titulo, Genero, Clasificacion, Plataforma) VALUES (%s, %s, %s, %s, %s)"
        valores = (nuevo_id, titulo, genero, clasificacion, plataforma)
        cursor.execute(sql, valores)
        conn.commit()
        return True
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al agregar:\n{e}")
        return False
    finally:
        conn.close()


def eliminar_videojuego(id_juego):
    """Elimina un videojuego por su ID."""
    conn = crear_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Videojuegos WHERE ID = %s", (id_juego,))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al eliminar:\n{e}")
        return False
    finally:
        conn.close()


def actualizar_videojuego(id_juego, titulo, genero, clasificacion, plataforma):
    """Actualiza los datos de un videojuego existente."""
    conn = crear_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        sql = """UPDATE Videojuegos
                 SET Titulo=%s, Genero=%s, Clasificacion=%s, Plataforma=%s
                 WHERE ID=%s"""
        cursor.execute(sql, (titulo, genero, clasificacion, plataforma, id_juego))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al actualizar:\n{e}")
        return False
    finally:
        conn.close()


# ============================================================
# INTERFAZ GRAFICA - APLICACION TKINTER
# ============================================================

class AppVideojuegos:
    def __init__(self, root):
        self.root = root
        self.root.title("IACC - Gestion de Videojuegos")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg="#11001c")

        # Variable para guardar el ID del registro seleccionado
        self.id_seleccionado = None

        self._construir_interfaz()
        self._cargar_tabla()

    # ----------------------------------------------------------
    # CONSTRUCCION DE LA INTERFAZ
    # ----------------------------------------------------------
    def _construir_interfaz(self):
        """Construye todos los widgets de la aplicación."""

        # ---- TITULO ----
        frame_titulo = tk.Frame(self.root, bg="#2d004d", pady=10)
        frame_titulo.pack(fill="x")
        tk.Label(
            frame_titulo,
            text="Sistema de Gestion de Videojuegos",
            font=("Arial", 16, "bold"),
            bg="#2d004d", fg="#00e5ff"
        ).pack()
        tk.Label(
            frame_titulo,
            text="IACC - Programación Avanzada | Semana 8 - Claudio Baeza H.",
            font=("Arial", 9),
            bg="#2d004d", fg="#ff007f"
        ).pack()

        # ---- CONTENIDO PRINCIPAL ----
        frame_main = tk.Frame(self.root, bg="#11001c")
        frame_main.pack(fill="both", expand=True, padx=15, pady=10)

        # ---- PANEL IZQUIERDO: Formulario ----
        frame_form = tk.LabelFrame(
            frame_main, text="Datos del Videojuego",
            bg="#2d004d", fg="#ffe800",
            font=("Arial", 10, "bold"), padx=10, pady=10
        )
        frame_form.pack(side="left", fill="y", padx=(0, 10))

        estilo_label = {"bg": "#2d004d", "fg": "#00e5ff", "font": ("Arial", 9), "anchor": "w"}
        estilo_entry = {"width": 30, "bg": "#11001c", "fg": "#ffe800",
                        "insertbackground": "#00e5ff", "relief": "solid",
                        "font": ("Arial", 9)}

        # Campo Titulo
        tk.Label(frame_form, text="Titulo del Videojuego:", **estilo_label).grid(row=0, column=0, sticky="w", pady=(5,2))
        self.entry_titulo = tk.Entry(frame_form, **estilo_entry)
        self.entry_titulo.grid(row=1, column=0, pady=(0,8), ipady=4)

        # Campo Genero
        tk.Label(frame_form, text="Genero:", **estilo_label).grid(row=2, column=0, sticky="w", pady=(0,2))
        self.combo_genero = ttk.Combobox(
            frame_form, width=28, state="readonly",
            values=["Accion", "Aventura", "RPG", "Deportes", "Estrategia",
                    "Simulacion", "Terror", "Pelea", "Carreras", "Plataforma","First-Person Shooter" ,"Otro"]
        )
        self.combo_genero.grid(row=3, column=0, pady=(0,8), ipady=3)
        self.combo_genero.set("Aventura")

        # Campo Clasificacion
        tk.Label(frame_form, text="Clasificacion:", **estilo_label).grid(row=4, column=0, sticky="w", pady=(0,2))
        self.combo_clasif = ttk.Combobox(
            frame_form, width=28, state="readonly",
            values=["E (Todos)", "E10+ (Mayores de 10)", "T (Adolescentes)",
                    "M (Adultos)", "Mature", "AO (Solo adultos)"]
        )
        self.combo_clasif.grid(row=5, column=0, pady=(0,8), ipady=3)
        self.combo_clasif.set("E10+ (Mayores de 10)")

        # Campo Plataforma
        tk.Label(frame_form, text="Plataforma:", **estilo_label).grid(row=6, column=0, sticky="w", pady=(0,2))
        self.combo_plat = ttk.Combobox(
            frame_form, width=28, state="readonly",
            values=["PC", "PlayStation 4", "PlayStation 5", "Xbox One",
                    "Xbox Series X", "Nintendo Switch", "Multiplataforma", "Mobile"]
        )
        self.combo_plat.grid(row=7, column=0, pady=(0,15), ipady=3)
        self.combo_plat.set("PC")

        # ---- BOTONES CRUD ----
        frame_botones = tk.Frame(frame_form, bg="#2d004d")
        frame_botones.grid(row=8, column=0, pady=5)

        btn_style = {"font": ("Arial", 9, "bold"), "width": 13, "relief": "flat",
                     "cursor": "hand2", "pady": 6}

        tk.Button(
            frame_botones, text="+ AGREGAR",
            bg="#00e5ff", fg="black",
            command=self._agregar, **btn_style
        ).grid(row=0, column=0, padx=3, pady=3)

        tk.Button(
            frame_botones, text="✎ ACTUALIZAR",
            bg="#ffe800", fg="black",
            command=self._actualizar, **btn_style
        ).grid(row=0, column=1, padx=3, pady=3)

        tk.Button(
            frame_botones, text="✕ ELIMINAR",
            bg="#ff007f", fg="white",
            command=self._eliminar, **btn_style
        ).grid(row=1, column=0, padx=3, pady=3)

        tk.Button(
            frame_botones, text="↺ LIMPIAR",
            bg="#4a0072", fg="white",
            command=self._limpiar_formulario, **btn_style
        ).grid(row=1, column=1, padx=3, pady=3)

        # ---- PANEL DERECHO: Buscador y Tabla ----
        frame_derecho = tk.Frame(frame_main, bg="#11001c")
        frame_derecho.pack(side="right", fill="both", expand=True)

        # Barra de búsqueda
        frame_buscador = tk.Frame(frame_derecho, bg="#11001c")
        frame_buscador.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            frame_buscador, text="🔍 Buscar por Título:", 
            bg="#11001c", fg="#00e5ff", font=("Arial", 10, "bold")
        ).pack(side="left")
        
        self.entry_buscar = tk.Entry(
            frame_buscador, width=30, bg="#2d004d", fg="#ffe800",
            insertbackground="#00e5ff", relief="solid", font=("Arial", 10)
        )
        self.entry_buscar.pack(side="left", padx=10, ipady=4)
        self.entry_buscar.bind("<KeyRelease>", self._filtrar_tabla)

        # Tabla de videojuegos
        frame_tabla = tk.LabelFrame(
            frame_derecho, text="Lista de Videojuegos en la Base de Datos",
            bg="#2d004d", fg="#ffe800",
            font=("Arial", 10, "bold"), padx=5, pady=5
        )
        frame_tabla.pack(fill="both", expand=True)

        # Configurar estilo de la tabla
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Treeview",
            background="#11001c", foreground="#00e5ff",
            fieldbackground="#11001c", rowheight=28,
            font=("Arial", 9)
        )
        estilo.configure("Treeview.Heading",
            background="#ff007f", foreground="white",
            font=("Arial", 9, "bold"), relief="flat"
        )
        estilo.map("Treeview", background=[("selected", "#ffe800")], foreground=[("selected", "black")])

        columnas = ("ID", "Titulo", "Genero", "Clasificacion", "Plataforma")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=18)

        # Configurar columnas
        self.tabla.heading("ID",           text="ID",           anchor="center")
        self.tabla.heading("Titulo",       text="Titulo",       anchor="w")
        self.tabla.heading("Genero",       text="Genero",       anchor="center")
        self.tabla.heading("Clasificacion",text="Clasificacion",anchor="center")
        self.tabla.heading("Plataforma",   text="Plataforma",   anchor="center")

        self.tabla.column("ID",            width=40,  anchor="center")
        self.tabla.column("Titulo",        width=260, anchor="w")
        self.tabla.column("Genero",        width=100, anchor="center")
        self.tabla.column("Clasificacion", width=110, anchor="center")
        self.tabla.column("Plataforma",    width=120, anchor="center")

        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)

        # Evento: al hacer clic en una fila, carga los datos en el formulario
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        # ---- BARRA DE ESTADO ----
        self.lbl_estado = tk.Label(
            self.root, text="Listo. Conectado a MySQL en localhost.",
            bg="#11001c", fg="#ff007f", font=("Arial", 8), anchor="w", padx=10
        )
        self.lbl_estado.pack(fill="x", side="bottom")

    # ----------------------------------------------------------
    # OPERACIONES CRUD
    # ----------------------------------------------------------

    def _agregar(self):
        """Valida los datos y agrega un nuevo videojuego."""
        titulo      = self.entry_titulo.get().strip()
        genero      = self.combo_genero.get().strip()
        clasificacion = self.combo_clasif.get().strip()
        plataforma  = self.combo_plat.get().strip()

        if not titulo:
            messagebox.showwarning("Campo Vacio", "Debes ingresar el Titulo del videojuego.")
            self.entry_titulo.focus()
            return

        # VALIDACION EXTRA: Prevenir registros duplicados (recomendado por el profesor)
        if existe_videojuego(titulo):
            messagebox.showwarning("Registro Duplicado", f"El videojuego '{titulo}' ya se encuentra registrado.")
            self.entry_titulo.focus()
            return

        if agregar_videojuego(titulo, genero, clasificacion, plataforma):
            messagebox.showinfo("Exito", f"El videojuego '{titulo}' fue agregado correctamente.")
            self._limpiar_formulario()
            self._cargar_tabla()
            self._actualizar_estado(f"Videojuego '{titulo}' agregado.")
        else:
            messagebox.showerror("Error", "No se pudo agregar el videojuego.")

    def _eliminar(self):
        """Elimina el videojuego seleccionado de la tabla."""
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin Seleccion", "Selecciona un videojuego de la lista para eliminarlo.")
            return

        titulo = self.entry_titulo.get()
        confirmar = messagebox.askyesno(
            "Confirmar Eliminacion",
            f"¿Estas seguro de que deseas eliminar el videojuego?\n\n'{titulo}'"
        )
        if confirmar:
            if eliminar_videojuego(self.id_seleccionado):
                messagebox.showinfo("Exito", f"Videojuego '{titulo}' eliminado correctamente.")
                self._limpiar_formulario()
                self._cargar_tabla()
                self._actualizar_estado(f"Videojuego '{titulo}' eliminado.")

    def _actualizar(self):
        """Actualiza los datos del videojuego seleccionado."""
        if self.id_seleccionado is None:
            messagebox.showwarning("Sin Seleccion",
                "Primero selecciona un videojuego de la lista,\nluego modifica los campos y presiona ACTUALIZAR.")
            return

        titulo        = self.entry_titulo.get().strip()
        genero        = self.combo_genero.get().strip()
        clasificacion = self.combo_clasif.get().strip()
        plataforma    = self.combo_plat.get().strip()

        if not titulo:
            messagebox.showwarning("Campo Vacio", "El Titulo no puede estar vacio.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Actualizacion",
            f"¿Estas seguro de que deseas guardar los cambios para el videojuego '{titulo}'?"
        )
        if confirmar:
            if actualizar_videojuego(self.id_seleccionado, titulo, genero, clasificacion, plataforma):
                messagebox.showinfo("Exito", f"Videojuego actualizado correctamente.")
                self._limpiar_formulario()
                self._cargar_tabla()
                self._actualizar_estado(f"Videojuego ID {self.id_seleccionado} actualizado.")

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.entry_titulo.delete(0, tk.END)
        self.combo_genero.set("Aventura")
        self.combo_clasif.set("E10+ (Mayores de 10)")
        self.combo_plat.set("PC")
        self.id_seleccionado = None

    # ----------------------------------------------------------
    # CARGAR DATOS EN LA TABLA
    # ----------------------------------------------------------

    def _cargar_tabla(self, busqueda=""):
        """Recarga los videojuegos en la tabla. Si hay busqueda, aplica el filtro."""
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        registros = obtener_todos_videojuegos(busqueda)
        for reg in registros:
            self.tabla.insert("", tk.END, values=reg)

        total = len(registros)
        if busqueda:
            self._actualizar_estado(f"Resultados de busqueda: {total} videojuegos.")
        else:
            self._actualizar_estado(f"Base de datos cargada. Total de videojuegos: {total}")

    def _filtrar_tabla(self, event):
        """Evento que se dispara al escribir en el buscador."""
        texto = self.entry_buscar.get().strip()
        self._cargar_tabla(texto)

    def _seleccionar_fila(self, event):
        """Al hacer clic en una fila, carga sus datos en el formulario."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        fila = self.tabla.item(seleccion[0])["values"]
        # fila = (ID, Titulo, Genero, Clasificacion, Plataforma)
        self.id_seleccionado = fila[0]

        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, fila[1])
        self.combo_genero.set(fila[2])
        self.combo_clasif.set(fila[3])
        self.combo_plat.set(fila[4])

        self._actualizar_estado(f"Videojuego seleccionado: ID {fila[0]} - {fila[1]}")

    def _actualizar_estado(self, mensaje):
        """Actualiza el texto de la barra de estado."""
        self.lbl_estado.config(text=f"  {mensaje}")


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = AppVideojuegos(root)
    root.mainloop()