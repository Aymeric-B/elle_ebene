# ----------------------------------
#          INSTALL & TEST
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr elle_ebene-*.dist-info
	@rm -fr elle_ebene.egg-info

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

# ----------------------------------
#      PARAMETRAGE GCP
# ----------------------------------

set_project:
	@gcloud config set project ${PROJECT_ID}

create_bucket:
	@gsutil mb -l ${GCR_REGION} -p ${PROJECT_ID} gs://${BUCKET_NAME}

# ----------------------------------
#      WEBSITE EN DIRECT
# ----------------------------------

run_streamlit:
	streamlit run Website/app.py

# ----------------------------------
#      WEBSITE SUR DOCKER LOCAL
# ----------------------------------

build_docker_local:
	docker build -t $(DOCKER_IMAGE_NAME) .

run_docker_local:
	open http://localhost:8501/
	docker run -p 8501:8501 -e PORT=8501 $(DOCKER_IMAGE_NAME)

# ----------------------------------
#      WEBSITE SUR DOCKER GCP
# ----------------------------------

build_docker_gcp:
	docker build -t $(GCR_MULTI_REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME) .

push_docker_gcp:	
	docker push $(GCR_MULTI_REGION)/$(PROJECT_ID)/$(DOCKER_IMAGE_NAME)

deploy_docker_gcp:
	gcloud run deploy ${GCP_INSTANCE_NAME} --image ${GCR_MULTI_REGION}/${PROJECT_ID}/${DOCKER_IMAGE_NAME} \
		--allow-unauthenticated --platform managed --region ${GCR_REGION} --memory ${SIZE}

stop_docker_gcp:
	gcloud run services delete ${GCP_INSTANCE_NAME} --region ${GCR_REGION} --async
