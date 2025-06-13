import os
from datetime import date
from dotenv import load_dotenv
load_dotenv()
# for mongo db connections

MONGODB_URI_KEY=os.getenv("MONGODB_URL")
DATABASE_NAME="vehicle_data"
COLLECTION_NAME="vehicle_indurance_info"

#vehicle_data.vehicle_indurance_info


PIPELINE_NAME:str=""
ARTIFACT_DIR:str="artifact" # artifact dir file name

MODEL_FILE_NAME="model.pkl" # model saving file name
PREPROCESSING_FILE_NAME="preprocessing.pkl" # saving our preprocessor (data transformation model)

TARGET_COLUMN="Response" # target column of data
CURRENT_YEAR=date.today().year

FILE_NAME:str="data.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"
SCHEMA_FILE_PATH:str=os.path.join("config","schema.yaml")

"""
Data Ingestion related constant 
"""
DATA_INGESTION_COLLECTION_NAME: str = "vehicle_indurance_info"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.25

"""
Data Validation related Constants
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME: str = "report.yaml"

"""
Data Transformation related constants
"""
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="tansformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"

"""
Model Trainer Related Constants
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")

MODEL_TRAINER_N_ESTIMATORS=200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101

"""
Model Evaluation related constants
"""
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE:float=0.02
MODEL_BUCKET_NAME="myfirstmlopsproject"
MODEL_PUSHER_S3_KEY="model-registry"

"""
Amazon aws connection keys
"""
AWS_ACCESS_KEY_ID_ENV_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ENV_KEY =os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME =os.getenv("AWS_DEFAULT_REGION")

APP_HOST="0.0.0.0"
APP_PORT=5000

