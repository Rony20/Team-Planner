#!/bin/sh

# start the gunicorn server with uvicorn worker on port 8000
echo "Starting gunicorn server..."
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 app.main:app 