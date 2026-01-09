import streamlit as st
import numpy as np
import joblib
import requests

# ================= PAGE CONFIG =================
st.set_page_config(page_title="VYNOX", layout="wide")

# ================= SESSION STATE =================
if "profile" not in st.session_state:
    st.session_state["profile"] = None

# ================= LOAD MODELS =================
clf = joblib.load("placement_model.pkl")
le_dsa = joblib.load("le_dsa.pkl")
le_major = joblib.load("le_major.pkl")
le_github = joblib.load("le_github.pkl")
le_domain = joblib.load("le_domain.pkl")
le_target = joblib.load("le_target.pkl")

# ================= API KEYS =================
RAPID_API_KEY = "6da45f54e5msha20ec1559af5427p166747jsnc887b50c4210"
FINDWORK_API_KEY = "YOUR_FINDWORK_API_KEY"   # free job API

# ================= FUNCTIONS =================
def predict_level(profile):
    X = np.array([
        le_dsa.transform([profile["dsa_level"]])[0],
        profile["problem_count"],
        profile["language_count"],
        profile["cs_fundamentals"],
        profile["project_count"],
        le_major.transform([profile["major_project"]])[0],
        le_github.transform([profile["github_quality"]])[0],
        le_domain.transform([profile["domain_focus"]])[0],
        profile["communication"],
        profile["resume_quality"],
        profile["mock_interviews"],
        profile["learning_consistency"],
        profile["self_awareness"]
    ]).reshape(1, -1)

    pred = clf.predict(X)[0]
    score = int(np.max(clf.predict_proba(X)) * 100)
    return le_target.inverse_transform([pred])[0], score


def recommendations(level, domain):
    data = {
        "Beginner": [
            "Learn Python / Java fundamentals",
            "Start DSA basics",
            "Study OS, DBMS, CN",
            "Solve 5 problems daily"
        ],
        "Intermediate": [
            f"Build projects in {domain}",
            "Improve GitHub & Resume",
            "Start mock interviews"
        ],
        "Expert": [
            "Advanced projects",
            "System Design",
            "Apply for internships & jobs"
        ]
    }
    return data[level]


# ================= COURSE API =================
def fetch_courses():
    url = "https://collection-for-coursera-courses.p.rapidapi.com/rapidapi/course/get_courses.php"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "collection-for-coursera-courses.p.rapidapi.com"
    }
    res = requests.get(url, headers=headers)
    return res.json() if res.status_code == 200 else []


# ================= JOB API =================
def fetch_jobs(role):
    url = f"https://findwork.dev/api/jobs/?search={role}"
    headers = {"Authorization": f"Token {FINDWORK_API_KEY}"}
    res = requests.get(url, headers=headers)
    return res.json().get("results", []) if res.status_code == 200 else []


# ================= SIDEBAR =================
user = st.session_state.profile["name"] if st.session_state.profile else "User"
st.sidebar.title("VYNOX 🚀")
st.sidebar.markdown(f"👋 Hello **{user}**")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "👤 Create Profile", "📊 Placement Readiness",
     "📚 Free Courses", "💼 Jobs", "ℹ️ About"]
)

# ================= HOME =================
if menu == "🏠 Home":
    st.title("VYNOX")
    st.subheader("AI-Powered Placement Readiness & Career Guidance Platform")

# ================= PROFILE =================
elif menu == "👤 Create Profile":
    st.header("Create Your Profile")

    with st.form("profile_form"):
        profile = {
            "name": st.text_input("Name"),
            "dsa_level": st.selectbox("DSA Level", ["Beginner", "Intermediate", "Advanced"]),
            "problem_count": st.number_input("Problems Solved", 0),
            "language_count": st.number_input("Languages Known", 1),
            "cs_fundamentals": st.slider("CS Fundamentals", 1, 5),
            "project_count": st.number_input("Projects", 0),
            "major_project": st.selectbox("Major Project", ["No", "Yes"]),
            "github_quality": st.selectbox("GitHub Quality", ["Low", "Medium", "High"]),
            "domain_focus": st.selectbox("Domain", ["Web", "ML", "Data", "Core"]),
            "communication": st.slider("Communication", 1, 5),
            "resume_quality": st.slider("Resume Quality", 1, 5),
            "mock_interviews": st.number_input("Mock Interviews", 0),
            "learning_consistency": st.slider("Consistency", 1, 5),
            "self_awareness": st.slider("Self Awareness", 1, 5)
        }

        submitted = st.form_submit_button("Save Profile")

    if submitted:
        st.session_state["profile"] = profile   # ✅ SAFE
        st.success("Profile saved successfully ✅")


# ================= PLACEMENT =================
elif menu == "📊 Placement Readiness":
    if not st.session_state.profile:
        st.warning("Create profile first")
    else:
        level, score = predict_level(st.session_state.profile)
        st.metric("Placement Level", level)
        st.progress(score)

        st.subheader("Guidance")
        for r in recommendations(level, st.session_state.profile["domain_focus"]):
            st.write("✔", r)

# ================= COURSES =================
elif menu == "📚 Free Courses":
    st.header("Free Coursera Courses")

    domain = st.selectbox(
        "Choose Domain",
        ["Python", "Machine Learning", "Data Science", "Web Development"]
    )

    if st.button("Fetch Courses"):
        with st.spinner("Loading courses..."):
            courses = fetch_courses()

        keywords = {
            "Python": ["python"],
            "Machine Learning": ["ml", "machine", "ai"],
            "Data Science": ["data"],
            "Web Development": ["web", "html", "css", "javascript"]
        }[domain]

        filtered = [c for c in courses if any(k in c.lower() for k in keywords)]

        for c in filtered[:10]:
            st.success(c)

# ================= JOBS =================
elif menu == "💼 Jobs":
    st.header("Live Job Openings")

    role = st.selectbox(
        "Select Role",
        ["Software Engineer", "Data Analyst", "ML Engineer"]
    )

    if st.button("Find Jobs"):
        jobs = fetch_jobs(role)

        if jobs:
            for j in jobs[:10]:
                st.markdown(f"""
                ### {j['role']}
                **Company:** {j['company_name']}  
                **Location:** {j['location']}  
                [Apply Here]({j['url']})
                """)
        else:
            st.warning("No jobs found")

# ================= ABOUT =================
elif menu == "ℹ️ About":
    st.header("About VYNOX")
    st.write("AI-powered placement & career guidance platform")
    st.write("Team: Swathika | Vishwa | Santhosh Kumar")
