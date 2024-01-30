from typing import List, Union

from pydantic import BaseModel

from constants import FREQUENCY, SEX, LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, \
HEART_RHYTHM, RESPIRATORY_RATE, RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, \
BODY_TEMPERATURE, PUPILS, BLOOD_PRESSURE


class Symptom(BaseModel):
    """
    A sign or symptom.  May have an effect on vitals (potentially multiple, hence the list).
    """
    name: str
    frequency: FREQUENCY = FREQUENCY.DEFAULT
    vitals: List[Union[LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
                       RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, \
                       BODY_TEMPERATURE, PUPILS, BLOOD_PRESSURE]]


class Condition(BaseModel):
    """
    A medical condition/disease/ailment.  
    """
    name: str
    sex: SEX = SEX.ANY  # conditions specific to a sex
    description: str = ""
    symptoms: List[Symptom]
    treatments: List[str]
    evacuation_guidelines: List[str]
    # references: List[str] = []


class PatientVitals(BaseModel):
    level_of_responsiveness: str = LEVEL_OF_RESPONSIVENESS.AOx4.value
    heart_rate: int = HEART_RATE.NORMAL.value
    heart_strength: str = HEART_STRENGTH.STRONG.value
    heart_rhythm: str = HEART_RHYTHM.REGULAR.value
    respiratory_rate: int = RESPIRATORY_RATE.NORMAL.value
    respiratory_rhythm: str = RESPIRATORY_RHYTHM.REGULAR.value
    respiratory_effort: str = RESPIRATORY_EFFORT.UNLABORED.value
    skin_color: str = SKIN_COLOR.PINK.value
    skin_temperature: str = SKIN_TEMPERATURE.WARM.value
    skin_moisture: str = SKIN_MOISTURE.DRY.value
    body_temperature: float = BODY_TEMPERATURE.NORMAL.value
    pupils: str = PUPILS.PERRL.value
    blood_pressure: str = BLOOD_PRESSURE.NORMAL.value

