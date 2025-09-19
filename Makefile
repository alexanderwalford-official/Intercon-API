make:
	fastapi dev main.py

tables:
	python3 .\create_tables.py

deploy:
	sudo docker-compose up -d --build