# Here's the deal: just type "make" compiles your requirements files.  
#				   it doesn't add or remove with pip.
#
# typing "make dev" gives you your development/testing libraries
# typing "make prod" deletes the dev things that aren't in prod (make sure you're in your virtual env!)
#
# if you want to add a new library, add it to requirements.in or dev-requirements.in or both

all: pip-compile requirements

.PHONY: pip-compile
pip-compile:
	@which pip-compile > /dev/null || pip install pip-tools

.PHONY: prod
prod:
	pip-sync requirements.txt

.PHONY: dev
dev:
	pip-sync dev-requirements.txt

.PHONY: requirements
requirements: requirements.txt dev-requirements.txt

requirements.txt: requirements.in
	pip-compile requirements.in

dev-requirements.txt: dev-requirements.in requirements.in
	pip-compile dev-requirements.in

