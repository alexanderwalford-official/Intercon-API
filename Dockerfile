FROM python:3.9

WORKDIR /app

# copy requirements and environment file
COPY requirements.txt ./
COPY .env ./

# install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy all project files into the container
COPY . .

# expose your port
EXPOSE 443

# start the app with SSL
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]
