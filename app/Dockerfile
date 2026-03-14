FROM python:3.10-slim


WORKDIR /code

# Copy the requirements file that exists in this folder (originally named with a typo)
COPY ./requierments.txt /code/requierments.txt

RUN pip install --no-cache-dir --upgrade -r /code/requierments.txt

COPY . /code/

EXPOSE 8000