import streamlit as st


# -------------------------------------------------------
# AI RETENTION ASSISTANT
# -------------------------------------------------------

def app():

    st.title("🤖 AI Customer Retention Assistant")

    st.markdown(
        """
        Use AI-powered recommendations to identify suitable
        retention actions for customers at high risk of churn.
        """
    )

    st.divider()

    # ---------------------------------------------------
    # Customer Information
    # ---------------------------------------------------

    st.subheader("👤 Customer Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        customer_id = st.text_input(
            "Customer ID",
            value="10045"
        )

        churn_probability = st.slider(
            "Churn Probability (%)",
            min_value=0,
            max_value=100,
            value=87
        )

    with col2:
        contract = st.selectbox(
            "Contract Type",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        tenure = st.number_input(
            "Tenure (Months)",
            min_value=0,
            max_value=120,
            value=8
        )

    with col3:
        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=1200.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=9600.0
        )

    st.divider()

    # ---------------------------------------------------
    # Risk Classification
    # ---------------------------------------------------

    if churn_probability >= 75:
        risk_level = "HIGH"
        risk_icon = "🔴"

    elif churn_probability >= 50:
        risk_level = "MEDIUM"
        risk_icon = "🟠"

    else:
        risk_level = "LOW"
        risk_icon = "🟢"

    st.subheader("📊 Churn Risk")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Churn Probability",
            f"{churn_probability}%"
        )

    with col2:
        st.metric(
            "Risk Level",
            f"{risk_icon} {risk_level}"
        )

    with col3:
        st.metric(
            "Customer Tenure",
            f"{tenure} months"
        )

    # ---------------------------------------------------
    # Recommendation Engine
    # ---------------------------------------------------

    def generate_recommendation():

        recommendations = []
        reasons = []

        # High churn risk
        if churn_probability >= 75:
            reasons.append(
                "Customer has a high predicted probability of churn."
            )

        # Contract
        if contract == "Month-to-month":
            recommendations.append(
                "Offer a 12-month or longer-term contract."
            )

            reasons.append(
                "Customer is currently on a month-to-month contract."
            )

        # Monthly charges
        if monthly_charges >= 1000:
            recommendations.append(
                "Provide a targeted pricing incentive."
            )

            reasons.append(
                "Monthly charges are relatively high."
            )

        # Tenure
        if tenure < 12:
            recommendations.append(
                "Provide a loyalty incentive for contract renewal."
            )

            reasons.append(
                "Customer has relatively short tenure."
            )

        # Default recommendation
        if not recommendations:
            recommendations.append(
                "Offer personalized customer support and loyalty benefits."
            )

        return recommendations, reasons

    # ---------------------------------------------------
    # Generate AI Recommendation
    # ---------------------------------------------------

    if st.button(
        "🤖 Generate Retention Recommendation",
        use_container_width=True
    ):

        recommendations, reasons = generate_recommendation()

        st.session_state["recommendations"] = recommendations
        st.session_state["reasons"] = reasons

    # ---------------------------------------------------
    # Display Recommendation
    # ---------------------------------------------------

    if "recommendations" in st.session_state:

        st.divider()

        st.subheader("💡 AI Retention Recommendation")

        if risk_level == "HIGH":
            st.warning(
                f"Customer **{customer_id}** requires immediate retention attention."
            )

        for recommendation in st.session_state["recommendations"]:
            st.write(f"✅ {recommendation}")

        st.subheader("🔍 Why This Recommendation?")

        for reason in st.session_state["reasons"]:
            st.write(f"• {reason}")

        # ------------------------------------------------
        # Targeted Offer
        # ------------------------------------------------

        st.subheader("🎯 Recommended Offer")

        if contract == "Month-to-month" and monthly_charges >= 1000:

            offer = (
                "Offer a 12-month contract with a targeted "
                "10% discount for the next 3 months."
            )

        elif contract == "Month-to-month":

            offer = (
                "Offer a 12-month contract with a personalized "
                "loyalty incentive."
            )

        elif monthly_charges >= 1000:

            offer = (
                "Offer a personalized pricing incentive "
                "to reduce price-related churn risk."
            )

        else:

            offer = (
                "Offer loyalty benefits and proactive "
                "customer support."
            )

        st.info(offer)

        # ------------------------------------------------
        # Customer Message
        # ------------------------------------------------

        st.subheader("📩 Suggested Customer Message")

        message = f"""
Dear Customer,

We value your continued partnership with us.

We would like to offer you an exclusive opportunity to
move to a longer-term plan with a personalized pricing
benefit.

This offer is designed to provide you with greater value
and flexibility while rewarding your continued loyalty.

Thank you for being a valued customer.
"""

        st.text_area(
            "AI Generated Message",
            value=message,
            height=180
        )

    # ---------------------------------------------------
    # Chatbot
    # ---------------------------------------------------

    st.divider()

    st.subheader("💬 Ask the Retention Assistant")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(message)

    user_question = st.chat_input(
        "Ask about this customer's retention strategy..."
    )

    if user_question:

        st.session_state.chat_history.append(
            ("user", user_question)
        )

        question = user_question.lower()

        # -----------------------------------------------
        # Simple AI response engine
        # -----------------------------------------------

        if "why" in question and "churn" in question:

            response = (
                f"The customer has a {churn_probability}% churn "
                f"probability and is classified as {risk_level} risk. "
                f"Key factors include the {contract.lower()} contract, "
                f"{tenure} months of tenure, and monthly charges of "
                f"{monthly_charges:.2f}."
            )

        elif "recommend" in question or "action" in question:

            recommendations, _ = generate_recommendation()

            response = (
                "Recommended retention actions:\n\n"
                + "\n".join(
                    f"• {item}"
                    for item in recommendations
                )
            )

        elif "offer" in question:

            response = (
                "The recommended offer is a targeted long-term "
                "contract incentive. For this customer, consider "
                "a 12-month contract with a temporary pricing benefit."
            )

        elif "message" in question:

            response = (
                "Suggested message: "
                "\"We value your continued partnership. "
                "We're offering you an exclusive long-term plan "
                "with a personalized pricing benefit.\""
            )

        else:

            response = (
                "Based on the customer's churn risk, I recommend "
                "focusing on contract renewal, personalized pricing, "
                "and proactive customer engagement."
            )

        st.session_state.chat_history.append(
            ("assistant", response)
        )

        st.rerun()