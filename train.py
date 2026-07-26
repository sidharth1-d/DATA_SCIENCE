import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = {
    'age' : [18,22,35,45,50,19,33,60,25,40],
    'bmi' : [22.5,28.1,25.0,32.2,29.5,20.1,38.0,27.0,24.0,30.0],
    'smoker' : [0,0,1,0,1,0,1,0,0,1],
    'premium' : [12000,14000,25000,22000,35000,11000,32000,28000,15000,29000]
}

df = pd.DataFrame(data)
x = df[['age','bmi','smoker']]
y = df['premium']

model = LinearRegression()
model.fit(x,y)

joblib.dump(model,'healthcare_model.pkl')

print("step 1 success : Model trained and saved as 'healthcare_model.pkl'!")