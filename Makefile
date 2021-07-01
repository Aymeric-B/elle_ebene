# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* elle_ebene/*.py

black:
	@black scripts/* elle_ebene/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr elle_ebene-*.dist-info
	@rm -fr elle_ebene.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)

# ----------------------------------
#      TEST API
# ----------------------------------
JOB_NAME=<JOB_NAME>
BUCKET_NAME=<BUCKET_NAME>
BUCKET_TRAINING_FOLDER=<BUCKET_TRAINING_FOLDER>
PACKAGE_NAME=elle_ebene
FILENAME=trainer
GCR_REGION=europe-west1
GCP_PROJECT_ID=elle-ebene-project
DOCKER_IMAGE_NAME=elle_ebene_docker

run_locally:
	@python -m elle_ebene.trainer

gcp_submit_training:
	gcloud ai-platform jobs submit training ${JOB_NAME} \
		--job-dir gs://${BUCKET_NAME}/${BUCKET_TRAINING_FOLDER} \
		--package-path ${PACKAGE_NAME} \
		--module-name ${PACKAGE_NAME}.${FILENAME} \
		--python-version=${PYTHON_VERSION} \
		--runtime-version=${RUNTIME_VERSION} \
		--region europe-west1 \
		--stream-logs

run_streamlit:
	streamlit run Website/app.py

build_docker_local:
	docker build -t $(DOCKER_IMAGE_NAME) .

run_docker_local:
	open http://localhost:8501/
	docker run -p 8501:8501 $(DOCKER_IMAGE_NAME)

docker_gcp:
	docker build -t GCR_REGION/GCP_PROJECT_ID/DOCKER_IMAGE_NAME .
	docker push GCR_REGION/GCP_PROJECT_ID/DOCKER_IMAGE_NAME

