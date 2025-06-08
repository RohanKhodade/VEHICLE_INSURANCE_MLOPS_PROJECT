import os
from datetime import date
from dotenv import load_dotenv
load_dotenv()
# for mongo db connections

MONGODB_URI_KEY=os.getenv("MONGO_URI")
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