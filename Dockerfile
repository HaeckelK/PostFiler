FROM python:3.9-slim-buster
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR app
RUN mkdir ./data
RUN mkdir -p ./uploads/processed
RUN mkdir -p ./uploads/unprocessed
RUN mkdir -p ./data/details/file_details
RUN mkdir ./storage
COPY ./web ./web
COPY ./core.py .
COPY ./interfaces.py .
COPY ./processes.py .
COPY ./utils.py .
COPY ./categories.txt /app/data/details/config/
COPY ./types.txt /app/data/details/config/
CMD cd web && gunicorn --bind 0.0.0.0:$FLASK_PORT app:app