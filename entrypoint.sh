#!/bin/sh
set -e

echo "⏳ Waiting for database to be fully ready..."
until pg_isready -h db -p 5432 -U ${POSTGRES_USER:-shop_user}; do
  echo "🕓 Database not ready yet, waiting 2 seconds..."
  sleep 2
done

echo "✅ Database is ready!"
sleep 2

echo "🚀 Running Alembic migrations..."
if alembic -c /app/alembic.ini upgrade head; then
  echo "✅ Alembic migrations completed successfully!"
else
  echo "⚠️ Alembic migration failed. Continuing anyway..."
fi

echo "✅ Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
