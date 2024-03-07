#!/bin/bash
gunicorn --bind 0.0.0.0:8000 exceltohtml.wsgi --reload --workers=3 --timeout=300