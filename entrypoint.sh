#!/bin/bash
set -e

echo "⏳ Waiting for database to be ready..."

until nc -z db 5432; do
  echo "🕓 Database not ready yet, waiting 2 seconds..."
  sleep 2
done

echo "✅ Database is ready!"

echo "🚀 Running Alembic migrations..."
if alembic -c /app/alembic.ini upgrade head; then
  echo "✅ Alembic migrations completed successfully!"
else
  echo "⚠️  Alembic migration failed. Continuing anyway..."
fi

echo "✅ Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
