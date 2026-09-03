# TestClient simula peticiones HTTP a tu API sin necesidad de arrancar
# un servidor real - hace las pruebas mucho mas rapidas
from fastapi.testclient import TestClient
from main import app

# Creamos un "cliente" que apunta directamente a tu aplicacion FastAPI
client = TestClient(app)


def test_crear_tarea():
    """Comprueba que se puede crear una tarea correctamente."""
    response = client.post(
        "/tasks",
        json={"title": "Tarea de test", "description": "Creada por pytest", "completed": False},
    )
    # Verificamos el codigo de estado
    assert response.status_code == 200
    # Verificamos que la respuesta contiene los datos esperados
    data = response.json()
    assert data["title"] == "Tarea de test"
    assert data["completed"] is False
    # Verificamos que la BD le asigno un id (osea, que se guardo de verdad)
    assert "id" in data


def test_listar_tareas():
    """Comprueba que listar tareas devuelve una lista (no un error)."""
    response = client.get("/tasks")
    assert response.status_code == 200
    # Verificamos que la respuesta es una lista, aunque este vacia
    assert isinstance(response.json(), list)


def test_obtener_tarea_inexistente():
    """Comprueba que pedir una tarea que no existe da 404, no un error interno."""
    response = client.get("/tasks/99999")
    assert response.status_code == 404


def test_actualizar_tarea():
    """Comprueba que se puede actualizar una tarea existente."""
    # Primero creamos una tarea para poder actualizarla despues
    crear = client.post(
        "/tasks",
        json={"title": "Tarea a actualizar", "description": "Original", "completed": False},
    )
    tarea_id = crear.json()["id"]

    # Ahora la actualizamos, marcandola como completada
    response = client.put(f"/tasks/{tarea_id}", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["completed"] is True
    # El titulo no deberia haber cambiado, porque no lo enviamos en el update
    assert response.json()["title"] == "Tarea a actualizar"


def test_eliminar_tarea():
    """Comprueba que se puede eliminar una tarea y que despues ya no existe."""
    # Creamos una tarea para eliminarla despues
    crear = client.post(
        "/tasks",
        json={"title": "Tarea a eliminar", "description": "Temporal", "completed": False},
    )
    tarea_id = crear.json()["id"]

    # La eliminamos
    response = client.delete(f"/tasks/{tarea_id}")
    assert response.status_code == 200

    # Verificamos que ya no se puede encontrar (debe dar 404)
    response = client.get(f"/tasks/{tarea_id}")
    assert response.status_code == 404