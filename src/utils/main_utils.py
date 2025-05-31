import os
import sys
import numpy as np
from pandas import DataFrame
import dill
import yaml

from src.logger import logging
from src.exception import MyException

# to read yaml file
def read_yaml_file(filepath:str)->dict:
    try:
        with open(filepath,"rb") as yamlfile:
            return yaml.safe_load(yamlfile)
    except Exception as e:
        raise MyException(e,sys) from e
    
def write_yaml_file(filepath:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise MyException (e,sys) from e
    
def load_object(filepath:str)->object:
    try:
        with open(filepath,"rb") as file_obj:
            obj=dill.load(file_obj)
        return obj
    except Exception as e:
        raise MyException(e,sys) from e
    
def save_numpy_array_data(filepath:str,array:np.array):
    try:
        dir_path=os.path.dirname(filepath)
        os.makedirs(dir_path,exist_ok=True)
        with open(filepath,"wb") as file_obj:
            np.save(file_obj,array)
            
    except Exception as e:
        raise MyException (e,sys) from e

def load_numpy_array_data(filepath:str)->np.array:
    try:
        with open(filepath,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MyException (e,sys) from e
    
def save_object(filepath:str,obj:object)->None:
    logging.info("Entered the save object method of utils")
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"wb") as fileobj:
            dill.dump(obj,fileobj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise MyException (e,sys) from e