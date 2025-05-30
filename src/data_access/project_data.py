import numpy as np
import pandas as pd
import sys
from typing import Optional

# importing custom packages
from src.logger import logging
from src.exception import MyException
from src.configuration.mongodb_connection import MongoDBClient

# importing constants
from src.constants import DATABASE_NAME


class Project_Data:
    """
    In the mongodb_connection.py we are connecting to the database here we further connect it with the collection 
    class to export mongo db records as a pandas dataframe
    """
    
    def __init__(self):
        """
        initializes the mongodb connection
        """
        try:
            self.mongodb_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise(e,sys)
    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        """
        Exports the entire mongo db collection as a pandas dataframe
        
        parameters:
            collection_name:name of mongo collection to export
            database_name:name of database (optional) optional to DATABASE_NAME
            
        return value:
            contains data with removed id column and na values replaced with NaN
        """
        try:
            
            # access the specific collection from database
            if database_name is None:
                collection=self.mongodb_client.database[collection_name]
            else:
                collection=self.mongodb_client[database_name][collection_name]
           
            # convert collection of data into dataframe
        
            print("fetching data from mongodb")
            df=pd.DataFrame(list(collection.find()))
            print("Data fetched with length {}".format(len(df)))
            if "id" in df.columns:
                df=df.drop(columns=["id"],axis=1)
            df.replace({"na":"NaN"},inplace=True)
            
            return df
        except Exception as e:
            raise(e,sys)
         
