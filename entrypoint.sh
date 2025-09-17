#!/bin/sh
# Start sqlite_web in the background
sqlite_web mainframe.db --host 0.0.0.0 --port 8080 &

# Run uvicorn in the foreground (keeps container alive)
uvicorn main:app --host 0.0.0.0 --port 443 \
  --ssl-keyfile key.pem --ssl-certfile cert.pem