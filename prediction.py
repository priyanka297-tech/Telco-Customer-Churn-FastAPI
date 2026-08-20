import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from api_client import ChurnAPIClient

API_BASE_URL = "http://127.0.0.1:8000"


def app():

    # Custom CSS

    st.markdown("""
    <style>

    .main{
    background-color:#F5F7FA;
    }

    .title{
    font-size:40px;
    font-weight:bold;
    text-align:center;
    padding:15px;
    border-radius:12px;
    background:linear-gradient(90deg,#2563eb,#0ea5e9,#06b6d4);
    color:white;
    }

    .block{
    padding:20px;
    border-radius:12px;
    background:white;
    box-shadow:0px 0px 15px rgba(0,0,0,0.1);
    margin-bottom:15px;
    }

    .metric{
    padding:15px;
    border-radius:12px;
    background:#ffffff;
    box-shadow:0px 0px 12px rgba(0,0,0,.08);
    text-align:center;
    }

    .predictButton button{
    width:100%;
    height:60px;
    font-size:22px;
    font-weight:bold;
    border-radius:10px;
    background:#2563eb;
    color:white;
    }

    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # API client — this page never touches the model, scaler, or the
    # pickle file directly. Every prediction goes over HTTP to the
    # FastAPI service, exactly like a web app, mobile app, or CRM would.
    # -----------------------------

    api_client = ChurnAPIClient(API_BASE_URL)

    # -----------------------------
    # Header
    # -----------------------------
    st.markdown("# 📊 Telco Customer Churn Prediction Dashboard")

    st.write(
        """
        Predict customer churn using a trained machine learning model,
        served via a FastAPI prediction service.
        """
        )

    if not api_client.is_reachable():
        st.error(
            f"⚠️ Cannot reach the prediction API at `{API_BASE_URL}`.\n\n"
            "Start it in a separate terminal with:\n\n"
            "```bash\nuvicorn api:app --reload --port 8000\n```"
        )
        st.stop()

    # -----------------------------
    # KPI Cards (pulled from the API, not hardcoded)
    # -----------------------------

    try:
        info = api_client.model_info()
    except Exception as exc:
        st.error(f"Failed to load model info from API: {exc}")
        st.stop()

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Test Samples", info.get("test_set_size", "-"))
    c2.metric("Features", info.get("n_features", "-"))
    c3.metric("Model", info.get("algorithm", "-"))

    try:
        acc = api_client.metrics().get("accuracy")
        c4.metric("Accuracy", f"{acc*100:.1f}%" if acc is not None else "-")
    except Exception:
        c4.metric("Accuracy", "-")

    st.divider()

    # -----------------------------
    # Customer Details
    # -----------------------------

    left,right = st.columns(2)

    with left:

        st.subheader("👤 Customer Information")

        gender = st.selectbox(
            "Gender",
            ["Female","Male"]
        )

        senior = st.selectbox(
            "Senior Citizen",
            [0,1]
        )

        partner = st.selectbox(
            "Partner",
            ["Yes","No"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes","No"]
        )

        tenure = st.slider(
            "Tenure",
            0,
            72,
            12
        )

        phone = st.selectbox(
            "Phone Service",
            ["Yes","No"]
        )

        multiple = st.selectbox(
            "Multiple Lines",
            ["No","Yes","No phone service"]
        )

        internet = st.selectbox(
            "Internet Service",
            ["DSL","Fiber optic","No"]
        )

    with right:

        st.subheader("💳 Service & Billing")

        online_security = st.selectbox(
            "Online Security",
            ["No","Yes","No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["No","Yes","No internet service"]
        )

        device = st.selectbox(
            "Device Protection",
            ["No","Yes","No internet service"]
        )

        support = st.selectbox(
            "Tech Support",
            ["No","Yes","No internet service"]
        )

        tv = st.selectbox(
            "Streaming TV",
            ["No","Yes","No internet service"]
        )

        movies = st.selectbox(
            "Streaming Movies",
            ["No","Yes","No internet service"]
        )

        contract = st.selectbox(
            "Contract",
            ["Month-to-month","One year","Two year"]
        )

        paperless = st.selectbox(
            "Paperless Billing",
            ["Yes","No"]
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    monthly = st.slider(
        "Monthly Charges",
        0.0,
        150.0,
        70.0
    )

    total = st.number_input(
        "Total Charges",
        value=1000.0
    )

    st.write("")

    # -----------------------------
    # Predict Button
    # -----------------------------

    st.markdown("<div class='predictButton'>",unsafe_allow_html=True)

    predict = st.button("🔍 Predict Churn")

    st.markdown("</div>",unsafe_allow_html=True)

    if predict:

        # Raw field values only — no encoding, no scaler, no model call
        # here. The API owns all of that.

        payload = {
            "gender": gender,
            "senior_citizen": senior,
            "partner": partner,
            "dependents": dependents,
            "tenure": tenure,
            "phone_service": phone,
            "multiple_lines": multiple,
            "internet_service": internet,
            "online_security": online_security,
            "online_backup": online_backup,
            "device_protection": device,
            "tech_support": support,
            "streaming_tv": tv,
            "streaming_movies": movies,
            "contract": contract,
            "paperless_billing": paperless,
            "payment_method": payment,
            "monthly_charges": monthly,
            "total_charges": total,
        }

        try:
            result = api_client.predict(payload)
        except Exception as exc:
            st.error(f"Prediction request to the API failed: {exc}")
            st.stop()

        prediction = result["churn_prediction"]
        probability = result["churn_probability"]
        risk_level = result["risk_level"]
        recommendation = result["recommendation"]

        st.divider()

        col1,col2 = st.columns([1,1])

        with col1:

            gauge = go.Figure(go.Indicator(

                mode="gauge+number",

                value=probability*100,

                title={'text':"Churn Probability"},

                gauge={

                    "axis":{"range":[0,100]},

                    "bar":{"color":"red"},

                    "steps":[

                        {"range":[0,30],"color":"green"},

                        {"range":[30,60],"color":"yellow"},

                        {"range":[60,100],"color":"red"}

                    ]

                }

            ))

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

        with col2:

            st.subheader("Prediction Result")

            if prediction==1:

                st.error("🔴 Customer is likely to Churn")

            else:

                st.success("🟢 Customer is likely to Stay")

            st.metric(
                "Churn Probability",
                f"{probability*100:.2f}%"
            )

            recommendation_md = "\n\n".join(f"• {item}" for item in recommendation)

            if risk_level == "Low":

                st.success("🟢 Low Risk")
                st.info(f"**Recommendation**\n\n{recommendation_md}")

            elif risk_level == "Medium":

                st.warning("🟡 Medium Risk")
                st.info(f"**Recommendation**\n\n{recommendation_md}")

            else:

                st.error("🔴 High Risk")
                st.info(f"**Recommendation**\n\n{recommendation_md}")

        st.divider()

        st.subheader("📋 Customer Summary")

        summary = pd.DataFrame({

            "Feature":[
                "Gender",
                "Senior Citizen",
                "Tenure",
                "Monthly Charges",
                "Total Charges",
                "Internet",
                "Contract"
            ],

            "Value":[
                gender,
                senior,
                tenure,
                monthly,
                total,
                internet,
                contract
            ]

        })

        st.dataframe(summary,use_container_width=True)
