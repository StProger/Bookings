#!/bin/bash

alembic upgrade head

guinicorn main:app --workers 4 --workers-class uvicorn.workers.UvicornWorkers --bind=0.0.0.0:8000