import streamlit as st

def app():
    
    # -------------------------------------------------------
    # Custom CSS
    # -------------------------------------------------------

    st.markdown("""
    <style>

    .main{
        background-color:#F5F7FA;
    }

    .hero{
        background:linear-gradient(135deg,#2563EB,#0891B2,#06B6D4);
        padding:35px;
        border-radius:15px;
        color:white;
        text-align:center;
    }

    .feature{
        background:white;
        padding:20px;
        border-radius:12px;
        box-shadow:0px 5px 12px rgba(0,0,0,0.08);
        text-align:center;
    }

    .footer{
        text-align:center;
        color:gray;
        font-size:15px;
    }

    </style>
    """, unsafe_allow_html=True)
    
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
        # Header
        # -----------------------------
    
    st.markdown(
    """
        <div class='title'>
        👩‍💻 Telco Customer Churn Prediction Dashboard
        </div>
        """,
    unsafe_allow_html=True
        )
    
    st.write("")
    
    # -------------------------------------------------------
    # KPI Cards
    # -------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Dataset", "7043 Customers")
    c2.metric("Algorithm", "Logistic Regression")
    c3.metric("Features", "19")
    c4.metric("Accuracy", "82%")

    st.write("")

    # -------------------------------------------------------
    # Dashboard Overview
    # -------------------------------------------------------

    st.header("📌 Dashboard Overview")

    col1, col2 = st.columns([2,1])

    with col1:

        st.write("""
    This application demonstrates a complete **Machine Learning Pipeline**
    for predicting customer churn in the telecom industry.

    ### The dashboard includes:

    - 📊 Customer Churn Prediction

    - 📈 Interactive Dataset Analysis

    - 🤖 Machine Learning Performance Evaluation

    - 📉 Visual Business Insights

    - 💼 Developer Portfolio

    The model predicts whether a customer is likely to **Stay**
    or **Churn**, enabling businesses to proactively retain valuable customers.
    """)

    with col2:

        st.info("""
    ### Model Details

    **Algorithm**

    Logistic Regression

    **Problem Type**

    Binary Classification

    **Scaling**

    StandardScaler

    **Deployment**

    Streamlit

    **Language**

    Python
    """)

    st.divider()

    # -------------------------------------------------------
    # Dashboard Modules
    # -------------------------------------------------------

    st.header("🚀 Dashboard Modules")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
    ### 📊 Prediction

    ✔ Predict customer churn

    ✔ Risk Score

    ✔ Probability Gauge

    ✔ Business Recommendation
    """)

        st.markdown("""
    ### 📈 Dataset Insights

    ✔ Interactive Charts

    ✔ Customer Analysis

    ✔ Churn Trends

    ✔ Download Dataset
    """)

    with col2:

        st.markdown("""
    ### 🤖 Model Performance

    ✔ Accuracy

    ✔ Confusion Matrix

    ✔ ROC Curve

    ✔ Feature Importance
    """)

        st.markdown("""
    ### 👩‍💻 About Developer

    ✔ Skills

    ✔ Projects

    ✔ Certifications

    ✔ Contact Information
    """)

    st.divider()

    # -------------------------------------------------------
    # Machine Learning Workflow
    # -------------------------------------------------------

    st.header("⚙️ Machine Learning Workflow")

    st.markdown("""
    ```text
    Raw Customer Data
            │
            ▼
    Data Cleaning
            │
            ▼
    Feature Engineering
            │
            ▼
    Feature Scaling
            │
            ▼
    Model Training
            │
            ▼
    Prediction
            │
            ▼
    Business Recommendation """)

    st.markdown("---")

    st.success("""
    ### Navigation

    ➡ Home

    ➡ Prediction

    ➡ Dataset Insights

    ➡ Model Performance

    ➡ About Developer
    """)

    st.markdown("---")

    st.info("""
    **Machine Learning Model**

    ✔ Logistic Regression

    ✔ Binary Classification

    ✔ Customer Churn Prediction
    """)