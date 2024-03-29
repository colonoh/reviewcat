from enum import Enum, IntEnum
from random import choice, random, sample
from typing import List, Union

from pydantic import BaseModel


class SEX(Enum):
    ANY = "any"
    FEMALE = "female"
    MALE = "male"

class FREQUENCY(float, Enum):  # perecent, where 1. = 100%
    RARELY = .2
    SOMETIMES = .5
    OFTEN = .8
    DEFAULT = .9
    ALWAYS = 1.

class LEVEL_OF_RESPONSIVENESS(Enum):
    AOx4 = "A&Ox4"
    AOx3 = "A&Ox3"
    AOx2 = "A&Ox2"
    AOx1 = "A&Ox1"
    # TODO: V, P, U

class HEART_RATE(IntEnum):
    SLOW = 40  # TODO
    NORMAL = 75  # TODO
    RAPID = 120  # TODO

class HEART_STRENGTH(Enum):
    WEAK = "weak"
    STRONG = "strong"

class HEART_RHYTHM(Enum):
    REGULAR = "regular"
    IRREGULAR = "irregular"

class RESPIRATORY_RATE(IntEnum):
    SLOW = 10  # TODO
    NORMAL = 16  # TODO
    RAPID = 25  # TODO

class RESPIRATORY_RHYTHM(Enum):
    REGULAR = "regular"
    IRREGULAR = "irregular"

class RESPIRATORY_EFFORT(Enum):
    UNLABORED = "unlabored"
    LABORED = "labored"
    SHALLOW = "shallow"

class SKIN_COLOR(Enum):
    PINK = "pink"
    PALE = "pale"

class SKIN_TEMPERATURE(Enum):
    WARM = "warm"
    COOL = "cool"
    HOT = "hot"

class SKIN_MOISTURE(Enum):
    DRY = "dry"
    WET = "wet"
    CLAMMY = "clammy"

class BODY_TEMPERATURE(float, Enum):  # degF
    NORMAL = 98.6
    HOT = 102.0  # TODO
    COLD = 96.0  # TODO

class PUPILS(Enum):
    PERRL = "equal, round, and reactive to light"

class BLOOD_PRESSURE(Enum):
    NORMAL = "a strong radial pulse"
    WEAK = "no detectable radial pulse"

class Symptom(BaseModel):
    """
    A sign or symptom.  If the symptom has an effect on vitals, the vital it affects should be in `vitals`.  Multiple 
    items in the `vitals` list are treated as if they are AND-ed together.  
    """
    name: str
    frequency: FREQUENCY = FREQUENCY.DEFAULT  # how often does this symptom occur
    vitals: List[Union[LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
                       RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, \
                       BODY_TEMPERATURE, PUPILS, BLOOD_PRESSURE]] = []

class Condition(BaseModel):
    """
    A medical condition/disease/ailment.  
    """
    name: str
    sex: SEX = SEX.ANY  # this condition is limited to this sex
    description: str
    symptoms: List[Symptom]
    treatments: List[str]
    evacuation_guidelines: List[str]
    # references: List[str] = []


class Patient(BaseModel):
    """
    Starts with vital values representing normal levels.
    """
    name: str = "Alex"
    condition: Condition
    selected_symptoms: List[Symptom] = []

    # vitals
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

    @property
    def sex(self) -> str:
        """
        Use the condition-specific sex or generate a random one if it affects everyone.
        """
        return self.condition.sex.value if self.condition.sex != SEX.ANY else choice([SEX.FEMALE.value, SEX.MALE.value])

    def get_symptoms(self):
        """
        Randomly choose some of the symptoms, based on frequency.  Do not pick symptoms with conflicting vital effects.
        """
        vitals_to_modify: set[str] = set()

        # go through the symptoms in a random order so if there are conflicts, the first one doesn't always get picked over the later ones
        for symptom in sample(self.condition.symptoms, k=len(self.condition.symptoms)):
            if random() <= symptom.frequency:  # pick a number 0..1, and if it is less than the frequency, select this symptom
                # check to see if any vitals this symptom has were already modified/conflict e.g. heart rate can't be both rapid AND slow
                vital_already_modified = False
                for vital in symptom.vitals:
                    if type(vital) in vitals_to_modify:  # type being something like HEART_RATE
                        vital_already_modified = True
                    else:
                        vitals_to_modify.add(type(vital))
                if not vital_already_modified:
                    self.selected_symptoms.append(symptom)

    def modify_vitals(self):
        """
        For any symptoms given which modify vitals, do the modification.
        """
        for symptom in self.selected_symptoms:
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
