from dataclasses import dataclass
from enum import auto, Enum
from random import randrange, sample
from typing import List, Union

from pydantic import BaseModel

from constants import PatientVitals, FREQUENCY, SEX, LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, \
HEART_RHYTHM, RESPIRATORY_RATE, RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, \
BODY_TEMPERATURE, PUPILS, BLOOD_PRESSURE


class Symptom(BaseModel):
    """
    A sign or symptom.  May affect vitals.  Each item in the vitals list 
    """
    name: str
    frequency: FREQUENCY = FREQUENCY.DEFAULT
    vitals: List[List[Union[LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
                            RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, \
                            BODY_TEMPERATURE, PUPILS, BLOOD_PRESSURE]]]  # outer list is OR'd, inner list is AND'd


class Condition(BaseModel):
    """
    """
    name: str
    sex: SEX = SEX.ANY  # conditions specific to a sex
    description: str = ""
    symptoms: List[Symptom]
    treatments: List[str]
    evacuation_guidelines: List[str]
    # references: List[str] = []


# read in a condition, symptoms, vitals
s1 = Symptom(name="Pale, cool, clammy skin",
             vitals=[[SKIN_COLOR.PALE, SKIN_TEMPERATURE.COOL, SKIN_MOISTURE.CLAMMY]])
s2 = Symptom(name="Rapid heartbeat",
             vitals=[[HEART_RATE.RAPID]])  # conflicts with slow heart rate
s3 = Symptom(name="Slow heartbeat",
             vitals=[[HEART_RATE.SLOW]])  # conflicts with rapid heart rate

condition = Condition(name="Shock",
                      symptoms=[s1, s2, s3],
                      treatments=["Treatment 1"],
                      evacuation_guidelines=["Evac 1"])
# print(condition)

# pick some of the symptoms (but keep all of them)
selected_symptoms: List[str] = []
vitals_to_modify: List[str] = []  # type: Union...

# go through the symptoms in a random order so if there are conflicts, the first one doesn't always get expressed over the later ones
for symptom in sample(condition.symptoms, k=len(condition.symptoms)):
    if randrange(100) <= symptom.frequency:  # pick a number 0..100, and if less than the freq, select this symptom
        # check to see if any vitals this symptom has were already modified/conflict e.g. heart rate can't be both rapid AND slow
        vital_already_modified = False
        for vitals in symptom.vitals:
            for vital in vitals:
                if type(vital) in vitals_to_modify:  # type being something like HEART_RATE
                    vital_already_modified = True
                else:
                    vitals_to_modify.append(type(vital))
        if not vital_already_modified:
            selected_symptoms.append(symptom.name)

print(selected_symptoms)
print(vitals_to_modify)

# create a baseline patient
patient = PatientVitals()
for symptom in condition.symptoms:
    if symptom.name in selected_symptoms:
        # overwrite the patient's default vitals with new ones
        for vitals in symptom.vitals:
            for vital in vitals:
                if vital.name in LEVEL_OF_RESPONSIVENESS.__members__:
                    patient.level_of_responsiveness = vital.value
                elif vital.name in HEART_RATE.__members__:
                    patient.heart_rate = vital.value
                elif vital.name in HEART_STRENGTH.__members__:
                    patient.heart_strength = vital.value
                elif vital.name in HEART_RHYTHM.__members__:
                    patient.heart_rhythm = vital.value
                elif vital.name in RESPIRATORY_RATE.__members__:
                    patient.respiratory_rate = vital.value
                elif vital.name in RESPIRATORY_RHYTHM.__members__:
                    patient.respiratory_rhythm = vital.value
                elif vital.name in RESPIRATORY_EFFORT.__members__:
                    patient.respiratory_effort = vital.value
                elif vital.name in SKIN_COLOR.__members__:
                    patient.skin_color = vital.value
                elif vital.name in SKIN_TEMPERATURE.__members__:
                    patient.skin_temperature = vital.value
                elif vital.name in SKIN_MOISTURE.__members__:
                    patient.skin_moisture = vital.value
                elif vital.name in BODY_TEMPERATURE.__members__:
                    patient.body_temperature = vital.value
                elif vital.name in PUPILS.__members__:
                    patient.pupils = vital.value
                elif vital.name in BLOOD_PRESSURE.__members__:
                    patient.blood_pressure = vital.value
                else:
                    raise ValueError(f"Don't know what vital {vital.name} is!")

# return the select symptoms and patient data
for s in selected_symptoms:
    print(s)
print(patient)

# return all the symptoms, treatments, evac guidelines
print(condition)