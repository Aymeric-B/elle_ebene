FROM python:3.8.6-buster

COPY Website /Website
COPY elle_ebene /elle_ebene
COPY model_weights /model_weights
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD streamlit run Website/app.py --server.port $PORT