FROM python:3.12-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY db/ ./db/
COPY migrations/ ./migrations/
COPY alembic.ini .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD alembic upgrade head && cd api && uvicorn main:app --host 0.0.0.0 --port 8000
