from random import choice

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from wfr_conditions import conditions
from models import SEX, LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, BODY_TEMPERATURE, PUPILS, \
BLOOD_PRESSURE, Symptom, Condition, PatientVitals


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    """
    Pick a random condition, get some of the symptoms, create baseline patient vitals, modify them based on the 
    symptoms, and return that data to the template.
    """
    condition = choice(conditions)
    selected_symptoms = condition.get_symptoms()

    patient = PatientVitals()
    patient.modify_vitals(selected_symptoms)

    return templates.TemplateResponse(request=request,
                                      name="index.html",
                                      context={"patient": patient,
                                               "selected_symptoms": selected_symptoms,
                                               "condition": condition})
