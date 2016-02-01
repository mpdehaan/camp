deps:
	pip3 --install -r requirements.text

test:
	PYTHONPATH=. py.test tests/*

