import sys
import os

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact

from src.data_access.project_data import Project_Data

from src.logger import logging
from src.exception import MyException


class DataIngestion:
   
    # creating the object of DataIngestionConfig and passing it in constructor
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        """
        parameter data ingestion config to load all configurations"""
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise MyException(e,sys) from e 
        
    # component to export dataframe as pandas DataFrame in feature store file path
    def export_data_into_feature_store(self)->DataFrame:
        """
        Method Name :   export_data_into_feature_store
        Description :   This method exports data from mongodb to csv file
        
        Output      :   data is returned as artifact of data ingestion components
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Exporting data  from mongo db")
            
            my_data=Project_Data() 
            dataframe=my_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name) # function returns dataframe
            logging.info(f"Data frame size {dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"saving exported data to feature store file path :{feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
   
        except Exception as e:
            raise MyException(e,sys) from e
        
    # component to split data in train test and store it in train file and test file
    
    def split_data_as_train_test(self,dataframe:DataFrame)->None:
        """
        this function split data as train test split 
        """
        logging.info("Initiating the train test split of data ingestion")
        try:
            if dataframe.shape[0]==0:
                raise MyException("Data fetched is empty",sys)
            train_data,test_data=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42)
            logging.info("train test spit completed")
            logging.info("exporting the train and test data in respective files")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_data.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info("Train and test Data exported to train file and test file")
            
        except Exception as e:
            raise MyException(e,sys) from e
        
    
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        """
        method initiate the data ingestion 
        return type is DataIngestionArtifact which store the file path of train and test file of the data"""
        
        logging.info("Entered initiating data ingestion ")
        try:
            dataframe=self.export_data_into_feature_store()
            logging.info(f"dataframe of shape {dataframe.shape} from initiate_data_ingestion from dataingestion component")
            self.split_data_as_train_test(dataframe)
            logging.info("data splitted and saved as train_test")
            
            logging.info("Exited initiate data ingestion")
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                          test_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"Data ingestion artifact :==>> {data_ingestion_artifact}")
            
            return data_ingestion_artifact
    
        except Exception as e:
            raise MyException (e,sys) from e
            
            
result=DataIngestion(data_ingestion_config=DataIngestionConfig())
result.initiate_data_ingestion()