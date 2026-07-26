import streamlit as st
import joblib
import pandas as pd
import os

st.set_page_config(page_title =  "Credit Risk Analyzer")
st.title("Loan credit Risk Analyzer")
st.write("Determine loan eligibility based on income and loan amount.")

model_path = os.path.join('models', 'credit_model.pkl')
if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error("Model not found! please run train.py first")
    st.stop()

st.sidebar.header("Applicant Details")
income = st.sidebar.number_input("Annual Income ($)",min_value = 5000,value = 50000,step = 1000)
loan_amount = st.sidebar.number_input("Requested loan Amount ($)" , min_value = 1000,value = 15000,step = 500)

if st.button("check Eligibility"):
    input_df = pd.DataFrame([[income,loan_amount]], columns = ['income','loan_amount'])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.divider()
    if prediction == 0:
        st.success("Result : SAFE")
        st.write(f"the model suggests this applicant is likely to repay.(Risk probability :{probability:.2f})")
    else:
        st.error("Result : RISKY")
        st.write(f"the model suggests a high risk of default. (Risk probability :{probability:.2f})")

with st.expander("how does this work?"):
    st.write(
        "this uses a **Logistics Regression** model.unlike linear regression which predicts a price ,this uses  a sigmoid function to calculate the probability of a 'yes/no' outcome."
    )