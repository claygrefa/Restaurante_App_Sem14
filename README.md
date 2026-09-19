# Restaurante App - Semana 14
Nombres CLAY MEDARDO GREFA TUNAY
Proyecto desarrollado para la asignatura **Programación Orientada a Objetos**.
La actividad de la Semana 14 corresponde al taller práctico **Organización
modular de un sistema orientado a objetos en Python**, con énfasis en el uso
de **componentes y contenedores de Tkinter**.


## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/          (opcional)
├── main.py
└── README.md
```

- **datos/**: archivos JSON con la información persistente (productos y
  usuarios).
- **modelos/**: clases `Producto` y `Usuario` que representan los datos del
  sistema.
- **servicios/**:
  - `ArchivoServicio`: encapsula la lectura y escritura de archivos JSON.
  - `RestauranteServicio`: concentra la lógica de negocio (validaciones,
    operaciones sobre productos, consulta de usuarios y persistencia).
- **ui/**: capa gráfica basada en Tkinter/ttk.
  - `LoginView`: ventana de inicio de sesión.
  - `MainView`: ventana principal con las secciones de usuarios y
    productos.
- **main.py**: punto de entrada que enlaza el login con la vista principal.

## Componentes y contenedores utilizados

- **Contenedores**: `Tk`, `Frame`, `LabelFrame`, `Notebook` (pestañas) y
  `Separator`.
- **Componentes**: `Label`, `Entry`, `Combobox`, `Button`, `Treeview`
  (tabla de datos), `Scrollbar` y `messagebox` para mensajes.
- **Gestores de geometría**: se combinan `pack()` y `grid()` según el
  contenedor.
- Los botones utilizan siempre `command=` para asociar la acción.

## Mejoras realizadas en la Semana 14

- La interfaz principal se organizó en **pestañas (`Notebook`)** para
  separar la sección de usuarios y la sección de productos.
- Se agregó un **encabezado** con el nombre del sistema y el usuario que
  inició sesión.
- El formulario de productos se agrupó dentro de un `LabelFrame` y se
  distribuyó con `grid()` para lograr una presentación clara.
- Las acciones se encuentran en un contenedor de botones independiente
  (`LabelFrame` "Acciones"), lo que mejora la organización visual.
- La visualización de productos y usuarios se realiza mediante `Treeview`
  con `Scrollbar`, ofreciendo una experiencia más ordenada.
- Después de cada operación, la tabla se **actualiza automáticamente**
  para que el usuario vea el resultado.

## Operaciones implementadas sobre productos

Desde la interfaz gráfica se pueden realizar, siempre a través de
`RestauranteServicio`:

- **Registrar** un nuevo producto.
- **Consultar / Cargar** un producto por su ID (se muestra en el formulario).
- **Actualizar** los datos de un producto existente.
- **Eliminar** un producto por su ID (con mensaje de confirmación).

Además:

- **Limpiar** formulario.
- **Recargar tabla** para volver a leer los datos desde `productos.json`.

## Persistencia

La información de productos se guarda en `datos/productos.json` a través
de `ArchivoServicio`. La interfaz **nunca** manipula archivos JSON de
manera directa: siempre solicita las operaciones a `RestauranteServicio`.

## Usuarios de prueba

El archivo `datos/usuarios.json` contiene los siguientes usuarios para
poder iniciar sesión:

| Usuario | Contraseña | Rol            |
|---------|------------|----------------|
| admin   | 1234       | administrador  |
| mesero  | abcd       | empleado       |
