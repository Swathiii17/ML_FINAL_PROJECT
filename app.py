# app.py
import streamlit as st
import numpy as np
import joblib

# ---------------- Load ML Model ----------------
clf = joblib.load("placement_model.pkl")
le_dsa = joblib.load("le_dsa.pkl")
le_major = joblib.load("le_major.pkl")
le_github = joblib.load("le_github.pkl")
le_domain = joblib.load("le_domain.pkl")
le_target = joblib.load("le_target.pkl")

# ---------------- Prediction Function ----------------
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
    prob = np.max(clf.predict_proba(X)) * 100
    level = le_target.inverse_transform([pred])[0]

    return level, int(prob)

# ---------------- Recommendation Engine ----------------
def recommendations(level, domain):
    if level == "Beginner":
        return [
            "Learn Programming Fundamentals (Python / Java)",
            "Start DSA Basics",
            "Complete CS Fundamentals (OS, DBMS, CN)",
            "Solve 5 problems daily"
        ]

    elif level == "Intermediate":
        domain_projects = {
            "Web": "Job Portal / Portfolio Website",
            "ML": "Student Placement Prediction System",
            "Data": "Student Performance Analysis",
            "Core": "CPU Scheduling Simulator"
        }
        return [
            f"Focus on {domain} domain",
            domain_projects[domain],
            "Improve GitHub & Resume",
            "Start mock interviews"
        ]

    else:
        advanced_projects = {
            "Web": "Full Stack E-commerce Platform",
            "ML": "AI Interview Bot / Recommendation System",
            "Data": "Predictive Analytics with Real Data",
            "Core": "OS Performance Optimization"
        }
        return [
            advanced_projects[domain],
            "Prepare for company-specific interviews",
            "Practice system design",
            "Apply for internships & jobs"
        ]

# ---------------- UI ----------------
st.set_page_config(page_title="Placement Readiness App", layout="wide")
st.title("🎯 Student Placement Readiness & Career Guidance App")

menu = st.sidebar.selectbox("Menu", ["Create Profile", "Result & Guidance"])

# ---------------- Profile Page ----------------
if menu == "Create Profile":
    st.header("📝 Student Profile")

    with st.form("profile_form"):
        dsa_level = st.selectbox("DSA Level", ["Beginner", "Intermediate", "Advanced"])
        problem_count = st.number_input("Problems Solved", 0, 1000)
        language_count = st.number_input("Languages Known", 1, 10)
        cs_fundamentals = st.slider("CS Fundamentals (1-5)", 1, 5)
        project_count = st.number_input("Projects Completed", 0, 10)
        major_project = st.selectbox("Major Project Done?", ["No", "Yes"])
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
            st.success("✅ Profile Saved Successfully")

# ---------------- Result Page ----------------
if menu == "Result & Guidance":
    if "profile" not in st.session_state:
        st.warning("⚠️ Please create your profile first")
    else:
        profile = st.session_state.profile
        level, score = predict_level(profile)

        st.header("📊 Placement Readiness Result")
        st.subheader(f"Level: **{level}**")
        st.progress(score)
        st.write(f"Readiness Score: **{score}%**")

        st.header("💡 Personalized Guidance")
        recs = recommendations(level, profile["domain_focus"])
        for r in recs:
            st.write("✔️", r)
