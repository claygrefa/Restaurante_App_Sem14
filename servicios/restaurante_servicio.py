"""
Servicio del restaurante
------------------------
Contiene TODA la lógica de negocio del sistema:
- Validación de credenciales
- Consulta de usuarios
- Operaciones CRUD sobre productos (registrar, consultar,
  actualizar, eliminar)
- Persistencia mediante ArchivoServicio

La capa de UI NUNCA debe leer o escribir JSON directamente:
siempre pasa por este servicio.
"""

import os

from modelos import Producto, Usuario
from servicios.archivo_servicio import ArchivoServicio


# Rutas relativas a la raíz del proyecto
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PRODUCTOS = os.path.join(RUTA_BASE, "datos", "productos.json")
RUTA_USUARIOS = os.path.join(RUTA_BASE, "datos", "usuarios.json")


class RestauranteServicio:
    def __init__(self):
        self._archivo_productos = ArchivoServicio(RUTA_PRODUCTOS)
        self._archivo_usuarios = ArchivoServicio(RUTA_USUARIOS)

    # ------------------------------------------------------------------
    # Usuarios
    # ------------------------------------------------------------------
    def obtener_usuarios(self) -> list:
        """Devuelve la lista de objetos Usuario registrados."""
        datos = self._archivo_usuarios.leer()
        return [Usuario.desde_diccionario(d) for d in datos]

    def validar_credenciales(self, usuario: str, contrasena: str) -> bool:
        """Retorna True si el usuario y la contraseña coinciden."""
        if not usuario or not contrasena:
            return False
        for u in self.obtener_usuarios():
            if u.usuario == usuario and u.contrasena == contrasena:
                return True
        return False

    # ------------------------------------------------------------------
    # Productos - CRUD
    # ------------------------------------------------------------------
    def obtener_productos(self) -> list:
        """Devuelve la lista completa de productos."""
        datos = self._archivo_productos.leer()
        return [Producto.desde_diccionario(d) for d in datos]

    def buscar_producto(self, id_producto: str):
        """Retorna un Producto por su id, o None si no existe."""
        id_producto = (id_producto or "").strip()
        if not id_producto:
            return None
        for p in self.obtener_productos():
            if p.id.lower() == id_producto.lower():
                return p
        return None

    def registrar_producto(self, id_producto: str, nombre: str,
                           categoria: str, precio, stock) -> tuple:
        """Registra un nuevo producto. Devuelve (ok, mensaje)."""
        # Validaciones de negocio
        error = self._validar_datos(id_producto, nombre, categoria, precio, stock)
        if error:
            return False, error

        if self.buscar_producto(id_producto) is not None:
            return False, f"Ya existe un producto con el ID '{id_producto}'."

        productos = self.obtener_productos()
        nuevo = Producto(id_producto.strip(), nombre.strip(),
                         categoria.strip(), float(precio), int(stock))
        productos.append(nuevo)
        self._guardar(productos)
        return True, f"Producto '{nuevo.nombre}' registrado correctamente."

    def actualizar_producto(self, id_producto: str, nombre: str,
                            categoria: str, precio, stock) -> tuple:
        """Actualiza los datos del producto con el ID indicado."""
        error = self._validar_datos(id_producto, nombre, categoria, precio, stock)
        if error:
            return False, error

        productos = self.obtener_productos()
        for i, p in enumerate(productos):
            if p.id.lower() == id_producto.strip().lower():
                productos[i] = Producto(p.id, nombre.strip(),
                                        categoria.strip(),
                                        float(precio), int(stock))
                self._guardar(productos)
                return True, f"Producto '{p.id}' actualizado correctamente."
        return False, f"No existe un producto con el ID '{id_producto}'."

    def eliminar_producto(self, id_producto: str) -> tuple:
        """Elimina el producto con el ID indicado."""
        id_producto = (id_producto or "").strip()
        if not id_producto:
            return False, "Debe indicar el ID del producto a eliminar."

        productos = self.obtener_productos()
        nuevos = [p for p in productos if p.id.lower() != id_producto.lower()]
        if len(nuevos) == len(productos):
            return False, f"No existe un producto con el ID '{id_producto}'."
        self._guardar(nuevos)
        return True, f"Producto '{id_producto}' eliminado correctamente."

    # ------------------------------------------------------------------
    # Ayudas internas
    # ------------------------------------------------------------------
    def _guardar(self, productos: list) -> None:
        self._archivo_productos.escribir([p.a_diccionario() for p in productos])

    def _validar_datos(self, id_producto, nombre, categoria, precio, stock):
        """Devuelve un mensaje de error o None si todo es válido."""
        if not id_producto or not str(id_producto).strip():
            return "El ID del producto es obligatorio."
        if not nombre or not str(nombre).strip():
            return "El nombre del producto es obligatorio."
        if not categoria or not str(categoria).strip():
            return "La categoría del producto es obligatoria."
        try:
            precio_val = float(precio)
            if precio_val < 0:
                return "El precio no puede ser negativo."
        except (TypeError, ValueError):
            return "El precio debe ser un número válido."
        try:
            stock_val = int(stock)
            if stock_val < 0:
                return "El stock no puede ser negativo."
        except (TypeError, ValueError):
            return "El stock debe ser un número entero."
        return None
