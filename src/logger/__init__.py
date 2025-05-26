import os
import logging
from logging.handlers import RotatingFileHandler
from from_root import from_root
from datetime import datetime

#configure the parameters for logging
LOG_DIR="logs"
LOG_FILE_NAME=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH=os.path.join(from_root(),LOG_DIR,LOG_FILE_NAME)
MAX_LOG_SIZE=5*1024*1024 # file size max 5 mb
LOG_BACKUP_COUNT=3 # keep 3 backup files

# create log dir if not exists 
os.makedirs(LOG_DIR,exist_ok=True)

#configure logging

def configure_logging():
    
    #configure the logger here
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    #Define the logger formatter how the log should be formatted
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    #File handler with rotation
    file_handler=RotatingFileHandler(LOG_FILE_PATH,maxBytes=MAX_LOG_SIZE,backupCount=LOG_BACKUP_COUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # configure console_handler
    console_handler=logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    

# call the logging here
configure_logging()    