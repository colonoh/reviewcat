from app.models import Condition, Patient, SEX, Symptom



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
