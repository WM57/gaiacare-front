FROM python:3.8.6-buster

COPY api /api
COPY gaiacare-front /gaiacare-front
COPY requirements.txt /requirements.txt
COPY /Users/admin/code/CyrilWarde/gcp/warm-skill-328010-28916c87c4b4.json /credentials.json

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
