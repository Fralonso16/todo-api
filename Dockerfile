# Imagen base: Python 3.12 en su version "slim" (mas ligera que la version completa)
FROM python:3.12-slim

# Carpeta de trabajo DENTRO del contenedor
WORKDIR /app

# Copiamos primero solo requirements.txt (no todo el codigo aun)
# Esto es una optimizacion: si no cambian las dependencias, Docker
# reutiliza esta capa en compilaciones futuras y va mas rapido
COPY requirements.txt .

# Instalamos las dependencias dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# Ahora copiamos el resto del codigo del proyecto
COPY . .

# Documenta que el contenedor escucha en el puerto 8000 (informativo)
EXPOSE 8000

# Comando que se ejecuta cuando arranca el contenedor
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]