from random import choice

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from mangum import Mangum # type: ignore

from models import Patient


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

    super_patient = Patient()
    super_patient.pick_condition()

    return templates.TemplateResponse(request=request, name="index.html", context={"patient": super_patient, "version": version})


handler = Mangum(app)
