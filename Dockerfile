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

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]