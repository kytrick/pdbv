# Here's the deal: just type "make" compiles your requirements files.  
#				   it doesn't add or remove with pip.
#
# typing "make dev" gives you your development/testing libraries
# typing "make prod" deletes the dev things that aren't in prod (make sure you're in your virtual env!)
#
# if you want to add a new library, add it to requirements.in or dev-requirements.in or both
#
# people usually use pip-freeze, but I wanted to track dev and prod requirements separately
# (i don't need ipython in production for example) https://github.com/nvie/pip-tools
# http://nvie.com/posts/better-package-management/
# I wanted an easy way to switch back and forth.  pip-tools lets you maintain separate environs.
#
# .PHONY indicates that there isn't an actual filename for that target
# format:  <target> : <recipe> 
#
#  pip-sync will install all required packages into your env, but will additionally 
#  uninstall everything else in there. Dangerous to use outside of your virtualenv


.PHONY: all
all: pip-compile requirements bower 

.PHONY: pip-compile
pip-compile:
	@pip-compile --help > /dev/null 2>&1 || (pip install --upgrade pip && pip install pip-tools)

.PHONY: bower
bower: npm
	@which bower > /dev/null 2>&1 || npm install -g bower
	@bower install

.PHONY: npm
npm:
	@npm --version > /dev/null 2>&1 || brew install npm 

.PHONY: prod
prod: all
	pip-sync requirements.txt

.PHONY: dev
dev: all
	pip-sync dev-requirements.txt

.PHONY: requirements
requirements: requirements.txt dev-requirements.txt

requirements.txt: requirements.in
	pip-compile requirements.in

dev-requirements.txt: dev-requirements.in requirements.in
	pip-compile dev-requirements.in