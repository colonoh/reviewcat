from enum import Enum, IntEnum


class SEX(Enum):
    ANY = "any"
    FEMALE = "female"
    MALE = "male"

class FREQUENCY(IntEnum):  # perecent, where 100 = 100%
    RARELY: float = 20
    SOMETIMES: float = 50
    OFTEN: float = 80
    DEFAULT: float = 90
    ALWAYS: float = 100

class LEVEL_OF_RESPONSIVENESS(Enum):
    AOx4 = "A&Ox4"
    AOx3 = "A&Ox3"
    AOx2 = "A&Ox2"
    AOx1 = "A&Ox1"
    # TODO: V, P, U

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

class SKIN_MOISTURE(Enum):
    DRY = "dry"
    WET = "wet"
    CLAMMY = "clammy"

class BODY_TEMPERATURE(Enum):  # degF
    NORMAL = 98.6
    HOT = 102.0  # TODO
    COLD = 96.0  # TODO

class PUPILS(Enum):
    PERRL = "equal, round, and reactive to light"

class BLOOD_PRESSURE(Enum):
    NORMAL = "a strong radial pulse"
    WEAK = "no detectable radial pulse"
