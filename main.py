from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from models import SEX, LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, BODY_TEMPERATURE, PUPILS, \
BLOOD_PRESSURE, Symptom, Condition, PatientVitals


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    # read in a condition, symptoms, vitals
    s1 = Symptom(name="Pale, cool, clammy skin",
                 vitals=[SKIN_COLOR.PALE, SKIN_TEMPERATURE.COOL, SKIN_MOISTURE.CLAMMY])
    s2 = Symptom(name="Rapid heartbeat",
                 vitals=[HEART_RATE.RAPID])  # conflicts with slow heart rate
    s3 = Symptom(name="Slow heartbeat",
                 vitals=[HEART_RATE.SLOW])  # conflicts with rapid heart rate

    condition = Condition(name="Shock",
                          symptoms=[s1, s2, s3],
                          treatments=["Treatment 1"],
                          evacuation_guidelines=["Evac 1"])
    # print(condition)

    selected_symptoms = condition.get_symptoms()
    print(selected_symptoms)

    # create a baseline patient
    patient = PatientVitals()
    patient.modify_vitals(selected_symptoms)

    # return the select symptoms and patient data
    for s in selected_symptoms:
        print(s.name)
    print(patient)

    # return all the symptoms, treatments, evac guidelines
    print(condition)


    return templates.TemplateResponse(request=request, name="index.html", context={"patient": patient,
                                                                                   "selected_symptoms": selected_symptoms,
                                                                                   "condition": condition}
    )

