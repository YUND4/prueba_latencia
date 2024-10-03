# Etapa de compilación con imagen completa de Python
FROM python:3.9-slim as builder

# Establece el directorio de trabajo
WORKDIR /app

# Instalar compilador y dependencias de postgres
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar requisitos en un directorio aparte para luego copiarlos
RUN pip install --user -r requirements.txt

# Comando para ejecutar el script de entrada
ENTRYPOINT ["/entrypoint.sh"]