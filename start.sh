#!/bin/bash
cd /home/yaozl/webTools
pip install -r requirements.txt -q
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
