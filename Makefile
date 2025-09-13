make:
	fastapi dev main.py

tables:
	python3 .\create_tables.py

build:
	docker build .