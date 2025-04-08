cd src

# export $(grep -v '^#' .env | xargs)

uv run alembic revision --autogenerate

uv run alembic upgrade head

uv run gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000