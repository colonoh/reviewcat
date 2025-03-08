from enum import Enum
from random import choice, random, sample, randint, shuffle, uniform
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


def generate_respiratory_rate() -> int:
    """
    Not backed by research!!  Picks a value from normal distribution between 12
    and 20.
    """
    mean = 16
    std_dev = 2
    return int(np.random.normal(mean, std_dev))


def generate_body_temperature(age: int, sex: SEX) -> float:
    """
    Temporarily using this formula from ChatGPT, which uses the following supposedly:
    - Mackowiak, P. A., Wasserman, S. S., & Levine, M. M. (1992). A critical appraisal of 98.6°F, the upper limit of 
      the normal body temperature, and other legacies of Carl Reinhold August Wunderlich. JAMA, 268(12), 1578-1580.
    - Sund-Levander, M., Forsberg, C., & Wahren, L. K. (2002). Normal oral, rectal, tympanic, and axillary body 
      temperature in adult men and women: A systematic literature review. Scandinavian Journal of Caring Sciences, 
      16(2), 122-128.
    """
    S = 0 if sex == SEX.MALE else 1  # apparently females are warmer
    eps = uniform(0, 0.5)  # randomness
    return 98.2 - (0.02 * age) + (0.3 * S) + eps


class Patient(BaseModel):
    name: str = Field(default_factory=generate_name)
    age: int = Field(default_factory=lambda: randint(AGE_LOWER_BOUND, AGE_UPPER_BOUND))
    sex: SEX = Field(default_factory=lambda: choice(list(SEX)))

    level_of_responsiveness: LEVEL_OF_RESPONSIVENESS = LEVEL_OF_RESPONSIVENESS.AOx4
    heart_rate: int = Field(default_factory=generate_heart_rate)
    heart_strength: HEART_STRENGTH = HEART_STRENGTH.STRONG
    heart_rhythm: HEART_RHYTHM = HEART_RHYTHM.REGULAR
    respiratory_rate: int = Field(default_factory=generate_respiratory_rate)
    respiratory_rhythm: RESPIRATORY_RHYTHM = RESPIRATORY_RHYTHM.REGULAR
    respiratory_effort: RESPIRATORY_EFFORT = RESPIRATORY_EFFORT.UNLABORED
    skin_color: SKIN_COLOR = SKIN_COLOR.PINK
    body_temperature: float = None  # replaced in generate_dynamic_values()
    skin_moisture: SKIN_MOISTURE = SKIN_MOISTURE.DRY
    skin_temperature: SKIN_TEMPERATURE = SKIN_TEMPERATURE.WARM
    pupils: PUPILS = PUPILS.PERRL
    # TODO: blood pressure

    difficulty: DIFFICULTY = DIFFICULTY.MEDIUM
    condition_name: str = None
    condition_description: str = None
    condition_selected_symptoms: list[str] = []  # symptoms we show the user
    condition_hidden_symptoms: list[str] = []  # symptoms that affect the patient but are hidden from the user
    condition_unselected_symptoms: list[str] = []  # symptoms that do not affect the patient

    condition_treatments: list[str] = []
    condition_evacuation_guidelines: list[str] = []

    @model_validator(mode="after")
    def generate_dynamic_values(cls, values):
        """
        Cause I don't a better way, generate the values based on other values here.
        """
        values.body_temperature = generate_body_temperature(values.age, values.sex)
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
            if not condition.get("sex") or condition.get("sex") == self.sex.value:  # restrict to sex (if applicable)
                self.condition_name = name
                self.condition_description = condition["description"]

                affected_vitals = set()
                shuffle(condition["symptoms"])  # randomize the conditions
                for symptom_name in condition["symptoms"]:
                    g = global_symptoms[symptom_name]
                    if not set(g.get("affects", [])).isdisjoint(affected_vitals):  # if any of this's symptom's vitals are already affected
                        self.condition_unselected_symptoms.append(symptom_name)
                        continue

                    # if we haven't selected at least a certain amount of symptoms, keep selecting them
                    ratio_of_symptoms_selected = (len(self.condition_selected_symptoms) + len(self.condition_hidden_symptoms)) / len(condition["symptoms"])
                    if ratio_of_symptoms_selected <= self.difficulty_percentage():
                        if g.get("affects"):  # if it affects the vitals (e.g. "rapid heart rate)
                            self.condition_hidden_symptoms.append(symptom_name)
                            for affected, changed in zip(g.get("affects", []), g.get("change", [])):
                                self.modify_vitals(affected, changed)
                                affected_vitals.add(affected)
                        else:  # doesn't affect vitals (e.g. "discomfort in the neck")
                            self.condition_selected_symptoms.append(symptom_name)

                    else:  # we have enough, this one wasn't selected
                        self.condition_unselected_symptoms.append(symptom_name)

                self.condition_treatments = condition["txs"]
                self.condition_evacuation_guidelines = condition.get("evacs", [])
                
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
                self.heart_rate = int(self.heart_rate*0.8)  # TODO
                return
            elif change == "increase":
                self.heart_rate = int(self.heart_rate*1.5)  # TODO
                return
        
        elif affects == "heart_strength":
            if change == "weak":
                self.heart_strength = HEART_STRENGTH.WEAK
                return
        
        elif affects == "heart_rhythm":
            if change == "irregular":
                self.heart_rhythm = HEART_RHYTHM.IRREGULAR
                return

        elif affects == "respiratory_rate":
            if change == "decrease":
                self.respiratory_rate = int(self.respiratory_rate*0.8)  # TODO
                return
            elif change == "increase":
                self.respiratory_rate = int(self.respiratory_rate*1.5)  # TODO
                return

        elif affects == "respiratory_effort":
            if change == "shallow":
                self.respiratory_effort = RESPIRATORY_EFFORT.SHALLOW
                return

        elif affects == "skin_color":
            if change == "pale":
                self.skin_color = SKIN_COLOR.PALE
                return
            
        elif affects == "skin_temperature":
            if change == "cool":
                self.skin_temperature = SKIN_TEMPERATURE.COOL
                return
            
        elif affects == "skin_moisture":
            if change == "clammy":
                self.skin_moisture = SKIN_MOISTURE.CLAMMY
                return
            
        raise ValueError(f"Unhandled modification of vitals: {affects=}, {change=}")  # shouldn't get this far


    def difficulty_percentage(self) -> float:
        if self.difficulty == DIFFICULTY.HARD:
            return 0.5
        elif self.difficulty == DIFFICULTY.MEDIUM:
            return 0.75
        else:
            return 1.0
