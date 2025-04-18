#!/bin/bash
echo "Starting application..."
gunicorn --worker-class gevent --bind 0.0.0.0:$PORT --log-level debug --access-logfile - --error-logfile - app:app 