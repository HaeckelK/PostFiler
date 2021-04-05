FROM python:3.9-slim-buster
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR app
RUN mkdir -p ./data ./uploads/processed ./uploads/unprocessed ./data/details/file_details ./storage
COPY ./web ./web
COPY ./core.py .
COPY ./interfaces.py .
COPY ./processes.py .
COPY ./utils.py .
COPY ./example.categories.txt /app/data/details/config/categories.txt
COPY ./example.types.txt /app/data/details/config/types.txt
ENV PYTHONUNBUFFERED=1
CMD cd web && gunicorn --bind 0.0.0.0:$FLASK_PORT app:app