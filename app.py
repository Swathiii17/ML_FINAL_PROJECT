import streamlit as st
import numpy as np
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="VYNOX", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "profile" not in st.session_state:
    st.session_state.profile = None
# ---------------- LANDING PAGE ----------------
if st.session_state.page == "landing":

    st.markdown("""
    <style>
    .hero {
        position: relative;
        width: 100%;
        height: 90vh;
        background-image: url("assets/landing.png");
        background-size: cover;
        background-position: center;
        border-radius: 12px;
    }

    .hero-button {
        position: absolute;
        top: 40%;
        right: 15%;
    }

    .hero-button button {
        font-size: 20px;
        padding: 14px 40px;
        border-radius: 50px;
        border: 2px solid white;
        background: rgba(0,0,0,0.3);
        color: white;
        cursor: pointer;
    }

    .hero-button button:hover {
        background: rgba(255,255,255,0.2);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # HERO SECTION
    st.markdown("""
    <div class="hero">
        <div class="hero-button">
            <form method="post">
                <button name="join">Join Us !!</button>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CLICK HANDLER
    if "join" in st.session_state:
        st.session_state.page = "main"
        st.rerun()

    # fallback click (Streamlit limitation workaround)
    if st.button("hidden_join", key="hidden_join", help=""):
        st.session_state.page = "main"
        st.rerun()


# ---------------- LOAD MODEL ----------------
clf = joblib.load("placement_model.pkl")
le_dsa = joblib.load("le_dsa.pkl")
le_major = joblib.load("le_major.pkl")
le_github = joblib.load("le_github.pkl")
le_domain = joblib.load("le_domain.pkl")
le_target = joblib.load("le_target.pkl")

# ---------------- LOAD DATASETS ----------------
courses_df = pd.read_csv("courses.csv")
jobs_df = pd.read_csv("jobs.csv")

# ---------------- FUNCTIONS ----------------
def predict_level(profile):
    X = np.array([
        le_dsa.transform([profile['dsa_level']])[0],
        profile['problem_count'],
        profile['language_count'],
        profile['cs_fundamentals'],
        profile['project_count'],
        le_major.transform([profile['major_project']])[0],
        le_github.transform([profile['github_quality']])[0],
        le_domain.transform([profile['domain_focus']])[0],
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


def recommend_courses(level):
    return courses_df[courses_df["level"] == level]


def recommend_jobs(level):
    return jobs_df[jobs_df["required_level"] == level]


# ---------------- MAIN APP ----------------
# ---------------- MAIN APP ----------------
if st.session_state.page == "main":

    user_name = (
        st.session_state.profile.get("name", "USER")
        if st.session_state.profile
        else "USER"
    )

    st.sidebar.image("assets/1000061197.png", width=120)
    st.sidebar.markdown(f"### 👋 Hey {user_name}!!")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "👤 Create Profile",
            "📊 Placement Readiness & Guidance",
            "📚 Courses Recommendation",
            "💼 Job Opportunities",
            "ℹ️ About VYNOX"
        ]
    )

    # ---------------- HOME ----------------
    if menu == "🏠 Home":
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image("assets/1000061197.png", width=220)
        with col2:
            st.title("VYNOX")
            st.subheader("AI-Driven Placement Readiness Platform")
            st.write(
                """
                **VYNOX** analyzes student skills using Machine Learning,
                predicts placement readiness, and recommends
                personalized courses and job opportunities.
                """
            )

    # ---------------- PROFILE ----------------
    elif menu == "👤 Create Profile":
        st.header("👤 Student Profile")

        with st.form("profile_form"):
            name = st.text_input("Your Name")
            dsa_level = st.selectbox("DSA Level", ["Beginner", "Intermediate", "Advanced"])
            problem_count = st.number_input("Problems Solved", 0, 1000)
            language_count = st.number_input("Languages Known", 1, 10)
            cs_fundamentals = st.slider("CS Fundamentals (1-5)", 1, 5)
            project_count = st.number_input("Projects Completed", 0, 100)
            major_project = st.selectbox("Major Project Completed?", ["No", "Yes"])
            github_quality = st.selectbox("GitHub Quality", ["Low", "Medium", "High"])
            domain_focus = st.selectbox("Domain Focus", ["Web", "ML", "Data", "Core"])
            communication = st.slider("Communication Skills (1-5)", 1, 5)
            resume_quality = st.slider("Resume Quality (1-5)", 1, 5)
            mock_interviews = st.number_input("Mock Interviews Attended", 0, 200)
            learning_consistency = st.slider("Learning Consistency (1-5)", 1, 5)
            self_awareness = st.slider("Self Awareness (1-5)", 1, 5)

            if st.form_submit_button("Save Profile"):
                st.session_state.profile = {
                    "name": name,
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
                st.success("✅ Profile saved successfully")

    # ---------------- READINESS ----------------
    elif menu == "📊 Placement Readiness & Guidance":
        if not st.session_state.profile:
            st.warning("⚠️ Please create your profile first")
        else:
            level, score = predict_level(st.session_state.profile)
            st.metric("Readiness Score", f"{score}%")
            st.progress(score / 100)
            st.success(f"Level: **{level}**")

    # ---------------- COURSES ----------------
    elif menu == "📚 Courses Recommendation":
        if not st.session_state.profile:
            st.warning("⚠️ Create profile first")
        else:
            level, _ = predict_level(st.session_state.profile)
            st.dataframe(
                recommend_courses(level),
                use_container_width=True
            )

    # ---------------- JOBS ----------------
    elif menu == "💼 Job Opportunities":
        if not st.session_state.profile:
            st.warning("⚠️ Create profile first")
        else:
            level, _ = predict_level(st.session_state.profile)
            st.dataframe(
                recommend_jobs(level),
                use_container_width=True
            )

    # ---------------- ABOUT ----------------
    elif menu == "ℹ️ About VYNOX":
        st.header("ℹ️ About VYNOX")
        st.write(
            "**VYNOX** is an AI-powered placement readiness platform "
            "for student career guidance."
        )

