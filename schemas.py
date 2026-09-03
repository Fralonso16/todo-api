# BaseModel es la clase base de Pydantic para crear schemas (validadores de datos)
from pydantic import BaseModel
# Optional indica que un campo puede no venir informado
from typing import Optional

# Schema para CREAR una tarea nueva: lo que el usuario debe enviar a la API
class TaskCreate(BaseModel):
    title: str                        # obligatorio
    description: Optional[str] = None # opcional, si no se envía, vale None
    completed: Optional[bool] = False  # opcional, por defecto False

# Schema para ACTUALIZAR una tarea existente: todos los campos son opcionales,
# porque quizá solo quieras cambiar uno (ej. marcarla como completada)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

# Schema para DEVOLVER una tarea al usuario: incluye el id, que la BD genera sola
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    # Esta configuración le dice a Pydantic que puede leer los datos
    # directamente desde un objeto de SQLAlchemy (como los de models.py),
    # no solo desde un diccionario
    model_config = {"from_attributes": True}