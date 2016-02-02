deps:
	pip3 install -r requirements.txt

test:
	PYTHONPATH=. py.test tests/*

