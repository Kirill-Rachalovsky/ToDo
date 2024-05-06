FROM python:3.12

RUN mkdir /fastapi_todo
WORKDIR /fastapi_todo

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
