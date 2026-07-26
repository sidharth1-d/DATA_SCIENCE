import joblib
import pandas as pd

model = joblib.load('healthcare_model.pkl')

def get_prediction(age , bmi , smoker_text):
    smoker = 1 if smoker_text.lower() == 'yes' else 0

    input_data = pd.DataFrame([[age , bmi , smoker]],
                              columns = ['age' , 'bmi' , 'smoker'])

    prediction = model.predict(input_data)
    return prediction[0]

result = get_prediction(age = 30 ,bmi = 25.0 , smoker_text = 'no')
print(f"step 2 success : the loaded model predicted a premium of ${result:.2f}")