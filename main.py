"""
main.py - Punto de entrada del sistema restaurante_app
------------------------------------------------------
Orquesta el flujo general:
    1. Se instancia el servicio del restaurante.
    2. Se muestra la ventana de inicio de sesión (LoginView).
    3. Si el acceso es válido, se abre la ventana principal (MainView).
"""

from servicios import RestauranteServicio
from ui import LoginView, MainView


def main():
    servicio = RestauranteServicio()

    # 1) Inicio de sesión
    login = LoginView(servicio)
    login.mostrar()

    # 2) Si el usuario ingresó correctamente, se abre la vista principal
    if login.acceso_ok:
        principal = MainView(servicio, usuario_actual=login.usuario_actual)
        principal.mostrar()


if __name__ == "__main__":
    main()
