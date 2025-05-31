import sys
from dataclasses import dataclass
from datetime import datetime
import os
from src.constants import *

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


# settings of pipeline
@dataclass
class TrainingPipelineConfig:
    pipeline_name:str=PIPELINE_NAME # name of pipeline
    artifact_dir:str=os.path.join(ARTIFACT_DIR,TIMESTAMP) # save the output of pipeline components in artifact dir
    timestamp:str=TIMESTAMP  # give artifact the unique Timestamp
    
training_pipeline_config:TrainingPipelineConfig=TrainingPipelineConfig()
    

# this class holds all the configuration needed for data ingestion component
@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
    training_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    testing_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name:str=DATA_INGESTION_COLLECTION_NAME
    
# this class holds data validation configuration
