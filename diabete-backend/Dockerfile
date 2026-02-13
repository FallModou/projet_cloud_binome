# =========================
# STAGE 1 : Build
# =========================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /install

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip  \
    &&  pip install --prefix=/install -r requirements.txt


# =========================
# STAGE 2 : Runtime
# =========================
FROM python:3.11-slim

WORKDIR /app

# Copier uniquement les dépendances nécessaires
COPY --from=builder /install /usr/local

# Copier le code
COPY app.py .
COPY model ./model

EXPOSE 8000

# Healthcheck demandé
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
 CMD curl -f http://localhost:8000/health || exit 1

# Lancer FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
