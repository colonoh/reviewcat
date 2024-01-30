from random import randrange, sample
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

    def get_symptoms(self) -> List[Symptom]:
        """
        Randomly choose some of the symptoms, based on frequency.  Do not pick symptoms with conflicting vital effects.
        """
        selected_symptoms: List[Symptom] = []
        vitals_to_modify: List[str] = []

        # go through the symptoms in a random order so if there are conflicts, the first one doesn't always get picked over the later ones
        for symptom in sample(self.symptoms, k=len(self.symptoms)):
            if randrange(100) <= symptom.frequency:  # pick a number 0..100, and if it is less than the frequency, select this symptom
                # check to see if any vitals this symptom has were already modified/conflict e.g. heart rate can't be both rapid AND slow
                vital_already_modified = False
                for vital in symptom.vitals:
                    if type(vital) in vitals_to_modify:  # type being something like HEART_RATE
                        vital_already_modified = True
                    else:
                        vitals_to_modify.append(type(vital))
                if not vital_already_modified:
                    selected_symptoms.append(symptom)
        return selected_symptoms


class PatientVitals(BaseModel):
    """
    A set of values representing normal levels.
    """
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

    def modify_vitals(self, symptoms: List[Symptom]):
        """
        For any symptoms given which modify vitals, do the modification.
        """
        for symptom in symptoms:
            # overwrite the patient's default vitals with new ones
            for vital in symptom.vitals:
                if vital.name in LEVEL_OF_RESPONSIVENESS.__members__:
                    self.level_of_responsiveness = vital.value
                elif vital.name in HEART_RATE.__members__:
                    self.heart_rate = vital.value
                elif vital.name in HEART_STRENGTH.__members__:
                    self.heart_strength = vital.value
                elif vital.name in HEART_RHYTHM.__members__:
                    self.heart_rhythm = vital.value
                elif vital.name in RESPIRATORY_RATE.__members__:
                    self.respiratory_rate = vital.value
                elif vital.name in RESPIRATORY_RHYTHM.__members__:
                    self.respiratory_rhythm = vital.value
                elif vital.name in RESPIRATORY_EFFORT.__members__:
                    self.respiratory_effort = vital.value
                elif vital.name in SKIN_COLOR.__members__:
                    self.skin_color = vital.value
                elif vital.name in SKIN_TEMPERATURE.__members__:
                    self.skin_temperature = vital.value
                elif vital.name in SKIN_MOISTURE.__members__:
                    self.skin_moisture = vital.value
                elif vital.name in BODY_TEMPERATURE.__members__:
                    self.body_temperature = vital.value
                elif vital.name in PUPILS.__members__:
                    self.pupils = vital.value
                elif vital.name in BLOOD_PRESSURE.__members__:
                    self.blood_pressure = vital.value
                else:
                    raise ValueError(f"Don't know what vital {vital.name} is!")
