FROM python:3.9-slim-buster
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./app ./app
WORKDIR app
RUN mkdir -p ./data ./uploads/processed ./uploads/unprocessed ./data/details/file_details ./storage
COPY ./example.categories.txt /app/data/details/config/categories.txt
COPY ./example.types.txt /app/data/details/config/types.txt
ENV PYTHONUNBUFFERED=1
ENV FILES_PATH=/app/uploads
ENV DETAILS_PATH=/app/data/details
ENV STORAGE_PATH=/app/storage
ENV FLASK_PORT=5000
CMD cd web && gunicorn --bind 0.0.0.0:$FLASK_PORT app:app