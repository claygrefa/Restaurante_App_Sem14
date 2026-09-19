"""
Modelo Producto
---------------
Representa un producto del restaurante. Solo contiene datos y
métodos simples para convertir a/desde diccionario (para la
persistencia en JSON).
"""


class Producto:
    def __init__(self, id_producto: str, nombre: str, categoria: str,
                 precio: float, stock: int):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = float(precio)
        self.stock = int(stock)

    # Convierte el objeto en diccionario para poder guardarlo en JSON
    def a_diccionario(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock,
        }

    # Crea un Producto a partir de un diccionario leído del JSON
    @classmethod
    def desde_diccionario(cls, datos: dict) -> "Producto":
        return cls(
            id_producto=datos.get("id", ""),
            nombre=datos.get("nombre", ""),
            categoria=datos.get("categoria", ""),
            precio=datos.get("precio", 0.0),
            stock=datos.get("stock", 0),
        )

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - {self.categoria} - ${self.precio:.2f} (stock: {self.stock})"
