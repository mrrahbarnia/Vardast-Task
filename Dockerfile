FROM python:3.11-slim-bullseye

RUN apt-get update && \
    apt-get install -y git curl

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get purge -y --auto-remove git && \
    rm -rf /var/lib/apt/lists/*

COPY ./src ./src


ENTRYPOINT ["python", "./src/__main__.py"]
