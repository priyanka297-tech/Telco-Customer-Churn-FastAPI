import streamlit as st

def app():

    # ---------------------------------------------------
    # Custom CSS
    # ---------------------------------------------------

    st.markdown("""
    <style>

    .main{
    background-color:#F8FAFC;
    }

    .title{
    font-size:42px;
    font-weight:bold;
    text-align:center;
    padding:15px;
    border-radius:12px;
    background:linear-gradient(90deg,#2563EB,#0EA5E9,#06B6D4);
    color:white;
    }

    .card{
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.08);
    margin-bottom:15px;
    }

    h3{
    color:#2563EB;
    }

    </style>
    """, unsafe_allow_html=True)
    
    st.divider()

    # ---------------------------------------------------
    # Header
    # ---------------------------------------------------

    st.markdown("""
    <div class="title">
    👩‍💻 About the Developer
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------
    # Profile
    # ---------------------------------------------------

    left, right = st.columns([1,2])

    with left:

        st.image(
            "assets/formal image.png",
            width=200,
        )

    with right:

        st.markdown("""
    ## Priyanka Pal

    **AI Engineer | Data Scientist | Machine Learning Engineer**

    Passionate about solving real-world business problems using
    Artificial Intelligence, Machine Learning, Deep Learning,
    Natural Language Processing, and Generative AI.

    Experienced in developing predictive models, interactive
    dashboards, recommendation systems, NLP applications,
    and deploying AI solutions using Streamlit.

    """)

    st.divider()

    # ---------------------------------------------------
    # Education
    # ---------------------------------------------------

    st.subheader("🎓 Education")

    st.info("""
    **Bachelor of Technology (B.Tech)**

    Computer Science & Design

    World College of Technology & Management

    CGPA: **9**
    """)

    # ---------------------------------------------------
    # Skills
    # ---------------------------------------------------

    st.subheader("🛠 Technical Skills")

    col1,col2,col3 = st.columns(3)

    with col1:

        st.success("""
    ### Programming

    ✔ Python

    ✔ SQL

    ✔ C++

    ✔ HTML

    ✔ CSS
    """)

    with col2:

        st.success("""
    ### Data Science

    ✔ Pandas

    ✔ NumPy

    ✔ Scikit-Learn

    ✔ TensorFlow

    ✔ Machine Learning

    ✔ Deep Learning
    """)

    with col3:

        st.success("""
    ### Tools

    ✔ Streamlit

    ✔ Power BI

    ✔ GitHub

    ✔ VS Code

    ✔ Jupyter Notebook

    ✔ MySQL
    """)

    st.divider()

    # ---------------------------------------------------
    # Projects
    # ---------------------------------------------------

    st.subheader("🚀 Featured Projects")

    projects = [

    "📊 Telco Customer Churn Prediction Dashboard",

    "🛍 Customer Churn Prediction System",

    "🎬 Movie Recommendation System",

    "📝 Amazon Review Sentiment Analysis",

    "🏪 Rossmann Sales Forecasting Dashboard",

    "🤖 Multi-Agent AI Assistant",

    "📄 PDF Question Answering System (RAG)",

    "🌦 Weather & News AI Assistant"

    ]

    for project in projects:
        st.markdown(f"- {project}")

    st.divider()

    # ---------------------------------------------------
    # Certifications
    # ---------------------------------------------------

    st.subheader("📜 Certifications")

    certifications = [

    "IBM Data Science Professional",

    "Applied AI Training - Edunet Foundation",

    "Ducat Data Science Program",

    "Microsoft AI Workshop",

    "Intel AI & Machine Learning Workshop"

    ]

    for cert in certifications:
        st.markdown(f"✅ {cert}")

    st.divider()

    # ---------------------------------------------------
    # Achievements
    # ---------------------------------------------------

    st.subheader("🏆 Achievements")

    st.success("""
    🥇 First Prize – Inter College Hackathon

    🏅 Smart India Hackathon Participant

    🏅 Microsoft AI Tour Participant

    🏅 DLF Foundation Merit Scholarship

    🏅 Finalist – 24-Hour National Hackathon
    """)

    st.divider()

    # ---------------------------------------------------
    # Tech Stack Used
    # ---------------------------------------------------

    st.subheader("⚙ Tech Stack Used in this Project")

    stack = {
        "Technology":[
            "Python",
            "Streamlit",
            "Scikit-Learn",
            "Pandas",
            "NumPy",
            "Plotly",
            "Pickle"
        ],
        "Purpose":[
            "Programming",
            "Web Application",
            "Machine Learning",
            "Data Processing",
            "Numerical Computing",
            "Visualization",
            "Model Serialization"
        ]
    }

    st.table(stack)

    st.divider()

    # ---------------------------------------------------
    # Contact
    # ---------------------------------------------------

    st.subheader("📬 Connect With Me")

    st.markdown("""
    📧 **Email:** your_email@gmail.com

    💼 **LinkedIn:**  
    https://linkedin.com/in/your-profile

    💻 **GitHub:**  
    https://github.com/your-profile

    🌐 **Portfolio:**  
    https://your-portfolio.streamlit.app
    """)

    st.divider()

    # ---------------------------------------------------
    # Footer
    # ---------------------------------------------------

    st.markdown("""
    ---
    <center>

    ### ⭐ Thank you for visiting this project!

    This dashboard demonstrates an end-to-end Machine Learning pipeline,
    including data preprocessing, model training, evaluation,
    interactive visualization, and deployment using Streamlit.

    Built with ❤️ by **Priyanka Pal**

    </center>
    """, unsafe_allow_html=True)