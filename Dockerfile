FROM python:3.8.6-buster

COPY api /hairapi
COPY elle_ebene /elle_ebene
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT