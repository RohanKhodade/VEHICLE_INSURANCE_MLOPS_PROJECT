import sys
import os

from src.logger import logging
from src.exception import MyException

from src.components.data_ingestion import DataIngestion

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        """
        this is responsible for starting data ingestion component
        """
        try:
            logging.info("starting data ingestion from training pipeline")
            logging.info("pulling data from mongodb")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("data saved as train and test in train file and test file")
            logging.info("Training Pileline --> Data ingestion completed")
            return data_ingestion_artifact
        
        except Exception as e:
            raise MyException (e,sys) from e
    
    
    
    def run_pipeline(self,)->None:
        """
        this function is responsible for rrunnig complete pipline
        """
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            
        except Exception as e:
            raise MyException (e,sys) from e