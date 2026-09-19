"""
Vista de inicio de sesión (LoginView)
-------------------------------------
Ventana Tkinter que solicita usuario y contraseña.
La validación NO se realiza aquí: se delega a
RestauranteServicio.validar_credenciales().
"""

import tkinter as tk
from tkinter import ttk, messagebox


class LoginView:
    def __init__(self, servicio):
        self.servicio = servicio
        self.acceso_ok = False           # bandera de acceso concedido
        self.usuario_actual = None       # se guarda el usuario que ingresó

        # ----- Ventana principal del login -----
        self.ventana = tk.Tk()
        self.ventana.title("Restaurante App - Inicio de sesión")
        self.ventana.geometry("380x260")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f2f5")

        # ----- Contenedor principal (Frame) -----
        contenedor = ttk.Frame(self.ventana, padding=20)
        contenedor.pack(expand=True, fill="both")

        # ----- Título -----
        titulo = ttk.Label(contenedor, text="Restaurante App",
                           font=("Segoe UI", 16, "bold"))
        titulo.pack(pady=(0, 5))
        subtitulo = ttk.Label(contenedor, text="Inicio de sesión",
                              font=("Segoe UI", 10))
        subtitulo.pack(pady=(0, 15))

        # ----- Formulario (contenedor con grid) -----
        formulario = ttk.Frame(contenedor)
        formulario.pack(fill="x")

        ttk.Label(formulario, text="Usuario:").grid(row=0, column=0,
                                                    sticky="w", pady=5)
        self.entry_usuario = ttk.Entry(formulario, width=25)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Contraseña:").grid(row=1, column=0,
                                                       sticky="w", pady=5)
        self.entry_contrasena = ttk.Entry(formulario, width=25, show="*")
        self.entry_contrasena.grid(row=1, column=1, padx=5, pady=5)

        # ----- Contenedor de acciones -----
        acciones = ttk.Frame(contenedor)
        acciones.pack(pady=15)

        ttk.Button(acciones, text="Ingresar",
                   command=self._ingresar).pack(side="left", padx=5)
        ttk.Button(acciones, text="Salir",
                   command=self.ventana.destroy).pack(side="left", padx=5)

        # Poner foco en el primer campo
        self.entry_usuario.focus()

    # ------------------------------------------------------------------
    # Acciones (siempre delegan al servicio)
    # ------------------------------------------------------------------
    def _ingresar(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if self.servicio.validar_credenciales(usuario, contrasena):
            self.acceso_ok = True
            self.usuario_actual = usuario
            messagebox.showinfo("Acceso concedido",
                                f"Bienvenido, {usuario}.")
            self.ventana.destroy()
        else:
            messagebox.showerror("Acceso denegado",
                                 "Usuario o contraseña incorrectos.")
            self.entry_contrasena.delete(0, tk.END)

    def mostrar(self):
        """Muestra la ventana y espera hasta que se cierre."""
        self.ventana.mainloop()
