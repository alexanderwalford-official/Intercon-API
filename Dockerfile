FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY key.pem cert.pem /code/

EXPOSE 4139

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4139", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]
