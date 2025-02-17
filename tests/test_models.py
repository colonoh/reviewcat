from app.models import Condition, Patient, SEX, Symptom, SuperPatient, LEVEL_OF_RESPONSIVENESS, HEART_STRENGTH, HEART_RHYTHM



class TestPatient:
    def test_sex(self):
        c = Condition(name="Dummy",
                      description="",
                      sex=SEX.MALE,
                      symptoms=[Symptom(name="Dummy")],
                      treatments=[""],
                      evacuation_guidelines=[""])
        p = Patient(condition=c)
        assert p.sex == SEX.MALE.value

    def test_level_of_responsiveness(self):
        v = SuperPatient()
        assert v.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx4
        v.modify_vitals("level_of_responsiveness", "decrease")
        assert v.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx3

    def test_heart_rate(self):
        v = SuperPatient()
        assert v.heart_rate == 75
        v.modify_vitals("heart_rate", "decrease")
        assert v.heart_rate == 75*.8
        v.modify_vitals("heart_rate", "increase")
        assert v.heart_rate == 75*.8*1.2

    def test_heart_strength(self):
        v = SuperPatient()
        assert v.heart_strength == HEART_STRENGTH.STRONG
        v.modify_vitals("heart_strength", "set_weak")
        assert v.heart_strength == HEART_STRENGTH.WEAK

    def test_heart_rhythm(self):
        v = SuperPatient()
        assert v.heart_rhythm == HEART_RHYTHM.REGULAR
        v.modify_vitals("heart_rhythm", "set_irregular")
        assert v.heart_rhythm == HEART_RHYTHM.IRREGULAR
