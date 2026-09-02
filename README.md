# To-Do API

API REST sencilla para gestionar tareas (crear, listar, actualizar y eliminar), construida como proyecto de práctica para aprender backend con Python.

## Tecnologías

- **Python 3**
- **FastAPI** — framework para construir la API
- **SQLAlchemy** — ORM para trabajar con la base de datos
- **SQLite** — base de datos ligera basada en archivo
- **Uvicorn** — servidor ASGI para ejecutar la aplicación

## Funcionalidades

- Crear una tarea nueva
- Listar todas las tareas
- Obtener una tarea concreta por su id
- Actualizar una tarea (parcialmente, solo los campos enviados)
- Eliminar una tarea
- Documentación interactiva automática (Swagger UI)

## Cómo ejecutarlo en local

1. Clona el repositorio:

git clone https://github.com/Fralonso16/todo-api.git
cd todo-api

2. Crea y activa un entorno virtual:

python -m venv venv
venv\Scripts\Activate


3. Instala las dependencias:

pip install -r requirements.txt


4. Arranca el servidor:

uvicorn main:app --reload

5. Abre la documentación interactiva en:

http://127.0.0.1:8000/docs


## Estructura del proyecto

todo-api/
├── main.py # Rutas de la API (endpoints)
├── models.py # Modelo de datos (tabla Task)
├── schemas.py # Validación de datos de entrada/salida
├── database.py # Configuración de la conexión a la BD
├── requirements.txt # Dependencias del proyecto
└── README.md


## Endpoints

| Método | Ruta              | Descripción                    |
|--------|-------------------|---------------------------------|
| POST   | /tasks            | Crea una tarea nueva            |
| GET    | /tasks            | Lista todas las tareas          |
| GET    | /tasks/{task_id}  | Obtiene una tarea por su id     |
| PUT    | /tasks/{task_id}  | Actualiza una tarea existente   |
| DELETE | /tasks/{task_id}  | Elimina una tarea               |
