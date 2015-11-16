all: pip-compile requirements

virtualenv: .python-version

.python-version:
	pyenv virtualenv 2.7.10 pdbv
	pyenv local pdbv
	pip install -r dev-requirements.txt

pip-compile:
	@which pip-compile > /dev/null || pip install pip-tools

requirements: requirements.txt dev-requirements.txt

requirements.txt: requirements.in
	pip-compile requirements.in

dev-requirements.txt: dev-requirements.in requirements.in
	pip-compile dev-requirements.in

prod:
	pip-sync requirements.txt

dev:
	pip-sync dev-requirements.txt
