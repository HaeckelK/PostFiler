FROM python:3.9-slim-buster
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR app
RUN mkdir ./data
COPY ./web ./web
COPY ./core.py .
COPY ./interfaces.py .
COPY ./processes.py .
COPY ./utils.py .
# CMD gunicorn "app:create_app()" --bind 0.0.0.0:$PORT
CMD cd web && flask run --port=$FLASK_PORT