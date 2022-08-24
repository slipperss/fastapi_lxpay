#/bin/sh

aerich upgrade
uvicorn main:app --host 0.0.0.0 --port $PORT