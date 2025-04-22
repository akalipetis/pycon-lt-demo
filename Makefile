LOAD_HOST = http://localhost:8000/
LOAD_CONCURRENCY = 10
LOAD_DURATION = 5s
PORT = 8000

gunicorn:
	uv run gunicorn -w 4 pyconlt:app --port=$(PORT)

uvicorn:
	uv run uvicorn pyconlt:app.asgi --interface asgi3 --port "$(PORT)"

migrate:
	uv run nanodjango migrate

collectstatic:
	uv run nanodjango collectstatic

dev:
	uv run nanodjango run pyconlt.py

loadtest:
	echo "GET $(LOAD_HOST)api/" | vegeta attack -duration=$(LOAD_DURATION) -max-workers=$(LOAD_CONCURRENCY) | tee report.bin | vegeta report