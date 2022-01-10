
clean:
	rm src/*.pyc
run:
	python src/main.py
test:
	pytest --verbose
setup:
	pip install -r requirements.txt
