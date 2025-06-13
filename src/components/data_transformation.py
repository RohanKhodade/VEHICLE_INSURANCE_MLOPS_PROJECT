import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.compose import ColumnTransformer

from src.constants import TARGET_COLUMN,SCHEMA_FILE_PATH,CURRENT_YEAR
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact,DataIngestionArtifact,DataValidationArtifact
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import save_object,save_numpy_array_data,read_yaml_file

class DataTransformation:
    
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
            self._schema_config=read_yaml_file(filepath=SCHEMA_FILE_PATH)

        except Exception as e:
            raise MyException (e,sys) from e
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise MyException(e,sys) from e
        
    def get_transformer_object(self)->Pipeline:
        logging.info("entered get data transformer object method of data transformation class")
        
        try:
            #Initialize the transformers
            numeric_transformer=StandardScaler()
            min_max_scaler=MinMaxScaler()
            logging.info("transformers initialized :Standard Scaler and MinMax Scaler")
            
            #Load Schema Configuration
            num_features=self._schema_config["num_features"]
            mm_columns=self._schema_config["mm_columns"]
            logging.info("columns loaded from schema")
            
            # creating  preprocesser pipeline
            preprocessor=ColumnTransformer(
                transformers=[
                    ("StandardScaler",numeric_transformer,num_features),
                    ("MinMaxScaler",min_max_scaler,mm_columns)
                ],
                remainder="passthrough" # leaves other columns untouched
            )
            # wrapping everything in a single pipeline
            final_pipeline=Pipeline(steps=[("Preprocessor",preprocessor)])
            logging.info("Final Pipeline ready")
            logging.info("Exited get data transformer object method of data transformation class")
            return final_pipeline
        except Exception as e:
            logging.info("exception in get_data_transformer object of data transformation object")
            raise MyException(e,sys) from e
        
    def map_gender_column(self,df):
        logging.info("Mapping gender column to binary values")
        df["Gender"]=df["Gender"].map({"Male":1,"Female":0}).astype(int)
        return df
    
    def create_dummy_columns(self,df):
        logging.info("Creating dummy variables for categorical features")
        df=pd.get_dummies(df,drop_first=True)
        return df
    
    def rename_columns(self,df):
        logging.info("Renaming specific columns anmd casting to int")
        df=df.rename(columns={
            "Vehicle_Age_< 1 Year":"Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years":"Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year","Vehicle_Age_gt_2_Years","Vehicle_Damage:Yes"]:
            if col in df.columns:
                df[col]=df[col].astype("int")   
        return df
    
    def drop_id_column(self,df):
        logging.info("dropping id columns")
        drop_col=self._schema_config["drop_columns"]
        if drop_col in df.columns:
            df=df.drop(drop_col, axis=1)
        return df
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        """
        Initiates data transformation component for the pipeline
        """
        try:
            logging.info("Data transformation Started")
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)
            
            # load train and test data
            train_df=self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df=self.read_data(file_path=self.data_ingestion_artifact.test_file_path)
            logging.info("Train -test data loaded")
            
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            
            logging.info("Input and target cols defined for both train and test df")
            
            # Apply custom transformations in specified sequence
            
            input_feature_train_df=self.map_gender_column(input_feature_train_df)
            input_feature_train_df=self.drop_id_column(input_feature_train_df)
            input_feature_train_df=self.create_dummy_columns(input_feature_train_df)
            input_feature_train_df=self.rename_columns(input_feature_train_df)
            
            input_feature_test_df=self.map_gender_column(input_feature_test_df)
            input_feature_test_df=self.drop_id_column(input_feature_test_df)
            input_feature_test_df=self.create_dummy_columns(input_feature_test_df)
            input_feature_test_df=self.rename_columns(input_feature_test_df)
            
            # 🔥 Align test columns with train columns to avoid transform errors
            input_feature_test_df = input_feature_test_df.reindex(columns=input_feature_train_df.columns, fill_value=0)
            
            logging.info("Custom transformations applied to train and test data")
            
            logging.info("starting data transformation")
            preprocessor=self.get_transformer_object()
            logging.info("Got the preprocessor object")
            
            logging.info("Initializing transformation for training data")
            input_feature_train_arr=preprocessor.fit_transform(input_feature_train_df)
            logging.info("Initializing transformation for testing data")
            input_feature_test_arr=preprocessor.transform(input_feature_test_df)
            
            logging.info("transformation done end to end to train-test df")
        
            logging.info("Applying SMOTTEN to Handle imbalance dataset ")
            smt=SMOTEENN(sampling_strategy="minority")
            input_feature_train_final,target_feature_train_final=smt.fit_resample(input_feature_train_arr,target_feature_train_df)
            input_feature_test_final,target_feature_test_final=smt.fit_resample(input_feature_test_arr,target_feature_test_df)
            logging.info("Smotten applied to train-test df")
            
            train_arr=np.c_[input_feature_train_final,np.array(target_feature_train_final)]
            test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]
            logging.info("feature target concatination done for train test df")
            
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            
            logging.info("saving transformation object and transformed files")
            
            logging.info("Data transformation completed successfully")
            print("Transformed Training Columns:", input_feature_train_df.columns.tolist())
            print("Transformed Testing Columns:", input_feature_test_df.columns.tolist())
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
                
            )
            
        except Exception as e:
            raise MyException(e,sys) from e