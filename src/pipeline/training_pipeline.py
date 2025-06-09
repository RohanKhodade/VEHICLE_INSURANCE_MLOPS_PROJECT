import sys
import os

from src.logger import logging
from src.exception import MyException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

from src.entity.config_entity import (DataIngestionConfig,
                                      DataValidationConfig,
                                      DataTransformationConfig,
                                      ModelTrainerConfig,
                                     )
from src.entity.artifact_entity import (DataIngestionArtifact,
                                        DataValidationArtifact,
                                        DataTransformationArtifact,
                                        ModelTrainerArtifact,
                                       )

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()
        self.data_validation_config=DataValidationConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_trainer_config=ModelTrainerConfig()
        #self.model_evaluation_config=ModelEvaluationConfig()
        #self.model_pusher_config=ModelPusherConfig()

    
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
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        logging.info("Entered data validation artifact of training pipeline")
        
        try:
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                           data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info("preformed the data validation ")
            logging.info("Exited the data validation of training pipeline")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        """
        responsible for starting data transformations component
        """
        try:
            data_transformation=DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                   data_transformation_config=self.data_transformation_config,
                                                   data_validation_artifact=data_validation_artifact
                                                   )
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e,sys) from e
        
    def start_model_trainer(self,data_transformation_artifact:DataIngestionArtifact)->ModelTrainerArtifact:
        """
        responsible for starting model training
        """
        try:
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                       model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys) from e
    def run_pipeline(self,)->None:
        """
        this function is responsible for rrunnig complete pipline
        """
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
        except Exception as e:
            raise MyException (e,sys) from e