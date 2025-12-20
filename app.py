import streamlit as st
import numpy as np
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="VYNOX | Placement Readiness", layout="wide")

# ---------------- LOAD MODEL ----------------
clf = joblib.load("placement_model.pkl")
le_dsa = joblib.load("le_dsa.pkl")
le_major = joblib.load("le_major.pkl")
le_github = joblib.load("le_github.pkl")
le_domain = joblib.load("le_domain.pkl")
le_target = joblib.load("le_target.pkl")

# ---------------- FUNCTIONS ----------------
def predict_level(profile):
    dsa = le_dsa.transform([profile['dsa_level']])[0]
    major = le_major.transform([profile['major_project']])[0]
    github = le_github.transform([profile['github_quality']])[0]
    domain = le_domain.transform([profile['domain_focus']])[0]

    X = np.array([
        dsa,
        profile['problem_count'],
        profile['language_count'],
        profile['cs_fundamentals'],
        profile['project_count'],
        major,
        github,
        domain,
        profile['communication'],
        profile['resume_quality'],
        profile['mock_interviews'],
        profile['learning_consistency'],
        profile['self_awareness']
    ]).reshape(1, -1)

    pred = clf.predict(X)[0]
    score = int(np.max(clf.predict_proba(X)) * 100)
    level = le_target.inverse_transform([pred])[0]
    return level, score


def recommendations(level, domain):
    if level == "Beginner":
        return [
            "Learn programming fundamentals (Python / Java)",
            "Start DSA basics",
            "Study OS, DBMS, CN fundamentals",
            "Practice 5 DSA problems daily"
        ]
    elif level == "Intermediate":
        projects = {
            "Web": "Job Portal / Portfolio Website",
            "ML": "Student Placement Prediction System",
            "Data": "Student Performance Analysis",
            "Core": "CPU Scheduling Simulator"
        }
        return [
            f"Focus on {domain} domain",
            projects[domain],
            "Improve GitHub and Resume",
            "Start mock interviews"
        ]
    else:
        advanced = {
            "Web": "Full Stack E-commerce Platform",
            "ML": "AI Interview Bot / Recommendation System",
            "Data": "Predictive Analytics System",
            "Core": "OS Performance Optimization"
        }
        return [
            advanced[domain],
            "Company-specific interview preparation",
            "System design practice",
            "Apply for internships & jobs"
        ]

# ---------------- SIDEBAR MENU ----------------
st.sidebar.image("assets/vynox_logo.png", width=120)
menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "👤 Create Profile", "📊 Placement Readiness", "💡 Guidance", "ℹ️ About VYNOX"]
)

# ---------------- HOME PAGE ----------------
if menu == "🏠 Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("assets/vynox_logo.png", width=220)
    with col2:
        st.title("VYNOX")
        st.subheader("A Product-Based Company")
        st.write(
            """
            **VYNOX** is a product-based company focused on empowering students 
            with AI-driven career and placement guidance.

            Our platform analyzes student skills, predicts placement readiness,
            and provides personalized learning, project, and job recommendations.
            """
        )

# ---------------- PROFILE PAGE ----------------
elif menu == "👤 Create Profile":
    st.header("Student Profile")

    with st.form("profile_form"):
        dsa_level = st.selectbox("DSA Level", ["Beginner", "Intermediate", "Advanced"])
        problem_count = st.number_input("Problems Solved", 0, 1000)
        language_count = st.number_input("Languages Known", 1, 10)
        cs_fundamentals = st.slider("CS Fundamentals (1-5)", 1, 5)
        project_count = st.number_input("Projects Completed", 0, 10)
        major_project = st.selectbox("Major Project Completed?", ["No", "Yes"])
        github_quality = st.selectbox("GitHub Quality", ["Low", "Medium", "High"])
        domain_focus = st.selectbox("Domain Focus", ["Web", "ML", "Data", "Core"])
        communication = st.slider("Communication Skills (1-5)", 1, 5)
        resume_quality = st.slider("Resume Quality (1-5)", 1, 5)
        mock_interviews = st.number_input("Mock Interviews Attended", 0, 20)
        learning_consistency = st.slider("Learning Consistency (1-5)", 1, 5)
        self_awareness = st.slider("Self Awareness (1-5)", 1, 5)

        submit = st.form_submit_button("Save Profile")

        if submit:
            st.session_state.profile = {
                "dsa_level": dsa_level,
                "problem_count": problem_count,
                "language_count": language_count,
                "cs_fundamentals": cs_fundamentals,
                "project_count": project_count,
                "major_project": major_project,
                "github_quality": github_quality,
                "domain_focus": domain_focus,
                "communication": communication,
                "resume_quality": resume_quality,
                "mock_interviews": mock_interviews,
                "learning_consistency": learning_consistency,
                "self_awareness": self_awareness
            }
            st.success("Profile saved successfully")

# ---------------- PLACEMENT READINESS ----------------
elif menu == "📊 Placement Readiness":
    if "profile" not in st.session_state:
        st.warning("Please create your profile first")
    else:
        level, score = predict_level(st.session_state.profile)
        st.header("Placement Readiness Result")
        st.subheader(f"Level: {level}")
        st.progress(score)
        st.write(f"Readiness Score: {score}%")

# ---------------- GUIDANCE ----------------
elif menu == "💡 Guidance":
    if "profile" not in st.session_state:
        st.warning("Please create your profile first")
    else:
        level, _ = predict_level(st.session_state.profile)
        st.header("Personalized Guidance")
        for r in recommendations(level, st.session_state.profile["domain_focus"]):
            st.write("✔️", r)

# ---------------- ABOUT ----------------
elif menu == "ℹ️ About VYNOX":
    st.header("About VYNOX")
    st.write("**VYNOX** is a product-based company building intelligent career solutions for students.")

    st.subheader("👥 Team Members")
    st.write("- **Swathika** – Team Lead")
    st.write("- **Vishwa** – Tech Lead")
    st.write("- **Santhosh** – Designer")

