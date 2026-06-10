import streamlit as st
import requests

API_URL = "https://loan-api-5xvs.onrender.com"

st.set_page_config(page_title="Loan Approval Predictor",page_icon="🏦",layout="centered")

st.title("🏦 AI Loan Approval Assistant")

st.markdown("""Fill in the applicant details below and click **Predict**.""")

with st.form("loan_form"):

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    married = st.selectbox(
        "Married",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["0", "1", "2", "3+"]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )

    applicant_income = st.number_input(
        "Applicant Income (Monthly)",
        min_value=0.0
    )

    coapplicant_income = st.number_input(
        "Coapplicant Income (Monthly)",
        min_value=0.0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0.0
    )

    loan_term = st.selectbox(
        "Loan Term (Months)",
        [60, 120, 180, 240, 300, 360]
    )

    credit_history = st.selectbox(
        "Credit History",
        [1, 0],
        format_func=lambda x:
            "Good (1)" if x == 1 else "Poor (0)"
    )

    property_area = st.selectbox(
        "Property Area",
        ["Urban", "Semiurban", "Rural"]
    )

    submit = st.form_submit_button("Predict")

if submit:

    payload = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    try:

        with st.spinner("Analyzing loan application..."):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=30
            )

        result = response.json()

        approved = result["loan_approved"]
        approval_prob = result["approved_probability"]
        rejection_prob = result["rejected_probability"]

        st.divider()

        st.subheader("Prediction Result")

        if approved == 1:
            st.success("✅ Loan Approved")
        else:
            st.error("❌ Loan Rejected")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Approval Probability",
                f"{approval_prob*100:.2f}%"
            )

        with col2:
            st.metric(
                "Rejection Probability",
                f"{rejection_prob*100:.2f}%"
            )

    except Exception as e:
        st.error(f"API Error: {e}")