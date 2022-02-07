#Internal vars
VENV_DIR=venv
TMP_DIR=.tmp

RMDIR = rmdir /s/q
PYTHON_ACTIVATE = ${VENV_DIR}\Scripts\activate
PYTHON = python

#TARGETS FOR HUMAN INTERACTION
default: deploy

clean:
	@echo "Clean"
	@${RMDIR} ${VENV_DIR}

install-requirements: ${VENV_DIR}

update: $(TMP_DIR)
	@echo "Update lambda"
	@cd lambda/api_lambda/ && tar.exe -a -c -f ../../.tmp/api_lambda.zip *.py
	@echo "fileb://${TMP_DIR}/api_lambda.zip"
	aws lambda update-function-code --function-name BiologyRevisionProjectSta-auroraserverlessdbAA0B4B-QVOK8Plt2izz --zip-file fileb://${TMP_DIR}/api_lambda.zip

deploy: install-requirements
	@echo "Deploy"
	@${PYTHON_ACTIVATE} && cdk deploy --all

#DIRECTORIES
${VENV_DIR}:
	@${PYTHON} -m venv venv
	@echo "Install requirements"
	@${PYTHON_ACTIVATE} \
	&& pip install -r requirements.txt


${TMP_DIR}:
	@mkdir $@

#Makefile internals
.NOTPARALLEL:

.PHONY: clean install-requirements deploy
