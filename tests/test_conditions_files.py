import yaml


class TestWFRConditions:
    def test_all_condition_symptoms_in_global_symptoms(self):
        with open("src/app/wfr_conditions.yaml", "r") as f:
            data = yaml.safe_load(f)
            global_symptoms = data["symptoms"]
            conditions = data["conditions"]

            for condition, details in conditions.items():
                for local_symptom in details["symptoms"]:
                    if local_symptom not in global_symptoms:
                        raise ValueError(f"{condition=} has symptom {local_symptom=} but it is not present in the global symptoms")

    def test_all_symptoms_vitals_handled(self):
        with open("src/app/wfr_conditions.yaml", "r") as f:
            data = yaml.safe_load(f)
            global_symptoms = data["symptoms"]
            # TODO
