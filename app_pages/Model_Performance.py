import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from api_client import ChurnAPIClient

API_BASE_URL = "http://127.0.0.1:8000"


def app():

    # -------------------------------------------------------
    # API client — metrics, confusion matrix, feature list, etc. are
    # all fetched over HTTP from the FastAPI service. This page never
    # opens the pickle or imports sklearn.
    # -------------------------------------------------------

    api_client = ChurnAPIClient(API_BASE_URL)

    st.markdown("# 🤖 Model Performance Dashboard")

    st.write(
    """
    Evaluate the trained Logistic Regression model using multiple
    performance metrics and visualizations, served via the FastAPI
    prediction service.
    """
    )

    if not api_client.is_reachable():
        st.error(
            f"⚠️ Cannot reach the prediction API at `{API_BASE_URL}`.\n\n"
            "Start it in a separate terminal with:\n\n"
            "```bash\nuvicorn api:app --reload --port 8000\n```"
        )
        st.stop()

    try:
        metrics = api_client.metrics()
        info = api_client.model_info()
    except Exception as exc:
        st.error(f"Failed to load metrics from API: {exc}")
        st.stop()

    accuracy = metrics["accuracy"]
    precision = metrics["precision"]
    recall = metrics["recall"]
    f1 = metrics["f1_score"]
    roc_auc = metrics["roc_auc"]
    cm = np.array(metrics["confusion_matrix"])
    fpr = metrics["roc_curve"]["fpr"]
    tpr = metrics["roc_curve"]["tpr"]
    feature_columns = info["feature_columns"]

    try:
        importance_data = api_client.feature_importance()
        importance_df = pd.DataFrame(importance_data["items"]).rename(
            columns={"feature": "Feature", "importance": "Importance"}
        )
    except Exception:
        importance_df = None

    st.divider()

    # -------------------------------------------------------
    # KPI Cards
    # -------------------------------------------------------

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Accuracy",
        f"{accuracy*100:.2f}%"
    )

    c2.metric(
        "Precision",
        f"{precision*100:.2f}%"
    )

    c3.metric(
        "Recall",
        f"{recall*100:.2f}%"
    )

    c4.metric(
        "F1 Score",
        f"{f1*100:.2f}%"
    )

    st.divider()

    # ==========================================================
    # Confusion Matrix
    # ==========================================================

    left,right = st.columns(2)

    with left:

        st.subheader("Confusion Matrix")

        fig = px.imshow(
            cm,
            text_auto=True,
            color_continuous_scale="Blues",
            labels=dict(
                x="Predicted",
                y="Actual"
            ),
            x=["No Churn","Churn"],
            y=["No Churn","Churn"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==========================================================
    # ROC Curve
    # ==========================================================

    with right:

        st.subheader("ROC Curve")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=fpr,
                y=tpr,
                mode="lines",
                name=f"AUC = {roc_auc:.3f}"
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[0,1],
                y=[0,1],
                mode="lines",
                name="Random",
                line=dict(dash="dash")
            )
        )

        fig.update_layout(
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==========================================================
    # Metrics Bar Chart
    # ==========================================================

    st.subheader("Evaluation Metrics")

    metrics_df = pd.DataFrame({

        "Metric":[
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score"
        ],

        "Score":[
            accuracy,
            precision,
            recall,
            f1
        ]

    })

    fig = px.bar(
        metrics_df,
        x="Metric",
        y="Score",
        text="Score",
        color="Metric"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================================
    # Feature Importance
    # ==========================================================

    st.subheader("Feature Importance")

    if importance_df is not None:

        fig = px.bar(
            importance_df.head(15),
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("Feature importance isn't available for this model type.")

    # ==========================================================
    # Classification Report
    # ==========================================================

    st.subheader("Classification Report")

    try:
        report = api_client.classification_report()["report"]
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df, use_container_width=True)
    except Exception as exc:
        st.info(f"Classification report unavailable: {exc}")

    # ==========================================================
    # Model Summary
    # ==========================================================

    st.subheader("Model Summary")

    summary = pd.DataFrame({

        "Property":[
            "Algorithm",
            "Testing Samples",
            "Total Features",
            "Prediction Type"
        ],

        "Value":[
            info["algorithm"],
            info["test_set_size"],
            info["n_features"],
            "Binary Classification"
        ]

    })

    st.table(summary)

    # ==========================================================
    # Strengths & Limitations
    # ==========================================================

    col1,col2 = st.columns(2)

    with col1:

        st.success("""
    ### Strengths

    ✔ Fast Training

    ✔ Highly Interpretable

    ✔ Low Memory Usage

    ✔ Probability Output

    ✔ Good Baseline Model
    """)

    with col2:

        st.warning("""
    ### Limitations

    ⚠ Linear Decision Boundary

    ⚠ Sensitive to Outliers

    ⚠ Requires Feature Scaling

    ⚠ Limited for Complex Relationships
    """)

    # ==========================================================
    # Business Recommendation
    # ==========================================================

    st.subheader("Business Recommendation")

    st.info("""
    ### Recommended Customer Retention Strategy

    • Focus on customers with predicted probability > 60%.

    • Convert Month-to-Month contracts into Annual contracts.

    • Offer loyalty discounts to high-risk customers.

    • Improve customer support for Fiber Optic users.

    • Regularly retrain the model with updated customer data.

    • Integrate this model into the CRM system for real-time churn alerts.
    """)
