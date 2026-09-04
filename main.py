# FastAPI: el framework que crea la API
# Depends: permite "inyectar" dependencias (como la sesión de BD) en cada ruta
# HTTPException: para devolver errores controlados (ej. tarea no encontrada)
from fastapi import FastAPI, Depends, HTTPException
# Session: el tipo de dato de una sesión de base de datos
from sqlalchemy.orm import Session
# Importamos lo que creamos en los otros archivos
from database import Base, engine, SessionLocal
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskOut

# Esto crea físicamente las tablas en la base de datos (el archivo tasks.db)
# a partir de lo que definimos en models.py. Si el archivo ya existe, no
# vuelve a crear las tablas que ya estén (es seguro ejecutarlo varias veces)
Base.metadata.create_all(bind=engine)

# Creamos la aplicación FastAPI, con un título que aparecerá en la documentación
app = FastAPI(title="To-Do API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://todo-api-frontend-7hu4.onrender.com",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Esta función abre una sesión de base de datos, la "presta" a la ruta que
# la necesite, y se asegura de cerrarla después (pase lo que pase)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Endpoint: crear una tarea nueva ---
# POST /tasks recibe los datos definidos en TaskCreate y devuelve TaskOut
@app.post("/tasks", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Creamos el objeto Task (modelo de BD) a partir de los datos recibidos
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
    )
    db.add(db_task)      # lo añadimos a la sesión
    db.commit()           # guardamos los cambios de verdad en la BD
    db.refresh(db_task)   # recargamos db_task para traer el id generado
    return db_task


# --- Endpoint: listar todas las tareas ---
@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


# --- Endpoint: obtener una tarea concreta por su id ---
@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        # Si no existe, devolvemos error 404 (no encontrado) con un mensaje claro
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


# --- Endpoint: actualizar una tarea existente ---
@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # exclude_unset=True: solo tenemos en cuenta los campos que el usuario
    # realmente envió, no todos los que trae el schema por defecto
    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task


# --- Endpoint: borrar una tarea ---
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(db_task)
    db.commit()
    return {"detail": "Tarea eliminada correctamente"}