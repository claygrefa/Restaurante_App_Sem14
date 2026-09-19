"""
Modelo Usuario
--------------
Representa a un usuario del sistema. Sirve para el inicio de
sesión y para la consulta de usuarios registrados.
"""


class Usuario:
    def __init__(self, usuario: str, contrasena: str, rol: str = "empleado"):
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    def a_diccionario(self) -> dict:
        return {
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "rol": self.rol,
        }

    @classmethod
    def desde_diccionario(cls, datos: dict) -> "Usuario":
        return cls(
            usuario=datos.get("usuario", ""),
            contrasena=datos.get("contrasena", ""),
            rol=datos.get("rol", "empleado"),
        )

    def __str__(self) -> str:
        return f"{self.usuario} ({self.rol})"
