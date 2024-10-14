VENV = default

all: venv install run

venv:
	test -d .venv/${VENV} || python -m venv .venv/${VENV}

install:
	. .venv/${VENV}/bin/activate && pip install -r requirements.txt

run:
	export $(xargs <.env)
	. .venv/${VENV}/bin/activate && flask --app chat run --host 0.0.0.0 --port 5000

clean:
	rm -rf .venv/${VENV}
	find -iname "*.pyc" -delete
