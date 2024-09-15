FROM python:3.10-slim

COPY scoring/src/ /code
COPY ./scoring/requirements.txt /code/requirements.txt
COPY common/ /code/common
WORKDIR /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENV PYTHONPATH=/code
EXPOSE 8003