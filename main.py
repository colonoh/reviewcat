from typing import Union

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from constants import LEVEL_OF_RESPONSIVENESS, FREQUENCY, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_COLOR, SKIN_MOISTURE, TEMPERATURE, PUPILS, \
BLOOD_PRESSURE, PatientVitals


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    patient = PatientVitals()


    return templates.TemplateResponse(
        request=request, name="index.html", context={"msg": "Hello world", "patient": patient}
    )

