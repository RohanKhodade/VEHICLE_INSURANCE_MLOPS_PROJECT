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
