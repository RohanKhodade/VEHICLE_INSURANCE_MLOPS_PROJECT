import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging

from src.constants import MONGODB_URI_KEY,DATABASE_NAME

ca=certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.

    Attributes:
    ----------
    client : MongoClient
        A shared MongoClient instance for the class.
    database : Database
        The specific database instance that MongoDBClient connects to.

    Methods:
    -------
    __init__(database_name: str) -> None
        Initializes the MongoDB connection using the given database name.
    """
    
    client=None
    
    def __init__(self,database_name:str=DATABASE_NAME)->None:
        """
        Initializes a connection to the MongoDB database. If no existing connection is found, it establishes a new one.

        Parameters:
        ----------
        database_name : str, optional
            Name of the MongoDB database to connect to. Default is set by DATABASE_NAME constant.

        Raises:
        ------
        MyException
            If there is an issue connecting to MongoDB or if the environment variable for the MongoDB URL is not set.
        """
        
        try:
            #check is mongo client is none if it is none then create a new connection else dont make any new connection
            if MongoDBClient.client is None:
                logging.info("Connecting to mongo db")
                mongo_db_url=MONGODB_URI_KEY
                if mongo_db_url is None:
                    raise Exception("mongo db url not set : ",mongo_db_url)
                
                # else establish a mongo connection
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCaFILE=ca)
                
            # use the share mongodb client for this instance
            self.client=MongoDBClient.client
            self.database=self.client[database_name] # connect to the specified database
            self.database_name=database_name
            
            logging.info("Mongo db connection successfull")
            
        except Exception as e:
            raise(e,sys) # raise the error 
                