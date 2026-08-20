import streamlit as st
import pandas as pd
import plotly.express as px

def app():

    # -----------------------------
    # Load Dataset
    # -----------------------------

    @st.cache_data
    def load_data():
        df = pd.read_csv("Telco-Customer-Churn.csv")

        df["TotalCharges"] = df["TotalCharges"].replace(" ", 0)
        df["TotalCharges"] = df["TotalCharges"].astype(float)

        return df


    df = load_data()

    # -----------------------------
    # Header
    # -----------------------------

    st.markdown("""
    # 📈 Dataset Insights

    Explore customer behavior and identify churn patterns.
    """)

    st.divider()

    # -----------------------------
    # Sidebar Filters
    # -----------------------------

    st.sidebar.header("Filters")

    contract = st.sidebar.multiselect(
        "Contract",
        df["Contract"].unique(),
        default=df["Contract"].unique()
    )

    internet = st.sidebar.multiselect(
        "Internet Service",
        df["InternetService"].unique(),
        default=df["InternetService"].unique()
    )

    gender = st.sidebar.multiselect(
        "Gender",
        df["gender"].unique(),
        default=df["gender"].unique()
    )

    filtered = df[
        (df["Contract"].isin(contract)) &
        (df["InternetService"].isin(internet)) &
        (df["gender"].isin(gender))
    ]

    # -----------------------------
    # KPI Cards
    # -----------------------------

    total = len(filtered)

    churn = filtered["Churn"].value_counts()["Yes"]

    stay = filtered["Churn"].value_counts()["No"]

    rate = churn / total * 100

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Total Customers", total)

    c2.metric("Churned", churn)

    c3.metric("Stayed", stay)

    c4.metric("Churn Rate", f"{rate:.2f}%")

    st.divider()

    # ==================================================
    # Row 1
    # ==================================================

    left,right = st.columns(2)

    with left:

        fig = px.pie(
            filtered,
            names="Churn",
            title="Customer Churn Distribution",
            hole=0.5
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.histogram(
            filtered,
            x="Contract",
            color="Churn",
            barmode="group",
            title="Churn by Contract Type"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # Row 2
    # ==================================================

    left,right = st.columns(2)

    with left:

        fig = px.box(
            filtered,
            x="Churn",
            y="MonthlyCharges",
            color="Churn",
            title="Monthly Charges vs Churn"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.box(
            filtered,
            x="Churn",
            y="tenure",
            color="Churn",
            title="Tenure vs Churn"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # Row 3
    # ==================================================

    left,right = st.columns(2)

    with left:

        fig = px.histogram(
            filtered,
            x="InternetService",
            color="Churn",
            title="Internet Service Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.histogram(
            filtered,
            x="PaymentMethod",
            color="Churn",
            title="Payment Method"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # Row 4
    # ==================================================

    fig = px.scatter(
        filtered,
        x="MonthlyCharges",
        y="TotalCharges",
        color="Churn",
        size="tenure",
        hover_data=["Contract","InternetService"],
        title="Monthly Charges vs Total Charges"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # Correlation Heatmap
    # ==================================================

    st.subheader("Correlation Heatmap")

    numeric = filtered.select_dtypes(include="number")

    corr = numeric.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="Blues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # Data Preview
    # ==================================================

    st.subheader("Dataset Preview")

    st.dataframe(
        filtered,
        use_container_width=True
    )

    # ==================================================
    # Download
    # ==================================================

    csv = filtered.to_csv(index=False).encode()

    st.download_button(
        "📥 Download Filtered Dataset",
        csv,
        file_name="filtered_telco_dataset.csv",
        mime="text/csv"
    )

    # ==================================================
    # Business Insights
    # ==================================================

    st.subheader("📊 Key Business Insights")

    st.info("""
    ### Key Observations

    • Customers with **Month-to-Month contracts** tend to churn more frequently.

    • **Fiber Optic** users generally exhibit a higher churn rate.

    • Customers with **shorter tenure** are more likely to leave.

    • Higher **Monthly Charges** are associated with increased churn risk.

    • Encouraging customers to switch to **One-Year or Two-Year contracts** can help reduce churn.
    """)