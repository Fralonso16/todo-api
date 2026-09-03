// URL base de la API
const API_URL = "http://127.0.0.1:8000";

// Referencias a elementos del HTML
const tasksList = document.getElementById("tasks-list");
const newTaskInput = document.getElementById("new-task-title");
const addTaskBtn = document.getElementById("add-task-btn");
const taskCount = document.getElementById("task-count");
const emptyMessage = document.getElementById("empty-message");
const filterButtons = document.querySelectorAll(".filter-btn");

// Filtro actualmente activo: "all", "pending" o "completed"
let currentFilter = "all";

// Cargamos las tareas en cuanto se abre la pagina
window.addEventListener("DOMContentLoaded", cargarTareas);


// --- Cargar y mostrar las tareas ---
async function cargarTareas() {
    const response = await fetch(`${API_URL}/tasks`);
    const tareas = await response.json();

    // Aplicamos el filtro activo antes de mostrar
    const tareasFiltradas = tareas.filter((tarea) => {
        if (currentFilter === "pending") return !tarea.completed;
        if (currentFilter === "completed") return tarea.completed;
        return true; // "all"
    });

    renderizarTareas(tareasFiltradas);

    // Actualizamos el contador con el total real, no el filtrado
    taskCount.textContent = `${tareas.length} tarea${tareas.length !== 1 ? "s" : ""}`;

    // Mostramos el mensaje de "vacio" si no hay nada que mostrar tras filtrar
    emptyMessage.style.display = tareasFiltradas.length === 0 ? "block" : "none";
}


// --- Pintar la lista de tareas en el HTML ---
function renderizarTareas(tareas) {
    tasksList.innerHTML = "";

    tareas.forEach((tarea) => {
        const li = document.createElement("li");
        li.className = "task-item" + (tarea.completed ? " completed" : "");

        // Checkbox para marcar como completada/pendiente
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = tarea.completed;
        checkbox.addEventListener("change", () => cambiarEstado(tarea.id, checkbox.checked));

        // Texto del titulo
        const span = document.createElement("span");
        span.className = "task-title";
        span.textContent = tarea.title;

        // Boton de eliminar
        const deleteBtn = document.createElement("button");
        deleteBtn.className = "delete-btn";
        deleteBtn.textContent = "✕";
        deleteBtn.addEventListener("click", () => eliminarTarea(tarea.id));

        li.appendChild(checkbox);
        li.appendChild(span);
        li.appendChild(deleteBtn);
        tasksList.appendChild(li);
    });
}


// --- Crear una tarea nueva ---
addTaskBtn.addEventListener("click", async () => {
    const title = newTaskInput.value.trim();
    if (!title) return;

    await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description: "", completed: false }),
    });

    newTaskInput.value = "";
    cargarTareas();
});

// Tambien permitimos crear la tarea pulsando Enter, no solo con el boton
newTaskInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") addTaskBtn.click();
});


// --- Cambiar el estado completado/pendiente ---
async function cambiarEstado(id, completed) {
    await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ completed }),
    });
    cargarTareas();
}


// --- Eliminar una tarea ---
async function eliminarTarea(id) {
    await fetch(`${API_URL}/tasks/${id}`, { method: "DELETE" });
    cargarTareas();
}


// --- Manejar los botones de filtro ---
filterButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
        // Quitamos "active" de todos y lo ponemos solo en el pulsado
        filterButtons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");

        currentFilter = btn.dataset.filter;
        cargarTareas();
    });
});