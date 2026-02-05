FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY cdc_replication.py .

RUN pip install --no-cache-dir mysql-connector-python psycopg2-binary

CMD ["python", "cdc_replication.py"]
