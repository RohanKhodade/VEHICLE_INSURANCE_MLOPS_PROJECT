import os
from pathlib import Path

project_name="src"

list_of_files=[
    f"{project_name}/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/components/data_ingestion.py",
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/configuration/mongodb_connection.py",
    f"{project_name}/data_access/__init__.py",
    f"{project_name}/data_access/project_data.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/entity/estimator.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/training_pipeline.py",
    f"{project_name}/pipeline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/main_utils.py",
    f"{project_name}/noteboook/mongodb_demo.ipynb",
    "app.py",
    "demo.py",
    "Dockerfile",
    ".dockerignore",
    "pyproject.toml",
    "setup.py",
    "requirements.txt",
    "config/model.yaml",
    "config/schema.yaml",
]

for file in list_of_files:
    file_path=Path(file)
    file_dir,file_name=os.path.split(file_path)
    if file_dir !="":
        os.makedirs(file_dir,exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path,"w") as f:
            pass
    else:
        print("file : {} already exists".format(file_path))
        
print("done")