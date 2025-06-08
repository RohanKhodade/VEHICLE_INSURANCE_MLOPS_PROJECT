# ---------------component to check the logging module--------------------
# from src.logger import logging

# logging.info("This is an info message")
# logging.debug("This is a dubug message")
# logging.error("This is an error message")


# ------------------ Component to check the custom exception module ----------------------
# from src.logger import logging
# from src.exception import MyException
# import sys

# try:
#     print(1/0)
# except Exception as e:
#     logging.info("divide by zero error")
#     raise MyException(e,sys) from e

    
# to check pipeline

from src.pipeline.training_pipeline import TrainPipeline

train_pipeline=TrainPipeline()
train_pipeline.run_pipeline()
