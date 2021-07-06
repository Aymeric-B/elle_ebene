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
#      PARAMETRES
# ----------------------------------
JOB_NAME=<JOB_NAME>
BUCKET_TRAINING_FOLDER=<BUCKET_TRAINING_FOLDER>
PACKAGE_NAME=elle_ebene
FILENAME=trainer

GCR_MULTI_REGION=eu.gcr.io
GCR_REGION=europe-west1
GCE_ZONE=europe-west1-b
SIZE=1024Mi

PROJECT_ID=elle-ebene-project-318513
BUCKET_NAME=elle_ebene_bucket
DOCKER_IMAGE_NAME=elle_ebene_docker
GCP_INSTANCE_NAME=elleebenedocker


run_locally:
	@python -m elle_ebene.trainer

run_streamlit:
	streamlit run Website/app.py

build_docker_local:
	docker build -t $(DOCKER_IMAGE_NAME) .

run_docker_local:
	open http://localhost:8501/
	docker run -p 8501:8501 -e PORT=8501 $(DOCKER_IMAGE_NAME)

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${GCR_REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

build_docker_gcp:
	docker build -t $(GCR_MULTI_REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME) .

push_docker_gcp:	
	docker push $(GCR_MULTI_REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME)

deploy_docker_gcp:
	gcloud run deploy ${GCP_INSTANCE_NAME} --image ${GCR_MULTI_REGION}/${PROJECT_ID}/${DOCKER_IMAGE_NAME} \
		--allow-unauthenticated --platform managed --region ${GCR_REGION} --memory ${SIZE}

stop_docker_gcp:
	gcloud run services delete ${GCP_INSTANCE_NAME} --region ${GCR_REGION} --async
