FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt
COPY ./.flake8 /.flake8
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN pip install -r /code/requirements.txt

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
