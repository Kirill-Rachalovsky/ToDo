FROM python:3.12

RUN mkdir /fastapi_todo
WORKDIR /fastapi_todo

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install SQLAlchemy==2.0.23

COPY . .

CMD uvicorn todo_app.main:app --host '0.0.0.0' --port 8000
