"""
Servicio de archivos
--------------------
Encapsula la lectura y escritura de archivos JSON.
De esta manera, ninguna otra capa (ni la UI, ni el servicio de
negocio) manipula archivos directamente.
"""

import json
import os


class ArchivoServicio:
    def __init__(self, ruta_archivo: str):
        self.ruta = ruta_archivo

    def leer(self) -> list:
        """Lee la lista almacenada en el archivo JSON. Si el
        archivo no existe o está vacío, devuelve una lista vacía."""
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    return []
                return json.loads(contenido)
        except (json.JSONDecodeError, OSError):
            return []

    def escribir(self, datos: list) -> None:
        """Guarda la lista de diccionarios en el archivo JSON."""
        # Se asegura que exista el directorio
        directorio = os.path.dirname(self.ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
