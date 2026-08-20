import streamlit as st
from streamlit_option_menu import option_menu

# Import pages
from prediction import app as prediction_app
from app_pages.Data_Insights import app as data_insights_app
from app_pages.Model_Performance import app as model_performance_app
from app_pages.about import app as about_app
from app_pages.Home import app as home_app
from app_pages.Retention_Assistant import app as retention_assistant_app

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:
    
    st.image(
        "assets/image_2.png",
        width=260,
    )

    selected = option_menu(

        menu_title="",

        options=[
            "Home",
            "Data Insights",
            "Prediction",
            "AI Retention Assistant",
            "Model Performance",
            "About"
        ],

        icons=[
            "house",
            "table",
            "robot",
            "chat-dots",
            "graph-up",
            "info-circle"
        ],

       

        default_index=0,

        styles={
            "container":{
                "padding":"5!important",
                "background-color":"#fafafa"
            },

            "icon":{
                "color":"orange",
                "font-size":"18px"
            },

            "nav-link":{
                "font-size":"16px",
                "text-align":"left",
                "margin":"0px",
                "--hover-color":"#eee"
            },

            "nav-link-selected":{
                "background-color":"#1565C0"
            }
        }
    )


# ----------------------------------------------------
# Routing
# ----------------------------------------------------

if selected=="Home":
    home_app()

elif selected=="Data Insights":
    data_insights_app()

elif selected=="Prediction":
    prediction_app()
    
elif selected=="AI Retention Assistant":
    retention_assistant_app()

elif selected=="Model Performance":
    model_performance_app()

elif selected=="About":
    about_app()

    
