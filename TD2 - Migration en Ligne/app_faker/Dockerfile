FROM python:3.12-slim

WORKDIR /app

# Installation des dépendances système minimales (optionnel mais utile)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier le code dans l'image
COPY faker_traffic.py .

# Installer les dépendances Python
RUN pip install --no-cache-dir Faker mysql-connector-python

CMD ["python", "faker_traffic.py"]
