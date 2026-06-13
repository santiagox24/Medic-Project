FROM python:3.10-slim


WORKDIR /code

# Copy the requirements file that exists in this folder
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8000