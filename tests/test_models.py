from app.models import *


class TestVitals:
    def test_level_of_responsiveness(self):
        p = SuperPatient()
        assert p.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx4
        p.modify_vitals("level_of_responsiveness", "decrease")
        assert p.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx3
        p.modify_vitals("level_of_responsiveness", "decrease")
        p.modify_vitals("level_of_responsiveness", "decrease")
        p.modify_vitals("level_of_responsiveness", "decrease")
        p.modify_vitals("level_of_responsiveness", "decrease")
        p.modify_vitals("level_of_responsiveness", "decrease")
        assert p.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.UNRESPONSIVE
        p.modify_vitals("level_of_responsiveness", "decrease")
        assert p.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.UNRESPONSIVE
        assert str(p.level_of_responsiveness) == "unresponsive"


class TestPatient:
    def test_level_of_responsiveness(self):
        v = SuperPatient()
        assert v.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx4
        v.modify_vitals("level_of_responsiveness", "decrease")
        assert v.level_of_responsiveness == LEVEL_OF_RESPONSIVENESS.AOx3

    def test_pick_condition(self):
        v = SuperPatient()
        assert v.condition_name == None
        v.pick_condition()
        assert v.condition_name != None
                

    def test_heart_rate(self):
        v = SuperPatient()
    #     v.modify_vitals("heart_rate", "decrease")
    #     assert v.heart_rate == 75*.8
    #     v.modify_vitals("heart_rate", "increase")
    #     assert v.heart_rate == 75*.8*1.2

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
