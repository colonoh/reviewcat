from dataclasses import dataclass
from enum import auto, Enum, StrEnum
import json
import random

from click import echo, pause


class LEVEL_OF_RESPONSIVENESS(Enum):
    AOx4 = "A&Ox4"
    AOx3 = "A&Ox3"
    AOx2 = "A&Ox2"
    AOx1 = "A&Ox1"
    # TODO: V, P, U

class FREQUENCY(Enum):
    RARELY = 0.2
    SOMETIMES = 0.5
    OFTEN = 0.8
    DEFAULT = 0.9
    ALWAYS = 1.0

class HEART_RATE(Enum):
    SLOW = 40  # TODO
    NORMAL = 75  # TODO
    RAPID = 120  # TODO

class HEART_STRENGTH(Enum):
    WEAK = "weak"
    STRONG = "strong"

class HEART_RHYTHM(Enum):
    REGULAR = "regular"
    IRREGULAR = "irregular"

class RESPIRATORY_RATE(Enum):
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

class SKIN_COLOR(Enum):
    PINK = "pink"
    PALE = "pale"

class SKIN_MOISTURE(Enum):
    DRY = "dry"
    WET = "wet"
    CLAMMY = "clammy"

class TEMPERATURE(Enum):  # degF
    NORMAL = 98.6
    HOT = 102.0  # TODO
    COLD = 96.0  # TODO

class PUPILS(Enum):
    PERRL = "equal, round, and reactive to light"

class BLOOD_PRESSURE(Enum):
    NORMAL = "a strong radial pulse"
    WEAK = "no detectable radial pulse"

@dataclass
class PatientVitals:
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
    temperature: float = TEMPERATURE.NORMAL.value
    pupils: str = PUPILS.PERRL.value
    blood_pressure: str = BLOOD_PRESSURE.NORMAL.value


def main():
    # pick a condition
    with open("conditions3.json", "r") as f:
        data = json.load(f)
    condition = random.choice(data)
    
    # pick symptoms
    patient = PatientVitals()
    unselected_symptoms = list()

    # process in a random order so that for opposing symptoms (e.g. slow and rapid heart rate), the last one isn't the only one that gets used
    for symptom in random.sample(condition["symptoms"], k=len(condition["symptoms"])):  
        frequency = FREQUENCY[symptom["frequency"]] if "frequency" in symptom else FREQUENCY["DEFAULT"]
        if random.random() > frequency.value:  # this symptom is randomly chosen to not be selected/presented to the user
            unselected_symptoms.append(symptom)
        else:  # selected but may still be hidden
            # if "hidden" in symptom and symptom["hidden"]:  # vital-affected symptoms are hidden since you can find them through the modified vitals
            #     hidden_symptoms.append(symptom)

            # modify vitals
            if "vitals" in symptom:
                for vitals in symptom["vitals"]:
                    # simple and straightforward but long
                    for vital in vitals:
                        if vital == "HEART_RATE_RAPID":
                            patient.heart_rate = HEART_RATE.RAPID.value
                        elif vital == "HEART_RATE_SLOW":
                            patient.heart_rate = HEART_RATE.SLOW.value
                        elif vital == "HEART_STRENGTH_WEAK":
                            patient.heart_strength = HEART_STRENGTH.WEAK.value
                        elif vital == "HEART_RHYTHM_IRREGULAR":
                            patient.heart_rhythm = HEART_RHYTHM.IRREGULAR.value
                        elif vital == "RESPIRATORY_RATE_RAPID":
                            patient.respiratory_rate = RESPIRATORY_RATE.RAPID.value
                        elif vital == "RESPIRATORY_RATE_SLOW":
                            patient.respiratory_rate = RESPIRATORY_RATE.SLOW.value
                        elif vital == "RESPIRATORY_RHYTHM_IRREGULAR":
                            patient.respiratory_rhythm = RESPIRATORY_RHYTHM.IRREGULAR.value
                        elif vital == "RESPIRATORY_EFFORT_LABORED":
                            patient.respiratory_effort = RESPIRATORY_EFFORT.LABORED.value
                        elif vital == "RESPIRATORY_EFFORT_SHALLOW":
                            patient.respiratory_effort = RESPIRATORY_EFFORT.SHALLOW.value
                        elif vital == "SKIN_COLOR_PALE":
                            patient.skin_color = SKIN_COLOR.PALE.value
                        elif vital == "SKIN_TEMPERATURE_COOL":
                            patient.skin_temperature = SKIN_TEMPERATURE.COOL.value
                        elif vital == "SKIN_TEMPERATURE_HOT":
                            patient.skin_temperature = SKIN_TEMPERATURE.HOT.value
                        elif vital == "SKIN_MOISTURE_WET":
                            patient.skin_moisture = SKIN_MOISTURE.WET.value
                        elif vital == "SKIN_MOISTURE_CLAMMY":
                            patient.skin_moisture = SKIN_MOISTURE.CLAMMY.value
                        else:
                            raise ValueError(f"Error: Cannot handle unknown vital `{vital}`!")

    # TODO: add jitter to some of the values

    sex = f"{condition["sex"].lower()}" if "sex" in condition else random.choice(["female", "male"])
    echo(f"You have a {sex} patient who has the following vitals:")
    echo(f"- Level of responsiveness: {patient.level_of_responsiveness}")
    echo(f"- Heart rate: {patient.heart_rate}, {patient.heart_strength}, and {patient.heart_rhythm}")
    echo(f"- Respiratory rate: {patient.respiratory_rate}, {patient.respiratory_rhythm}, and {patient.respiratory_effort}")
    echo(f"- Skin: {patient.skin_color}, {patient.skin_temperature}, and {patient.skin_moisture}")
    echo(f"- Temperature: {patient.temperature} degrees F")
    echo(f"- Pupils: {patient.pupils}")
    echo(f"- Blood pressure: {patient.blood_pressure}")

    echo("\nThe patient has the following signs & symptoms:")
    for symptom in condition["symptoms"]:
        if symptom not in unselected_symptoms and "vitals" not in symptom:
            echo(f"- {symptom["name"]}")
    
    # wait for input
    echo("\nWhat do you think the condition is?  What are the treatments?  What are the evacuation guidelines?\n")
    pause()
    echo("")

    # present condition/treatment/evac protocols
    echo(f"The condition is: {condition["name"]}")

    echo(f"\nSigns & Symptoms:")
    for symptom in condition["symptoms"]:
        note = ""
        if "vitals" in symptom:
            note = "(expressed via vitals)"
        if symptom in unselected_symptoms:  # note: should come after vitals check to overwrite it
            note = "(not present for this patient)"
        echo(f"- {symptom["name"]} {note}")
    
    echo(f"\nTreatments:")
    for treatment in condition["treatments"]:
        echo(f"- {treatment}")

    if "evacuation_guidelines" in condition:
        echo(f"\nEvacuation guidelines:")
        for guideline in condition["evacuation_guidelines"]:
            echo(f"- {guideline}")


if __name__ == "__main__":
    main()