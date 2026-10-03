FROM python:3.10-slim


WORKDIR /code

# Copy the requirements file that exists in this folder
COPY app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app/ /code/
COPY data_services/ /data_services/

EXPOSE 8000