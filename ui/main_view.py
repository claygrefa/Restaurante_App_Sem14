"""
Vista principal (MainView)
--------------------------
Interfaz principal del sistema. Está organizada mediante
CONTENEDORES y COMPONENTES de Tkinter/ttk:

    - Notebook (pestañas): separa la sección de Usuarios y Productos
    - LabelFrame: agrupa el formulario, las acciones y la tabla
    - Frame: contenedores intermedios para organizar filas
    - Treeview: muestra la información en forma tabular
    - Entry / Label / Button: componentes básicos
    - grid() y pack(): gestores de geometría estudiados

La UI SOLO coordina lo que ve el usuario. Toda la lógica se
delega a RestauranteServicio (validaciones, persistencia, etc.).
Los botones utilizan siempre command= como pide la actividad.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class MainView:
    def __init__(self, servicio, usuario_actual: str = ""):
        self.servicio = servicio
        self.usuario_actual = usuario_actual

        # ----- Ventana principal -----
        self.ventana = tk.Tk()
        self.ventana.title("Restaurante App")
        self.ventana.geometry("760x520")
        self.ventana.minsize(720, 480)
        self.ventana.configure(bg="#f0f2f5")

        # ---------- Contenedor superior (encabezado) ----------
        encabezado = ttk.Frame(self.ventana, padding=(10, 8))
        encabezado.pack(fill="x")

        ttk.Label(encabezado, text="Sistema de gestión ",
                  font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Label(encabezado,
                  text=f"Usuario: {self.usuario_actual}",
                  font=("Segoe UI", 10)).pack(side="right")

        # Separador visual
        ttk.Separator(self.ventana, orient="horizontal").pack(fill="x")

        # ---------- Contenedor de contenido (Notebook) ----------
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Se arman las dos pestañas
        self._construir_pestana_usuarios()
        self._construir_pestana_productos()

        # ---------- Barra inferior ----------
        pie = ttk.Frame(self.ventana, padding=(10, 5))
        pie.pack(fill="x")
        ttk.Button(pie, text="Salir",
                   command=self.ventana.destroy).pack(side="right")

        # Al arrancar se cargan los datos en las tablas
        self._cargar_usuarios()
        self._cargar_productos()

    # ==================================================================
    # PESTAÑA USUARIOS - solo consulta
    # ==================================================================
    def _construir_pestana_usuarios(self):
        pestana = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(pestana, text="Usuarios")

        # Contenedor con la tabla de usuarios
        marco = ttk.LabelFrame(pestana, text="Usuarios registrados",
                               padding=10)
        marco.pack(expand=True, fill="both")

        columnas = ("usuario", "rol")
        self.tabla_usuarios = ttk.Treeview(marco, columns=columnas,
                                           show="headings", height=10)
        self.tabla_usuarios.heading("usuario", text="Usuario")
        self.tabla_usuarios.heading("rol", text="Rol")
        self.tabla_usuarios.column("usuario", width=200, anchor="w")
        self.tabla_usuarios.column("rol", width=150, anchor="center")

        # Scroll vertical
        scroll = ttk.Scrollbar(marco, orient="vertical",
                               command=self.tabla_usuarios.yview)
        self.tabla_usuarios.configure(yscrollcommand=scroll.set)

        self.tabla_usuarios.pack(side="left", expand=True, fill="both")
        scroll.pack(side="right", fill="y")

        # Contenedor de acciones para usuarios
        acciones = ttk.Frame(pestana)
        acciones.pack(fill="x", pady=(10, 0))
        ttk.Button(acciones, text="Actualizar lista",
                   command=self._cargar_usuarios).pack(side="left")

    def _cargar_usuarios(self):
        # Limpia la tabla y vuelve a cargarla
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)
        for u in self.servicio.obtener_usuarios():
            self.tabla_usuarios.insert("", "end", values=(u.usuario, u.rol))

    # ==================================================================
    # PESTAÑA PRODUCTOS - CRUD
    # ==================================================================
    def _construir_pestana_productos(self):
        pestana = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(pestana, text="Productos")

        # ---------- Contenedor: Formulario ----------
        formulario = ttk.LabelFrame(pestana, text="Datos del producto",
                                    padding=10)
        formulario.pack(fill="x")

        # Fila 1: ID y Nombre
        ttk.Label(formulario, text="ID:").grid(row=0, column=0,
                                               sticky="w", padx=5, pady=5)
        self.entry_id = ttk.Entry(formulario, width=15)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2,
                                                   sticky="w", padx=5, pady=5)
        self.entry_nombre = ttk.Entry(formulario, width=30)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Fila 2: Categoría, Precio, Stock
        ttk.Label(formulario, text="Categoría:").grid(row=1, column=0,
                                                      sticky="w", padx=5, pady=5)
        self.combo_categoria = ttk.Combobox(
            formulario, width=13, state="readonly",
            values=("Desayuno", "Plato fuerte", "Postre",
                    "Bebida", "Snack"))
        self.combo_categoria.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Precio ($):").grid(row=1, column=2,
                                                       sticky="w", padx=5, pady=5)
        self.entry_precio = ttk.Entry(formulario, width=12)
        self.entry_precio.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Stock:").grid(row=1, column=4,
                                                  sticky="w", padx=5, pady=5)
        self.entry_stock = ttk.Entry(formulario, width=10)
        self.entry_stock.grid(row=1, column=5, padx=5, pady=5, sticky="w")

        # ---------- Contenedor: Acciones (botones command=) ----------
        acciones = ttk.LabelFrame(pestana, text="Acciones", padding=10)
        acciones.pack(fill="x", pady=10)

        ttk.Button(acciones, text="Registrar",
                   command=self._registrar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Consultar",
                   command=self._consultar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Actualizar",
                   command=self._actualizar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Eliminar",
                   command=self._eliminar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Limpiar",
                   command=self._limpiar_formulario).pack(side="left", padx=5)
        ttk.Button(acciones, text="Recargar tabla",
                   command=self._cargar_productos).pack(side="right", padx=5)

        # ---------- Contenedor: Tabla ----------
        marco_tabla = ttk.LabelFrame(pestana, text="Productos registrados",
                                     padding=10)
        marco_tabla.pack(expand=True, fill="both")

        columnas = ("id", "nombre", "categoria", "precio", "stock")
        self.tabla_productos = ttk.Treeview(marco_tabla, columns=columnas,
                                            show="headings", height=8)
        self.tabla_productos.heading("id", text="ID")
        self.tabla_productos.heading("nombre", text="Nombre")
        self.tabla_productos.heading("categoria", text="Categoría")
        self.tabla_productos.heading("precio", text="Precio ($)")
        self.tabla_productos.heading("stock", text="Stock")
        self.tabla_productos.column("id", width=70, anchor="center")
        self.tabla_productos.column("nombre", width=200, anchor="w")
        self.tabla_productos.column("categoria", width=130, anchor="center")
        self.tabla_productos.column("precio", width=90, anchor="e")
        self.tabla_productos.column("stock", width=70, anchor="center")

        scroll = ttk.Scrollbar(marco_tabla, orient="vertical",
                               command=self.tabla_productos.yview)
        self.tabla_productos.configure(yscrollcommand=scroll.set)
        self.tabla_productos.pack(side="left", expand=True, fill="both")
        scroll.pack(side="right", fill="y")

    # ------------------------------------------------------------------
    # Operaciones sobre productos (delegan al servicio)
    # ------------------------------------------------------------------
    def _registrar(self):
        datos = self._leer_formulario()
        ok, mensaje = self.servicio.registrar_producto(
            datos["id"], datos["nombre"], datos["categoria"],
            datos["precio"], datos["stock"])
        self._mostrar_resultado(ok, mensaje)
        if ok:
            self._cargar_productos()
            self._limpiar_formulario()

    def _consultar(self):
        id_producto = self.entry_id.get().strip()
        if not id_producto:
            messagebox.showwarning("Consulta",
                                   "Debe indicar el ID del producto a consultar.")
            return
        producto = self.servicio.buscar_producto(id_producto)
        if producto is None:
            messagebox.showinfo("Consulta",
                                f"No se encontró el producto '{id_producto}'.")
            return
        # Se cargan los datos en el formulario
        self._limpiar_formulario(mantener_id=True)
        self.entry_nombre.insert(0, producto.nombre)
        self.combo_categoria.set(producto.categoria)
        self.entry_precio.insert(0, str(producto.precio))
        self.entry_stock.insert(0, str(producto.stock))
        messagebox.showinfo("Consulta",
                            f"Producto '{producto.id}' cargado en el formulario.")

    def _actualizar(self):
        datos = self._leer_formulario()
        ok, mensaje = self.servicio.actualizar_producto(
            datos["id"], datos["nombre"], datos["categoria"],
            datos["precio"], datos["stock"])
        self._mostrar_resultado(ok, mensaje)
        if ok:
            self._cargar_productos()

    def _eliminar(self):
        id_producto = self.entry_id.get().strip()
        if not id_producto:
            messagebox.showwarning("Eliminar",
                                   "Debe indicar el ID del producto a eliminar.")
            return
        confirmar = messagebox.askyesno(
            "Confirmar",
            f"¿Está seguro de eliminar el producto '{id_producto}'?")
        if not confirmar:
            return
        ok, mensaje = self.servicio.eliminar_producto(id_producto)
        self._mostrar_resultado(ok, mensaje)
        if ok:
            self._cargar_productos()
            self._limpiar_formulario()

    # ------------------------------------------------------------------
    # Utilidades de la vista
    # ------------------------------------------------------------------
    def _cargar_productos(self):
        for item in self.tabla_productos.get_children():
            self.tabla_productos.delete(item)
        for p in self.servicio.obtener_productos():
            self.tabla_productos.insert(
                "", "end",
                values=(p.id, p.nombre, p.categoria,
                        f"{p.precio:.2f}", p.stock))

    def _leer_formulario(self) -> dict:
        return {
            "id": self.entry_id.get().strip(),
            "nombre": self.entry_nombre.get().strip(),
            "categoria": self.combo_categoria.get().strip(),
            "precio": self.entry_precio.get().strip(),
            "stock": self.entry_stock.get().strip(),
        }

    def _limpiar_formulario(self, mantener_id: bool = False):
        if not mantener_id:
            self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.combo_categoria.set("")
        self.entry_precio.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)

    def _mostrar_resultado(self, ok: bool, mensaje: str):
        if ok:
            messagebox.showinfo("Operación exitosa", mensaje)
        else:
            messagebox.showerror("No se pudo completar", mensaje)

    def mostrar(self):
        """Muestra la ventana principal."""
        self.ventana.mainloop()
