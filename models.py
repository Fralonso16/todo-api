# Importamos los tipos de columna que vamos a usar en la tabla
from sqlalchemy import Column, Integer, String, Boolean
# Importamos Base, la clase que creamos en database.py
from database import Base

# Esta clase representa la tabla "tasks" en la base de datos
# Cada instancia de esta clase = una fila de la tabla = una tarea
class Task(Base):
    __tablename__ = "tasks"  # nombre real de la tabla en la base de datos

    # Columna id: número único que identifica cada tarea (clave primaria)
    id = Column(Integer, primary_key=True, index=True)

    # Columna title: el texto de la tarea, obligatorio
    title = Column(String, nullable=False)

    # Columna description: texto opcional con más detalles de la tarea
    description = Column(String, nullable=True)

    # Columna completed: True o False, indica si la tarea está hecha
    # Por defecto, toda tarea nueva empieza como no completada (False)
    completed = Column(Boolean, default=False)