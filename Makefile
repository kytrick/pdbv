all: pip

pip: requirements.txt dev-requirements.txt

requirements.txt: requirements.in
	pip-compile requirements.in

dev-requirements.txt: dev-requirements.in
	pip-compile dev-requirements.in

prod:
	pip-sync requirements.txt

dev:
	pip-sync dev-requirements.txt
