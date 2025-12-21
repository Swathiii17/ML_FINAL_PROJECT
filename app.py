import streamlit as st
import numpy as np
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VYNOX",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"  # directly go to home

if "profile" not in st.session_state:
    st.session_state.profile = None

# ---------------- LOAD MODEL ----------------
clf = joblib.load("placement_model.pkl")
le_dsa = joblib.load("le_dsa.pkl")
le_major = joblib.load("le_major.pkl")
le_github = joblib.load("le_github.pkl")
le_domain = joblib.load("le_domain.pkl")
le_target = joblib.load("le_target.pkl")

# ---------------- FUNCTIONS ----------------
def predict_level(profile):
    dsa = le_dsa.transform([profile["dsa_level"]])[0]
    major = le_major.transform([profile["major_project"]])[0]
    github = le_github.transform([profile["github_quality"]])[0]
    domain = le_domain.transform([profile["domain_focus"]])[0]

    X = np.array([
        dsa,
        profile["problem_count"],
        profile["language_count"],
        profile["cs_fundamentals"],
        profile["project_count"],
        major,
        github,
        domain,
        profile["communication"],
        profile["resume_quality"],
        profile["mock_interviews"],
        profile["learning_consistency"],
        profile["self_awareness"]
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

# ---------------- DATA ----------------
COURSES = [
    {"title": "Python for Everybody", "platform": "Coursera", "domain": "Programming", "level": "Beginner", "link": "https://www.coursera.org/learn/python"},
    {"title": "DSA Basics", "platform": "YouTube", "domain": "DSA", "level": "Beginner", "link": "https://www.youtube.com/watch?v=8hly31xKli0"},
    {"title": "Operating Systems", "platform": "NPTEL", "domain": "CS Fundamentals", "level": "Intermediate", "link": "https://nptel.ac.in/courses/106"},
    {"title": "Machine Learning", "platform": "Coursera", "domain": "ML", "level": "Intermediate", "link": "https://www.coursera.org/learn/machine-learning"},
    {"title": "Deep Learning Specialization", "platform": "Coursera", "domain": "ML", "level": "Expert", "link": "https://www.coursera.org/specializations/deep-learning"}
]

JOB_REQUIREMENTS = {
    "Software Engineer": {
        "level": "Intermediate",
        "skills": ["DSA", "OOPS", "Java / Python / C++", "Basic System Design"]
    },
    "Data Analyst": {
        "level": "Beginner",
        "skills": ["Python / Excel", "SQL", "Statistics", "Visualization"]
    },
    "ML Engineer": {
        "level": "Expert",
        "skills": ["ML Algorithms", "Python", "Deployment", "Data Processing"]
    }
}

# ---------------- SIDEBAR ----------------
user_name = st.session_state.profile["name"] if st.session_state.profile else "USER"

st.sidebar.markdown(f"### 👋 Hey {user_name}")
menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👤 Create Profile",
        "📊 Placement Readiness & Guidance",
        "📚 Free Courses",
        "💼 Job Entry Requirements",
        "ℹ️ About VYNOX"
    ]
)

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.image("assets/logo.png", width=200)  # Logo at top
    st.title("VYNOX")
    st.subheader("AI-powered platform for placement readiness & career guidance.")

# ---------------- PROFILE ----------------
elif menu == "👤 Create Profile":
    st.header("Student Profile")

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
            st.success("Profile saved successfully ✅")

# ---------------- PLACEMENT ----------------
elif menu == "📊 Placement Readiness & Guidance":
    if not st.session_state.profile:
        st.warning("Please create your profile first.")
    else:
        level, score = predict_level(st.session_state.profile)
        st.subheader(f"Level: {level}")
        st.progress(score)
        st.write(f"Readiness Score: {score}%")

        st.header("Guidance")
        for g in recommendations(level, st.session_state.profile["domain_focus"]):
            st.write("✔", g)

# ---------------- COURSES ----------------
elif menu == "📚 Free Courses":
    for c in COURSES:
        st.subheader(c["title"])
        st.write(c["platform"], "|", c["domain"], "|", c["level"])
        st.markdown(f"[Go to Course]({c['link']})")
        st.divider()

# ---------------- JOBS ----------------
elif menu == "💼 Job Entry Requirements":
    for job, info in JOB_REQUIREMENTS.items():
        st.subheader(job)
        st.write("Minimum Level:", info["level"])
        for s in info["skills"]:
            st.write("•", s)

# ---------------- ABOUT ----------------
elif menu == "ℹ️ About VYNOX":
    st.subheader("About VYNOX")
    st.write("AI-powered career & placement guidance platform.")
    st.write("**Team:** Swathika (Lead), Vishwa (Tech), Santhosh Kumar (Design)")

