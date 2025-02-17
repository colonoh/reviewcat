from enum import Enum, IntEnum
from random import choice, random, sample, randint, shuffle
from typing import List, Union
import yaml

import numpy as np
from pydantic import BaseModel, Field, model_validator


AGE_LOWER_BOUND = 18
AGE_UPPER_BOUND = 80


class SEX(Enum):
    FEMALE = "female"
    MALE = "male"

    def __str__(self):
        return self.value

class LEVEL_OF_RESPONSIVENESS(Enum):
    AOx4 = "A&Ox4"
    AOx3 = "A&Ox3"
    AOx2 = "A&Ox2"
    AOx1 = "A&Ox1"
    VERBAL = "verbal"
    PAIN = "pain"
    UNRESPONSIVE = "unresponsive"

    def __str__(self):
        return self.value

class HEART_STRENGTH(Enum):
    WEAK = "weak"
    STRONG = "strong"

    def __str__(self):
        return self.value

class HEART_RHYTHM(Enum):
    REGULAR = "regular"
    IRREGULAR = "irregular"

    def __str__(self):
        return self.value


class RESPIRATORY_RHYTHM(Enum):
    REGULAR = "regular"
    IRREGULAR = "irregular"

    def __str__(self):
        return self.value


class RESPIRATORY_EFFORT(Enum):
    UNLABORED = "unlabored"
    LABORED = "labored"
    SHALLOW = "shallow"

    def __str__(self):
        return self.value

class SKIN_COLOR(Enum):
    PINK = "pink"
    PALE = "pale"

    def __str__(self):
        return self.value

class SKIN_TEMPERATURE(Enum):
    WARM = "warm"
    COOL = "cool"
    HOT = "hot"

    def __str__(self):
        return self.value

class SKIN_MOISTURE(Enum):
    DRY = "dry"
    WET = "wet"
    CLAMMY = "clammy"

    def __str__(self):
        return self.value

class PUPILS(Enum):
    NOT_PERRL = "not equal, round, and reactive to light"
    PERRL = "equal, round, and reactive to light"

    def __str__(self):
        return self.value

class DIFFICULTY(Enum):  # difficulty of the quiz
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

def generate_name() -> str:
    unisex_names = [
        "Alex", "Andy", "Avery", "Blake", "Casey", "Charlie", "Dakota", 
        "Devin", "Drew", "Elliot", "Emery", "Finley", "Frankie", "Harper", 
        "Hayden", "Jamie", "Jordan", "Jules", "Kai", "Kendall", "Lane", 
        "Logan", "Micah", "Morgan", "Parker", "Quinn", "Reese", "Riley", 
        "River", "Robin", "Rowan", "Sage", "Sam", "Skylar", "Taylor", "Tatum", 
        "Toby", "Tyler", "Wren" 
    ]
    return choice(unisex_names)


def generate_heart_rate() -> int:
    """
    Not backed by research!!  Picks a value from normal distribution between 60
    and 100 (bpm).
    """
    mean = 80  # bpm
    std_dev = 7.72  # calculated to get 99% of the vaules within 60-100
    return int(np.random.normal(mean, std_dev))


class SuperPatient(BaseModel):
    name: str = Field(default_factory=generate_name)
    age: int = Field(default_factory=lambda: randint(AGE_LOWER_BOUND, AGE_UPPER_BOUND))
    sex: SEX = Field(default_factory=lambda: choice(list(SEX)))

    level_of_responsiveness: LEVEL_OF_RESPONSIVENESS = LEVEL_OF_RESPONSIVENESS.AOx4
    heart_rate: int = 80 #Field(default_factory=lambda: generate_heart_rate)
    heart_strength: HEART_STRENGTH = HEART_STRENGTH.STRONG
    heart_rhythm: HEART_RHYTHM = HEART_RHYTHM.REGULAR
    respiratory_rate: int = 0  # Will be set dynamically
    respiratory_rhythm: RESPIRATORY_RHYTHM = RESPIRATORY_RHYTHM.REGULAR
    respiratory_effort: RESPIRATORY_EFFORT = RESPIRATORY_EFFORT.UNLABORED
    skin_color: SKIN_COLOR = SKIN_COLOR.PINK
    skin_temperature: float = 98.6  # TODO
    skin_moisture: SKIN_MOISTURE = SKIN_MOISTURE.DRY
    body_temperature: float = 98.6  # TODO
    pulils: PUPILS = PUPILS.PERRL
    # TODO: blood pressure

    difficulty: DIFFICULTY = DIFFICULTY.EASY
    condition_name: str = None
    condition_description: str = None
    condition_symptoms: list[str] = []
    condition_treatments: list[str] = []
    condition_evacuation_guidelines: list[str] = []


    @model_validator(mode="after")
    def generate_dynamic_values(cls, values):
        """
        Cause I don't a better way, generate the values based on other values here.
        """
        values.respiratory_rate = 22 - values.age  # TODO: nonsense 
        return values

    def pick_condition(self):
        # pick a random condition that 
        with open("wfr_conditions.yaml", "r") as f:
            data = yaml.safe_load(f)
        global_symptoms = data["symptoms"]
        all_conditions = data["conditions"]
        names = list(all_conditions.keys())
        shuffle(names)
        for name in names:
            condition = all_conditions[name]
            # get one that only applies to this (or any) sex
            if not condition.get("sex") or condition.get("sex") == self.sex.value:
                self.condition_name = name
                self.condition_description = condition["description"]
                # TODO: only pick some, and don't pick vitals that already have been affected
                for symptom_name in condition["symptoms"]:
                    self.condition_symptoms.append(symptom_name)
                    g = global_symptoms[symptom_name]
                    for affected, changed in zip(g.get("affects", []), g.get("change", [])):
                        self.modify_vitals(affected, changed)
                self.condition_treatments = condition["txs"]
                self.condition_evacuation_guidelines = condition["evacs"]
                return
        
        if self.condition_name == None:
            raise Exception(f"Could not find any matching conditions for {self.sex.name=}")


    def modify_vitals(self, affects: str, change: str):
        if affects == "level_of_responsiveness":
            if change == "decrease":
                if self.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx4:
                    self.level_of_responsiveness = LEVEL_OF_RESPONSIVENESS.AOx3
                elif self.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx3:
                    self.level_of_responsiveness = LEVEL_OF_RESPONSIVENESS.AOx2
                elif self.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx2:
                    self.level_of_responsiveness = LEVEL_OF_RESPONSIVENESS.AOx1
                elif self.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx1:
                    self.level_of_responsiveness = LEVEL_OF_RESPONSIVENESS.VERBAL
                elif self.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.VERBAL:
                    self.level_of_responsiveness = LEVEL_OF_RESPONSIVENESS.PAIN
                elif self.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.PAIN:
                    self.level_of_responsiveness = LEVEL_OF_RESPONSIVENESS.UNRESPONSIVE
                return

        elif affects == "heart_rate":
            if change == "decrease":
                self.heart_rate = int(self.heart_rate*0.8)
                return
            elif change == "increase":
                self.heart_rate = int(self.heart_rate*1.2)
                return
        
        elif affects == "heart_strength":
            if change == "set_weak":
                self.heart_strength = HEART_STRENGTH.WEAK
                return
        
        elif affects == "heart_rhythm":
            if change == "set_irregular":
                self.heart_rhythm = HEART_RHYTHM.IRREGULAR
                return

        elif affects == "skin_color":
            if change == "pale":
                self.skin_color = SKIN_COLOR.PALE
                return
            
        elif affects == "skin_temperature":
            if change == "cool":
                self.skin_temperature *= 0.9  # TODO
                return
            
        elif affects == "skin_moisture":
            if change == "clammy":
                self.skin_moisture = SKIN_MOISTURE.CLAMMY
                return
            
        raise ValueError(f"Unhandled modification of vitals: {affects=}, {change=}")  # shouldn't get this far


class BLOOD_PRESSURE(Enum):
    NORMAL = "a strong radial pulse"
    WEAK = "no detectable radial pulse"


class FREQUENCY(float, Enum):  # perecent, where 1. = 100%
    RARELY = .2
    SOMETIMES = .5
    OFTEN = .8
    DEFAULT = .9
    ALWAYS = 1.
