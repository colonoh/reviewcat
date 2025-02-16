from random import choice

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from mangum import Mangum # type: ignore

from wfr_conditions import conditions
from models import SEX, LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, BODY_TEMPERATURE, PUPILS, \
BLOOD_PRESSURE, Symptom, Condition, Patient


app = FastAPI()
templates = Jinja2Templates(directory="templates")
version = "0.0.2"


@app.get("/dev/")  # TODO: this is hardcoded to get this to work on AWS Lambda, fix this someday
def index(request: Request):
    """
    Pick a random condition, get some of the symptoms, create baseline patient vitals, modify them based on the 
    symptoms, and return that data to the template.
    """
    print(f"root_path /dev/: {request.scope.get("root_path")}")
    patient = Patient(condition=choice(conditions))
    patient.get_symptoms()
    patient.modify_vitals()

    return templates.TemplateResponse(request=request, name="index.html", context={"patient": patient, "version": version})


handler = Mangum(app)
