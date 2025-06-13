from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse,RedirectResponse
from uvicorn import run as app_run

from typing import Optional

from src.constants import APP_HOST,APP_PORT
from src.pipeline.prediction_pipeline import  VehicleData,VehicleDataClassifier
from src.pipeline.training_pipeline import TrainPipeline


#initialize the fast api application
app=FastAPI()

# mount static files for serving static files like css
app.mount("/static",StaticFiles(directory="static"),name="static")

# jinja 2 template setup
templates=Jinja2Templates(directory="templates")

origins=["*"]

# configure middle ware
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )
class DataForm:
    """
    Dataformm class to handle and process incoming form of data
    """
    def __init__(self,request:Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None
        
    async def get_vehicle_data(self):
        """
        method to retrive and assign form data to class attribute
        this method is asynchronous to handle form data fethcing without blocking
        """
        form = await self.request.form()
        self.Gender = form.get("Gender")
        self.Age = form.get("Age")
        self.Driving_License = form.get("Driving_License")
        self.Region_Code = form.get("Region_Code")
        self.Previously_Insured = form.get("Previously_Insured")
        self.Annual_Premium = form.get("Annual_Premium")
        self.Policy_Sales_Channel = form.get("Policy_Sales_Channel")
        self.Vintage = form.get("Vintage")
        self.Vehicle_Age_lt_1_Year = form.get("Vehicle_Age_lt_1_Year")
        self.Vehicle_Age_gt_2_Years = form.get("Vehicle_Age_gt_2_Years")
        self.Vehicle_Damage_Yes = form.get("Vehicle_Damage_Yes")
        
@app.get("/",tags=["authentication"])
async def index(request:Request):
    """
    Renders main html tamplate for vehicle data input
    """
    return templates.TemplateResponse(
        "vehicledata.html",{"request":request,"context":"Rendering"}
    )
    
@app.get("/train")
async def trainRouteClient():
    """
    Endpoint to initiate the modle training pipeline
    """
    try:
        train_pipeline=TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successfull")
    except Exception as e:
        return Response(f"Error occured! {e}")
    
@app.post("/")
async def predictRouteClient(request:Request):
    """
    End point to recive form data,process it  and make the prediction
    """
    try:
        form=DataForm(request)
        await form.get_vehicle_data()
        vehicle_data = VehicleData(
                                Gender= form.Gender,
                                Age = form.Age,
                                Driving_License = form.Driving_License,
                                Region_Code = form.Region_Code,
                                Previously_Insured = form.Previously_Insured,
                                Annual_Premium = form.Annual_Premium,
                                Policy_Sales_Channel = form.Policy_Sales_Channel,
                                Vintage = form.Vintage,
                                Vehicle_Age_lt_1_Year = form.Vehicle_Age_lt_1_Year,
                                Vehicle_Age_gt_2_Years = form.Vehicle_Age_gt_2_Years,
                                Vehicle_Damage_Yes = form.Vehicle_Damage_Yes
                                )
        # convert form data to dataframe for the model
        vehicle_df=vehicle_data.get_vehicle_input_data_frame()
        
        # initiate prediction pipeline
        model_predictor=VehicleDataClassifier()
        
        # make prediction and retrive the result
        value=model_predictor.predict(dataframe=vehicle_df)[0]
        
        # interupt the prediction result as Response-yes or response no
        status="Reponse-yes" if value==1 else "Response-No"
        
        # render the same html page with prediction result
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request":request,"context":status},
        )
        
    except Exception as e:
        return {"status":False,"error":f"{e}"}
    
# main entry point to start the fast api server

if __name__=="__main__":
    app_run(app,host=APP_HOST,port=APP_PORT)