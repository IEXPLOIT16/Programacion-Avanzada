# ============================================================
#  PROGRAMACION AVANZADA - SEMANA 9 evaluacion final
#  Clínica SaludTotal - Gestión de Pacientes Avanzada - IACC
#  Autor: Claudio Baeza Henríquez  - 2026
# ============================================================
import os
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import datetime
import random
import re

# ============================================================
# CONFIGURACION DE LA BASE DE DATOS
# ============================================================
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': '',
    'database': 'clinica_saludtotal'
}

# ============================================================
# FUNCIONES DE BASE DE DATOS
# ============================================================

def crear_conexion():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        messagebox.showerror("Error de Conexion", f"No se pudo conectar a la BD clinica_saludtotal.\nError: {e}")
        return None

def obtener_pacientes(busqueda=""):
    conn = crear_conexion()
    if not conn: return []
    try:
        cursor = conn.cursor()
        if busqueda:
            sql = "SELECT ID, RUT, NumFicha, Nombre, Edad, Genero, HistorialMedico, Telefono, Correo, Especialidad, Estado, FechaIngreso FROM Pacientes WHERE LOWER(Nombre) LIKE LOWER(%s) OR RUT LIKE %s ORDER BY ID"
            termino = f"%{busqueda}%"
            cursor.execute(sql, (termino, termino))
        else:
            cursor.execute("SELECT ID, RUT, NumFicha, Nombre, Edad, Genero, HistorialMedico, Telefono, Correo, Especialidad, Estado, FechaIngreso FROM Pacientes ORDER BY ID")
        return cursor.fetchall()
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al leer pacientes:\n{e}")
        return []
    finally:
        conn.close()

def paciente_existe(rut):
    conn = crear_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Pacientes WHERE RUT = %s", (rut,))
        return cursor.fetchone()[0] > 0
    except Error: return False
    finally: conn.close()

def agregar_paciente(rut, num_ficha, nombre, edad, genero, historial, telefono, correo, especialidad, estado):
    conn = crear_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        fecha_ingreso = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO Pacientes (RUT, NumFicha, Nombre, Edad, Genero, HistorialMedico, Telefono, Correo, Especialidad, Estado, FechaIngreso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (rut, num_ficha, nombre, edad, genero, historial, telefono, correo, especialidad, estado, fecha_ingreso))
        conn.commit()
        return True
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al agregar:\n{e}")
        return False
    finally:
        conn.close()

def actualizar_paciente(id_paciente, rut, nombre, edad, genero, historial, telefono, correo, especialidad, estado):
    conn = crear_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = """UPDATE Pacientes 
                 SET RUT=%s, Nombre=%s, Edad=%s, Genero=%s, HistorialMedico=%s, Telefono=%s, Correo=%s, Especialidad=%s, Estado=%s 
                 WHERE ID=%s"""
        cursor.execute(sql, (rut, nombre, edad, genero, historial, telefono, correo, especialidad, estado, id_paciente))
        conn.commit()
        return cursor.rowcount > 0
    except Error as e:
        messagebox.showerror("Error SQL", f"Error al actualizar:\n{e}")
        return False
    finally:
        conn.close()

def eliminar_paciente(id_paciente):
    conn = crear_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Pacientes WHERE ID = %s", (id_paciente,))
        conn.commit()
        return cursor.rowcount > 0
    except Error: return False
    finally: conn.close()


# ============================================================
# INTERFAZ GRAFICA
# ============================================================

class AppSaludTotal:
    def __init__(self, root):
        self.root = root
        self.root.title("Clínica SaludTotal - Gestión de Pacientes Avanzada")
        self.root.geometry("1300x700")
        
        self.color_bg = "#f0f4f8"
        self.color_primary = "#0056b3"
        self.color_text = "#333333"
        self.color_white = "#ffffff"

        self.root.configure(bg=self.color_bg)
        self.id_seleccionado = None

        self._construir_interfaz()
        self._cargar_tabla()

    def _construir_interfaz(self):
        lbl_titulo = tk.Label(self.root, text="🏥 Sistema de Gestión de Pacientes - Clínica SaludTotal", bg=self.color_primary, fg=self.color_white, font=("Segoe UI", 16, "bold"), pady=5)
        lbl_titulo.pack(fill="x")

        lbl_subtitulo = tk.Label(self.root, text="IACC - Programación Avanzada | Semana 9 - Claudio Baeza H.", bg=self.color_primary, fg="#e0e0e0", font=("Segoe UI", 10, "italic"), pady=5)
        lbl_subtitulo.pack(fill="x")

        frame_main = tk.Frame(self.root, bg=self.color_bg, padx=10, pady=10)
        frame_main.pack(fill="both", expand=True)

        # Panel Izquierdo (Formulario 2 columnas)
        frame_izq = tk.Frame(frame_main, bg=self.color_bg)
        frame_izq.pack(side="left", fill="y", padx=(0, 10))

        frame_form = tk.LabelFrame(frame_izq, text="Ficha Médica del Paciente", bg=self.color_white, fg=self.color_primary, font=("Segoe UI", 11, "bold"), padx=15, pady=10, relief="solid", bd=1)
        frame_form.pack(fill="both", expand=True)

        label_font = ("Segoe UI", 9, "bold")
        entry_font = ("Segoe UI", 9)

        # Fila 0: RUT y Edad
        tk.Label(frame_form, text="RUT del Paciente:", bg="white", fg=self.color_text, font=label_font).grid(row=0, column=0, sticky="w", pady=(2,0))
        tk.Label(frame_form, text="Edad:", bg="white", fg=self.color_text, font=label_font).grid(row=0, column=1, sticky="w", padx=10, pady=(2,0))
        
        self.entry_rut = tk.Entry(frame_form, width=22, font=entry_font)
        self.entry_rut.grid(row=1, column=0, pady=(0,5), ipady=3, sticky="w")
        self.entry_rut.bind("<KeyRelease>", self._formatear_rut)
        
        self.entry_edad = tk.Entry(frame_form, width=15, font=entry_font)
        self.entry_edad.grid(row=1, column=1, padx=10, pady=(0,5), ipady=3, sticky="w")

        # Fila 2: Nombre
        tk.Label(frame_form, text="Nombre Completo:", bg="white", fg=self.color_text, font=label_font).grid(row=2, column=0, columnspan=2, sticky="w", pady=(2,0))
        self.entry_nombre = tk.Entry(frame_form, width=42, font=entry_font)
        self.entry_nombre.grid(row=3, column=0, columnspan=2, pady=(0,5), ipady=3, sticky="w")

        # Fila 4: Genero y Telefono
        tk.Label(frame_form, text="Género:", bg="white", fg=self.color_text, font=label_font).grid(row=4, column=0, sticky="w", pady=(2,0))
        tk.Label(frame_form, text="Teléfono:", bg="white", fg=self.color_text, font=label_font).grid(row=4, column=1, sticky="w", padx=10, pady=(2,0))
        
        self.combo_genero = ttk.Combobox(frame_form, values=["Masculino", "Femenino", "Otro", "Prefiere no decir"], font=entry_font, state="readonly", width=19)
        self.combo_genero.grid(row=5, column=0, pady=(0,5), ipady=3, sticky="w")
        
        self.entry_telefono = tk.Entry(frame_form, width=20, font=entry_font)
        self.entry_telefono.grid(row=5, column=1, padx=10, pady=(0,5), ipady=3, sticky="w")

        # Fila 6: Correo
        tk.Label(frame_form, text="Correo Electrónico:", bg="white", fg=self.color_text, font=label_font).grid(row=6, column=0, columnspan=2, sticky="w", pady=(2,0))
        self.entry_correo = tk.Entry(frame_form, width=42, font=entry_font)
        self.entry_correo.grid(row=7, column=0, columnspan=2, pady=(0,5), ipady=3, sticky="w")
        self.entry_correo.bind("<KeyRelease>", self._validar_correo_visual)

        # Fila 8: Especialidad y Estado
        tk.Label(frame_form, text="Especialidad Asignada:", bg="white", fg=self.color_text, font=label_font).grid(row=8, column=0, sticky="w", pady=(2,0))
        tk.Label(frame_form, text="Estado Actual:", bg="white", fg=self.color_text, font=label_font).grid(row=8, column=1, sticky="w", padx=10, pady=(2,0))
        
        esp_lista = ["Medicina General", "Pediatría", "Endocrinología", "Traumatología", "Cardiología", "Broncopulmonar"]
        self.combo_especialidad = ttk.Combobox(frame_form, values=esp_lista, font=entry_font, state="readonly", width=19)
        self.combo_especialidad.grid(row=9, column=0, pady=(0,5), ipady=3, sticky="w")
        
        est_lista = ["En Tratamiento", "Alta Médica", "Derivado", "En Observación"]
        self.combo_estado = ttk.Combobox(frame_form, values=est_lista, font=entry_font, state="readonly", width=17)
        self.combo_estado.grid(row=9, column=1, padx=10, pady=(0,5), ipady=3, sticky="w")

        # Fila 10: Historial
        tk.Label(frame_form, text="Historial Médico / Tratamiento:", bg="white", fg=self.color_text, font=label_font).grid(row=10, column=0, columnspan=2, sticky="w", pady=(2,0))
        self.text_historial = tk.Text(frame_form, width=42, height=4, font=entry_font, wrap="word")
        self.text_historial.grid(row=11, column=0, columnspan=2, pady=(0,10), sticky="w")

        # Botones CRUD
        frame_botones = tk.Frame(frame_form, bg="white")
        frame_botones.grid(row=12, column=0, columnspan=2, pady=5)
        btn_style = {"font": ("Segoe UI", 9, "bold"), "width": 14, "cursor": "hand2", "pady": 4}
        
        tk.Button(frame_botones, text="+ AGREGAR", bg="#28a745", fg="white", command=self._agregar, **btn_style).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="✎ ACTUALIZAR", bg="#ffc107", fg="black", command=self._actualizar, **btn_style).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame_botones, text="✕ ELIMINAR", bg="#dc3545", fg="white", command=self._eliminar, **btn_style).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botones, text="↺ LIMPIAR", bg="#6c757d", fg="white", command=self._limpiar_formulario, **btn_style).grid(row=1, column=1, padx=2, pady=2)
        
        # Boton Informe
        tk.Button(frame_form, text="📄 GENERAR INFORME MÉDICO", bg=self.color_primary, fg="white", font=("Segoe UI", 10, "bold"), pady=6, cursor="hand2", command=self._generar_informe).grid(row=13, column=0, columnspan=2, sticky="we", pady=(10,0))

        # Panel Derecho (Tabla)
        frame_derecho = tk.Frame(frame_main, bg=self.color_bg)
        frame_derecho.pack(side="right", fill="both", expand=True)

        frame_buscador = tk.Frame(frame_derecho, bg=self.color_bg)
        frame_buscador.pack(fill="x", pady=(0, 10))
        tk.Label(frame_buscador, text="🔍 Buscar por Nombre o RUT:", bg=self.color_bg, fg=self.color_primary, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.entry_buscar = tk.Entry(frame_buscador, width=40, font=entry_font)
        self.entry_buscar.pack(side="left", padx=10, ipady=3)
        self.entry_buscar.bind("<KeyRelease>", self._filtrar_tabla)

        frame_tabla = tk.LabelFrame(frame_derecho, text="Directorio General de Pacientes", bg=self.color_white, fg=self.color_primary, font=("Segoe UI", 11, "bold"), padx=5, pady=5, relief="solid", bd=1)
        frame_tabla.pack(fill="both", expand=True)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="white", fieldbackground="white", foreground="black", rowheight=30, font=("Segoe UI", 8))
        estilo.configure("Treeview.Heading", background=self.color_primary, foreground="white", font=("Segoe UI", 9, "bold"))
        estilo.map("Treeview", background=[("selected", "#007bff")])

        # AQUI AGREGAMOS "Historial" DE VUELTA A LAS COLUMNAS VISIBLES
        columnas = ("ID", "RUT", "Ficha", "Nombre", "Edad", "Genero", "Especialidad", "Estado", "Historial", "Telefono", "Correo", "Ingreso")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Configurar cabeceras
        for col in columnas:
            self.tabla.heading(col, text=col)

        # Configurar anchos (incluyendo historial que sera un poco mas ancho)
        anchos = [30, 80, 80, 120, 40, 70, 100, 90, 150, 80, 120, 120]
        for col, ancho in zip(columnas, anchos):
            self.tabla.column(col, width=ancho, anchor="center" if col not in ("Nombre","Correo","Historial") else "w")

        # Configurar barras de desplazamiento (Scrollbars vertical y horizontal)
        scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal", command=self.tabla.xview)
        
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tabla.pack(side="left", fill="both", expand=True)

        self.tabla.bind("<ButtonRelease-1>", self._seleccionar_fila)

        self.lbl_estado = tk.Label(self.root, text="Sistema Inicializado - Esperando acciones", bg="#d1ecf1", fg="#0c5460", font=("Segoe UI", 9), anchor="w", padx=10, pady=5)
        self.lbl_estado.pack(fill="x", side="bottom")

    # ----------------------------------------------------------
    # METODOS DE ACCION
    # ----------------------------------------------------------

    def _actualizar_estado(self, mensaje):
        self.lbl_estado.config(text=mensaje)

    def _formatear_rut(self, event):
        if event.keysym in ("BackSpace", "Delete", "Left", "Right", "Up", "Down", "Tab"):
            return
        texto = self.entry_rut.get()
        rut_limpio = ''.join(c.upper() for c in texto if c.isdigit() or c.upper() == 'K')
        if len(rut_limpio) > 1:
            cuerpo = rut_limpio[:-1]
            dv = rut_limpio[-1]
            try:
                cuerpo_fmt = "{:,}".format(int(cuerpo)).replace(',', '.')
                rut_formateado = f"{cuerpo_fmt}-{dv}"
            except ValueError:
                rut_formateado = rut_limpio
        else:
            rut_formateado = rut_limpio

        self.entry_rut.delete(0, tk.END)
        self.entry_rut.insert(0, rut_formateado)
        self.entry_rut.icursor(tk.END)

    def _validar_correo_visual(self, event):
        """Pinta el borde del campo de correo de rojo si es invalido mientras se escribe."""
        correo = self.entry_correo.get().strip()
        if not correo:
            self.entry_correo.config(highlightthickness=0)
            return
        if self._es_correo_valido(correo):
            self.entry_correo.config(highlightthickness=1, highlightbackground="green", highlightcolor="green")
        else:
            self.entry_correo.config(highlightthickness=2, highlightbackground="red", highlightcolor="red")
        
    def _generar_numero_ficha(self):
        ahora = datetime.datetime.now()
        aleatorio = random.randint(1000, 9999)
        return f"F-{ahora.year}-{aleatorio}"

    def _es_correo_valido(self, correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, correo) is not None

    def _agregar(self):
        rut = self.entry_rut.get().strip()
        nombre = self.entry_nombre.get().strip()
        edad_str = self.entry_edad.get().strip()
        genero = self.combo_genero.get() if self.combo_genero.get() != "Seleccionar..." else "No Especificado"
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()
        especialidad = self.combo_especialidad.get() if self.combo_especialidad.get() else "No Asignada"
        estado = self.combo_estado.get() if self.combo_estado.get() else "Sin Estado"
        historial = self.text_historial.get("1.0", tk.END).strip()

        if not rut or not nombre or not edad_str:
            messagebox.showwarning("Campos Requeridos", "El RUT, Nombre y Edad son obligatorios.")
            return

        try: edad = int(edad_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "La Edad debe ser un numero entero.")
            return

        if correo and not self._es_correo_valido(correo):
            messagebox.showwarning("Correo Inválido", "El formato del correo es incorrecto.")
            self.entry_correo.focus()
            return

        if paciente_existe(rut):
            messagebox.showwarning("Duplicado", f"Ya existe un paciente con el RUT '{rut}'.")
            return
            
        num_ficha = self._generar_numero_ficha()

        if agregar_paciente(rut, num_ficha, nombre, edad, genero, historial, telefono, correo, especialidad, estado):
            messagebox.showinfo("Éxito", f"Paciente registrado.\nFicha: {num_ficha}\nEspecialidad: {especialidad}")
            self._limpiar_formulario()
            self._cargar_tabla()
            self._actualizar_estado(f"Paciente '{nombre}' agregado exitosamente.")

    def _actualizar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Sin Selección", "Selecciona un paciente de la tabla.")
            return

        rut = self.entry_rut.get().strip()
        nombre = self.entry_nombre.get().strip()
        edad_str = self.entry_edad.get().strip()
        genero = self.combo_genero.get()
        telefono = self.entry_telefono.get().strip()
        correo = self.entry_correo.get().strip()
        especialidad = self.combo_especialidad.get()
        estado = self.combo_estado.get()
        historial = self.text_historial.get("1.0", tk.END).strip()

        if not rut or not nombre:
            messagebox.showwarning("Campos Requeridos", "RUT y Nombre son obligatorios.")
            return
        try: edad = int(edad_str)
        except ValueError:
            messagebox.showerror("Error de Formato", "La Edad debe ser un numero.")
            return
        if correo and not self._es_correo_valido(correo):
            messagebox.showwarning("Correo Inválido", "Por favor ingresa un correo electrónico válido.")
            return

        confirma = messagebox.askyesno("Confirmar", f"¿Actualizar datos de '{nombre}'?")
        if confirma:
            if actualizar_paciente(self.id_seleccionado, rut, nombre, edad, genero, historial, telefono, correo, especialidad, estado):
                messagebox.showinfo("Éxito", "Historial clínico actualizado.")
                self._limpiar_formulario()
                self._cargar_tabla()
                self._actualizar_estado(f"Paciente {self.id_seleccionado} actualizado.")

    def _eliminar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Sin Selección", "Selecciona un paciente para eliminar.")
            return
        nombre = self.entry_nombre.get().strip()
        confirma = messagebox.askyesno("Crítico", f"¿Eliminar permanentemente a '{nombre}'?")
        if confirma:
            if eliminar_paciente(self.id_seleccionado):
                messagebox.showinfo("Éxito", "Paciente eliminado.")
                self._limpiar_formulario()
                self._cargar_tabla()
                self._actualizar_estado(f"Paciente '{nombre}' eliminado.")

    def _limpiar_formulario(self):
        self.entry_rut.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_edad.delete(0, tk.END)
        self.combo_genero.set("")
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)
        self.entry_correo.config(highlightthickness=0)
        self.combo_especialidad.set("")
        self.combo_estado.set("")
        self.text_historial.delete("1.0", tk.END)
        self.id_seleccionado = None

    def _cargar_tabla(self, busqueda=""):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        pacientes = obtener_pacientes(busqueda)
        # ID, RUT, NumFicha, Nombre, Edad, Genero, HistorialMedico, Telefono, Correo, Especialidad, Estado, FechaIngreso
        for p in pacientes:
            # Se muestra TODO en el Treeview, ahora con el Historial en la posicion 8
            # columnas = ("ID", "RUT", "Ficha", "Nombre", "Edad", "Genero", "Especialidad", "Estado", "Historial", "Telefono", "Correo", "Ingreso")
            fila_visible = (p[0], p[1], p[2], p[3], p[4], p[5], p[9], p[10], p[6], p[7], p[8], p[11])
            self.tabla.insert("", tk.END, values=fila_visible)

        self._actualizar_estado(f"Directorio actualizado. Total: {len(pacientes)}")

    def _filtrar_tabla(self, event):
        texto = self.entry_buscar.get().strip()
        self._cargar_tabla(texto)

    def _seleccionar_fila(self, event):
        seleccion = self.tabla.selection()
        if not seleccion: return

        fila = self.tabla.item(seleccion[0])["values"]
        
        # fila = [ID, RUT, Ficha, Nombre, Edad, Genero, Especialidad, Estado, Historial, Telefono, Correo, Ingreso]
        self.id_seleccionado = fila[0]
        
        self.entry_rut.delete(0, tk.END)
        self.entry_rut.insert(0, fila[1])
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, fila[3])
        self.entry_edad.delete(0, tk.END)
        self.entry_edad.insert(0, fila[4])
        self.combo_genero.set(fila[5] if fila[5] != "None" else "")
        self.combo_especialidad.set(fila[6] if fila[6] != "None" else "")
        self.combo_estado.set(fila[7] if fila[7] != "None" else "")
        
        # El historial ahora es la posicion 8
        self.text_historial.delete("1.0", tk.END)
        self.text_historial.insert(tk.END, str(fila[8]) if fila[8] != "None" else "")
        
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, str(fila[9]) if fila[9] != "None" else "")
        
        self.entry_correo.delete(0, tk.END)
        self.entry_correo.insert(0, str(fila[10]) if fila[10] != "None" else "")
        self.entry_correo.config(highlightthickness=0)

    def _generar_informe(self):
        # Filtra los pacientes según lo que esté escrito en el buscador
        busqueda_actual = self.entry_buscar.get().strip()
        pacientes = obtener_pacientes(busqueda_actual)
        
        if not pacientes:
            messagebox.showwarning("Sin Datos", "No hay pacientes para generar informe.")
            return

        ahora = datetime.datetime.now()
        fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
        nombre_archivo = f"Informe_SaludTotal_{ahora.strftime('%Y%m%d_%H%M')}.txt"

        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write("="*80 + "\n")
                f.write("                INFORME MÉDICO DE PACIENTES - SALUDTOTAL\n")
                f.write("="*80 + "\n")
                f.write(f"Fecha de generación: {fecha_formateada}\n")
                f.write(f"Total de pacientes en sistema: {len(pacientes)}\n\n")
                
                for p in pacientes:
                    # p = ID(0), RUT(1), NumFicha(2), Nombre(3), Edad(4), Genero(5), Historial(6), Telefono(7), Correo(8), Especialidad(9), Estado(10), FechaIngreso(11)
                    f.write(f"[{p[10]}] Paciente: {p[3]} (Ficha N°: {p[2]})\n")
                    f.write(f"RUT: {p[1]} | Edad: {p[4]} | Genero: {p[5]}\n")
                    f.write(f"Especialidad: {p[9]} | Fecha Ingreso: {p[11]}\n")
                    f.write(f"Contacto: {p[7]} / {p[8]}\n")
                    f.write(f"Historial/Tratamiento: {p[6]}\n")
                    f.write("-" * 80 + "\n")

            messagebox.showinfo("Informe Generado", f"El informe fue generado exitosamente:\n\n{nombre_archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el informe.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppSaludTotal(root)
    root.mainloop()
