import streamlit as st
import numpy as np
import joblib
import requests

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
# ---------------- COURSE API ----------------
RAPID_API_KEY = "6da45f54e5msha20ec1559af5427p166747jsnc887b50c4210"
def fetch_courses(domain):
    url = "https://collection-for-coursera-courses.p.rapidapi.com/rapidapi/course/get_institution.php"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "collection-for-coursera-courses.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    st.write(response.json())

    if response.status_code == 200:
        data = response.json()
        return data if isinstance(data, list) else []
    else:
        return []

# ---------------- JOB REQUIREMENTS ----------------
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
    st.header("🎓 Free Courses (Coursera)")

    domain = st.selectbox(
        "Select Domain",
        ["Python", "Machine Learning", "Data Science", "Web", "AI"]
    )

    if st.button("🔍 Find Courses"):
        with st.spinner("Fetching real courses..."):
            courses = fetch_courses(domain)

        filtered = [
            c for c in courses
            if domain.lower() in c.get("course_name", "").lower()
        ]

        if not filtered:
            st.warning("No courses found. Try another domain.")
        else:
            for c in filtered[:5]:
                st.subheader(c.get("course_name", "Course"))
                st.markdown(f"[Go to Course]({c.get('course_url', '#')})")
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

