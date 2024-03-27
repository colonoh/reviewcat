from models import SEX, LEVEL_OF_RESPONSIVENESS, HEART_RATE, HEART_STRENGTH, HEART_RHYTHM, RESPIRATORY_RATE, \
RESPIRATORY_RHYTHM, RESPIRATORY_EFFORT, SKIN_COLOR, SKIN_TEMPERATURE, SKIN_MOISTURE, BODY_TEMPERATURE, PUPILS, \
BLOOD_PRESSURE, Symptom, Condition, Patient


# how to deal with: 
# - multiple of the same discomforts (e.g. discomfort in the neck, jaw, teeth, and/or back) (e.g. rapid, slow, and/or weak pulse)
# - mutually exclusive symptoms (e.g. rapid pulse, slow pulse)

conditions = [Condition(name="Angina",
                        description="Pain from diminished blood flow to the heart.",
                        symptoms=[Symptom(name="Nausea"), 
                                  Symptom(name="Discomfort in the neck"), 
                                  Symptom(name="Discomfort in the jaw"),
                                  Symptom(name="Discomfort in the teeth"), 
                                  Symptom(name="Discomfort in the back"), 
                                  Symptom(name="Shortness of breath"),
                                  Symptom(name="Stabbing pain"), 
                                  Symptom(name="Stomach (abdominal) pain"), 
                                  Symptom(name="Rapid pulse", vitals=[HEART_RATE.RAPID]), 
                                  Symptom(name="Slow pulse", vitals=[HEART_RATE.SLOW]), 
                                  Symptom(name="Weak pulse", vitals=[HEART_STRENGTH.WEAK]),  # shouldn't this also be seen in the blood pressure?
                                  Symptom(name="Irregular pulse", vitals=[HEART_RHYTHM.IRREGULAR]), 
                                  Symptom(name="Pale, cool, clammy skin", vitals=[SKIN_COLOR.PALE, SKIN_TEMPERATURE.COOL, SKIN_MOISTURE.CLAMMY])],
                        treatments=["Reduce anxiety and activity",
                                    "Administer oxygen",
                                    "Administer aspirin",
                                    "Evacuate"],
                        evacuation_guidelines=["Evacuate any patient with chest pain that is not clearly musculoskeletal, pulmonary, or gastrointestinal.",
                                               "Expedite evacuation for any patient with chest pain that does not relieve within 20 minutes."]),

              Condition(name="Shock (early stages)",
                        description="The inadequate perfusion of tissue with oxygenated blood, due to a failure of any or all of three basic components of the circulatory system - heart, blood vessels, and blood - to deliver oxygenated blood to the tissues.",
                        symptoms=[Symptom(name="Pale, cool, clammy skin", vitals=[SKIN_COLOR.PALE, SKIN_TEMPERATURE.COOL, SKIN_MOISTURE.CLAMMY]), 
                                  Symptom(name="Rapid pulse", vitals=[HEART_RATE.RAPID]), 
                                  Symptom(name="Slow pulse", vitals=[HEART_RATE.SLOW]),
                                  Symptom(name="Weak pulse", vitals=[HEART_STRENGTH.WEAK]),  # shouldn't this also be seen in the blood pressure?
                                  Symptom(name="Rapid respirations", vitals=[RESPIRATORY_RATE.RAPID]), 
                                  Symptom(name="Shallow respirations", vitals=[RESPIRATORY_EFFORT.SHALLOW]), 
                                  Symptom(name="Anxiety"), 
                                  Symptom(name="Restlessness"), 
                                  Symptom(name="Nausea"), 
                                  Symptom(name="Thirst")], 
                        treatments=["Maintain ABCs - airway, breathing, circulation",
                                    "Control bleeding, stabilize fractures",
                                    "Protect patient temperature within normal limits",
                                    "Elevate the legs",
                                    "Consider (giving) fluids"],
                        evacuation_guidelines=["Evacuate any patient whose vital signs do not stabilize or improve over time.",
                                               "Evacuate rapidly any patient with decreased mental status or deteriorating vital signs."])] 