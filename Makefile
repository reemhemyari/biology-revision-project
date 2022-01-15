#Internal vars
VENV_DIR=venv

RMDIR = rmdir /s/q
PYTHON_ACTIVATE = ${VENV_DIR}\Scripts\activate
PYTHON = python

#TARGETS FOR HUMAN INTERACTION
default: deploy

clean:
	@echo "Clean"
	@${RMDIR} ${VENV_DIR}

install-requirements: ${VENV_DIR}

deploy: install-requirements
	@echo "Deploy yo!"
	@${PYTHON_ACTIVATE} && cdk deploy --all

#DIRECTORIES
${VENV_DIR}:
	@${PYTHON} -m venv venv
	@echo "Install requirements"
	@${PYTHON_ACTIVATE} \
	&& pip install -r requirements.txt

#Makefile internals
.NOTPARALLEL:

.PHONY: clean install-requirements deploy
