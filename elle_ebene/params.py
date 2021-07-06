#params.py
#Fichier  de paramètres

# Pre-processing parameters
RESIZING_DIM =  500
COLOR_BACKGROUND = [255,255,255] #white
VALID_IMAGES = [".jpg",".jpeg",".png"]

# Model predict parameters
MODEL_USED = "seg_aug"

# Experiment name for MLFolow system
EXPERIMENT_NAME = "[FR] [Lyon] [myr-aym-lou] elle_ebene_baseline V0"
MLFLOW_URI = "https://mlflow.lewagon.co/"

# GCP parameters
BUCKET_NAME = "elle_ebene_bucket"
MODEL_NAME = "Baseline"
MODEL_VERSION = "V0"
