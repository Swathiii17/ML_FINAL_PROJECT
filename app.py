import streamlit as st
import numpy as np
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VYNOX",
    layout="wide"
)
# Page navigation
if "page" not in st.session_state:
    st.session_state.page = "landing"

# User profile
if "profile" not in st.session_state:
    st.session_state.profile = None
#--------Landing page----
if st.session_state.page == "landing":
    st.image("assets/landing.png", use_column_width=True)

    col1, col2, col3 = st.columns([3,2,3])
    with col2:
        if st.button("🌱 Join Us"):
            st.session_state.page = "main"
            st.rerun()
            
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

COURSES = [
    {
        "title": "Python for Everybody",
        "platform": "Coursera",
        "domain": "Programming",
        "level": "Beginner",
        "link": "https://www.coursera.org/learn/python"
    },
    {
        "title": "DSA Basics",
        "platform": "YouTube (FreeCodeCamp)",
        "domain": "DSA",
        "level": "Beginner",
        "link": "https://www.youtube.com/watch?v=8hly31xKli0"
    },
    {
        "title": "Operating Systems",
        "platform": "NPTEL",
        "domain": "CS Fundamentals",
        "level": "Intermediate",
        "link": "https://nptel.ac.in/courses/106"
    },
    {
        "title": "Machine Learning",
        "platform": "Coursera",
        "domain": "ML",
        "level": "Intermediate",
        "link": "https://www.coursera.org/learn/machine-learning"
    },
    {
        "title": "Deep Learning Specialization",
        "platform": "Coursera",
        "domain": "ML",
        "level": "Expert",
        "link": "https://www.coursera.org/specializations/deep-learning"
    }
]



JOB_REQUIREMENTS = {
    "Software Engineer": {
        "level": "Intermediate",
        "skills": [
            "DSA (Arrays, Trees, Graphs)",
            "OOPS",
            "One programming language (Java / Python / C++)",
            "Basic System Design"
        ]
    },
    "Data Analyst": {
        "level": "Beginner",
        "skills": [
            "Python / Excel",
            "SQL",
            "Data Visualization",
            "Statistics basics"
        ]
    },
    "ML Engineer": {
        "level": "Expert",
        "skills": [
            "Machine Learning algorithms",
            "Python & Libraries",
            "Model deployment",
            "Data preprocessing"
        ]
    }
}


# ---------------- SIDEBAR MENU ----------------
if st.session_state.page == "main":
  # ---------------- SIDEBAR MENU ----------------
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
        "📚 Free Courses",
        "💼 Job Entry Requirements",
        "ℹ️ About VYNOX"
     ]
    )

# ---------------- HOME PAGE ----------------
if menu == "🏠 Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("assets/1000061197.png", width=220)
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
    name = st.text_input(
    "Your Name",
    value=st.session_state.profile["name"] if st.session_state.profile else ""
   )

    with st.form("profile_form"):
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

        submit = st.form_submit_button("Save Profile")

        if submit:
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

# ---------------- PLACEMENT READINESS and guidance----------------
elif menu == "📊 Placement Readiness & Guidance":
    if "profile" not in st.session_state:
        st.warning("⚠️ Please create your profile first")
    else:
        profile = st.session_state.profile
        level, score = predict_level(profile)

        st.header("📊 Placement Readiness Result")
        st.subheader(f"Level: **{level}**")
        st.progress(score)
        st.write(f"Readiness Score: **{score}%**")

        st.divider()

        st.header("💡 Personalized Guidance")
        guidance = recommendations(level, profile["domain_focus"])
        for g in guidance:
            st.write("✔️", g)

# ---------------- Online courses----------------
elif menu == "📚 Free Courses":
    st.header("📚 Free & Efficient Online Courses")

    search = st.text_input("🔍 Search course (title / domain / level)")
    domain_filter = st.selectbox("Filter by Domain", ["All", "Programming", "DSA", "ML", "CS Fundamentals"])
    level_filter = st.selectbox("Filter by Level", ["All", "Beginner", "Intermediate", "Expert"])

    for course in COURSES:
        text = f"{course['title']} {course['domain']} {course['level']}".lower()

        if search.lower() not in text:
            continue
        if domain_filter != "All" and course["domain"] != domain_filter:
            continue
        if level_filter != "All" and course["level"] != level_filter:
            continue

        st.subheader(course["title"])
        st.write(f"📌 Platform: {course['platform']}")
        st.write(f"🎯 Domain: {course['domain']}")
        st.write(f"📈 Level: {course['level']}")
        st.markdown(f"[🔗 Go to Course]({course['link']})")
        st.divider()

# ---------------- Job----------------
elif menu == "💼 Job Entry Requirements":
    st.header("💼 Job Entry & Requirement Guide")

    for job, info in JOB_REQUIREMENTS.items():
        st.subheader(job)
        st.write(f"🎯 Minimum Level Required: **{info['level']}**")
        st.write("🛠 Required Skills:")
        for skill in info["skills"]:
            st.write("•", skill)
        st.divider()

# ---------------- ABOUT ----------------
elif menu == "ℹ️ About VYNOX":
    st.header("About VYNOX")
    st.write("**VYNOX** is a product-based company building intelligent career solutions for students.")

    st.subheader("👥 Team Members")
    st.write("- **Swathika** – Team Lead")
    st.write("- **Vishwa** – Tech Lead")
    st.write("- **Santhosh Kumar** – Designer")

