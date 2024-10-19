VENV = default

all: install run

venv:
	test -d .venv/${VENV} || python -m venv .venv/${VENV}

install: venv
	. .venv/${VENV}/bin/activate && pip install -r requirements.txt

install-cpu: venv
	. .venv/${VENV}/bin/activate && pip install -r requirements-orig-cpu.txt

run:
	export $(xargs <.env)
	. .venv/${VENV}/bin/activate && flask --app chat run --host 0.0.0.0 --port 5000

deploy:
	kubectl create namespace demo || true
	kubectl apply -f iac/k8s/
	kubectl apply -f iac/argocd/

clean:
	rm -rf .venv/${VENV}
	find -iname "*.pyc" -delete
