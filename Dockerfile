FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install . --no-cache-dir
COPY . .
ENV PYTHONPATH=/app/src