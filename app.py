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
RAPID_API_KEY = "YOUR_RAPID_API_KEY"
FINDWORK_API_KEY = "YOUR_FINDWORK_API_KEY"

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
FALLBACK_COURSES = [
    {
        "name": "Python for Everybody – Coursera",
        "url": "https://www.coursera.org/specializations/python",
        "description": "Learn Python basics and work with data. Free to audit; certificate optional."
    },
    {
        "name": "Machine Learning – Andrew Ng",
        "url": "https://www.coursera.org/learn/machine-learning",
        "description": "Introductory ML course covering algorithms and applications. Free to audit; certificate optional."
    },
    {
        "name": "Google Data Analytics",
        "url": "https://www.coursera.org/professional-certificates/google-data-analytics",
        "description": "Learn data cleaning, visualization, and analysis using Google tools. Free to audit; certificate optional."
    },
    {
        "name": "Web Development Bootcamp – Udemy",
        "url": "https://www.udemy.com/course/the-web-developer-bootcamp/",
        "description": "Full-stack web development with HTML, CSS, JS, and Node.js. Free access possible via coupons or audit."
    },
    {
        "name": "CS50 – Harvard",
        "url": "https://cs50.harvard.edu/x/",
        "description": "Harvard’s CS50 Introduction to Computer Science. Free to study online with optional certificate."
    }
]
#def fetch_courses():
    #url = "https://collection-for-coursera-courses.p.rapidapi.com/rapidapi/course/get_courses.php"

   # headers = {
       # "X-RapidAPI-Key": RAPID_API_KEY,
       # "X-RapidAPI-Host": "collection-for-coursera-courses.p.rapidapi.com"
   # }

   # try:
        #res = requests.get(url, headers=headers, timeout=10)
        #res.raise_for_status()
        #data = res.json()

        #courses = []
        #for item in data:
            #courses.append({
                #"name": item.get("course_name", "Unnamed Course"),
                #"url": item.get("course_url", "#")
            #})

        #return courses

    #except Exception as e:
        #st.error(f"Course API Error: {e}")
        #return []


# ================= JOB API =================
FALLBACK_JOBS = [
    {
        "role": "Junior Python Developer",
        "company_name": "Tech Solutions Pvt Ltd",
        "location": "Remote",
        "url": "https://www.indeed.com/viewjob?jk=python_dev_001"
    },
    {
        "role": "Machine Learning Intern",
        "company_name": "DataCorp AI",
        "location": "Bangalore, India",
        "url": "https://www.indeed.com/viewjob?jk=ml_intern_002"
    },
    {
        "role": "Web Developer Intern",
        "company_name": "WebWorks",
        "location": "Chennai, India",
        "url": "https://www.indeed.com/viewjob?jk=web_dev_003"
    },
    {
        "role": "Data Analyst Intern",
        "company_name": "Analytics Pro",
        "location": "Remote",
        "url": "https://www.indeed.com/viewjob?jk=data_analyst_004"
    },
    {
        "role": "Frontend Developer",
        "company_name": "DesignSoft",
        "location": "Mumbai, India",
        "url": "https://www.indeed.com/viewjob?jk=frontend_dev_005"
    }
]
#def fetch_jobs(role):
    #url = f"https://findwork.dev/api/jobs/?search={role}"

    #headers = {
        #"Authorization": f"Token {FINDWORK_API_KEY}"
    #}

    #try:
        #res = requests.get(url, headers=headers, timeout=10)
        #res.raise_for_status()
        #return res.json().get("results", [])

    #except Exception as e:
        #st.error(f"Job API Error: {e}")
        #return []


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

    # HERO SECTION
    st.markdown("## 👋 WELCOME TO **TEAM VYNOX**")
    st.markdown("### Your Smart Path to Placement")

    st.write(
        "VYNOX is a product-based platform designed to guide students "
        "towards successful placements using intelligent prediction, "
        "skill analysis, and personalized guidance.\n"
    )

    st.info("👉 Use the **Create Profile** tab to get started\n")

    st.divider()

    # HOW PLATFORM WORKS
    st.markdown("## 🔄 How Our Platform Works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("**Create Profile**\n\nEnter academic & skill details")

    with col2:
        st.success("**Placement Prediction**\n\nML predicts readiness level")

    with col3:
        st.success("**Course Guidance**\n\nPersonalized learning paths")

    with col4:
        st.success("**Job Suggestions**\n\nRoles aligned to your profile")

    st.divider()

    # WHAT WE OFFER
    st.markdown("## 🎯 What We Offer\n")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("**Placement Readiness**\n\nData-driven insights")

    with c2:
        st.info("**Skill Enhancement**\n\nFocused recommendations")

    with c3:
        st.info("**Career Guidance**\n\nLong-term growth direction")

    st.divider()

    # SLOGAN / VISION / MISSION
    st.markdown("### 🏷️ **OUR SLOGAN**")
    st.write("**  Shaping Digital Futures**")

    st.markdown("### 👁️ **OUR VISION**")
    st.write(
        "  To empower students with intelligent tools that transform "
        "career preparation into a confident and data-driven journey."
    )

    st.markdown("### 🚀 **OUR MISSION**")
    st.write(
        "  To build reliable, innovative, and accessible products that "
        "guide learners towards successful careers through technology."
    )

    st.divider()

    st.caption("© 2026 VYNOX | All Rights Reserved")


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
        st.session_state["profile"] = profile
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
    st.header("📚 Free Courses")

    for course in FALLBACK_COURSES:
    with st.container():
        st.markdown(
            f'''
            <div style='border:2px solid #4CAF50; padding:20px; border-radius:10px; margin-bottom:20px;'>
                <h3 style='color:#4CAF50;'>🎓 {course["name"]}</h3>
                <p>{course["description"]}</p>
                <a href='{course["url"]}' target='_blank' style='text-decoration:none; color:white; background-color:#4CAF50; padding:8px 16px; border-radius:5px;'>Go to Course</a>
            </div>
            ''',
            unsafe_allow_html=True
        )



# ================= JOBS =================
elif menu == "💼 Jobs":
    st.header("💼 Jobs")

    for job in FALLBACK_JOBS:
        with st.container():
            st.markdown(
                f"""
                <div style="border:2px solid #2196F3; padding:20px; border-radius:10px; margin-bottom:20px;">
                    <h3 style="color:#2196F3;">💼 {job['role']}</h3>
                    <p><b>Company:</b> {job['company_name']}<br>
                    <b>Location:</b> {job['location']}</p>
                    <a href="{job['url']}" target="_blank" style="text-decoration:none; color:white; background-color:#2196F3; padding:8px 16px; border-radius:5px;">Apply Now</a>
                </div>
                """,
                unsafe_allow_html=True
            )



# ================= ABOUT =================
elif menu == "ℹ️ About":

    # PAGE TITLE
    st.markdown("## ℹ️ About **VYNOX**")
    st.markdown("### Empowering Students for Smarter Career Decisions")

    st.divider()

    # DESCRIPTION (useful for viva)
    st.write(
        "VYNOX is an AI-powered, product-based placement readiness platform "
        "designed to support students in evaluating their career preparedness. "
        "By combining machine learning, skill analysis, and personalized guidance, "
        "VYNOX helps learners understand their strengths, identify gaps, and take "
        "confident steps toward successful placements."
    )

    st.write(
        "The platform bridges the gap between academic knowledge and industry "
        "expectations by offering placement prediction, curated learning paths, "
        "and real-world job insights in a single unified system."
    )

    st.divider()

    # PROJECT TEAM
    st.markdown("## 👥 Project Team")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            "**Swathika P**  \n"
            "Team Lead"
        )

    with col2:
        st.success(
            "**Vishwa R**  \n"
            "Tech Lead"
        )

    with col3:
        st.success(
            "**Santhosh Kumar U**  \n"
            "Designer"
        )

    st.divider()

    # CONTACT DETAILS
    st.markdown("## 📞 Contact Details")

    c1, c2,c3 = st.columns(3)

    with c1:
        st.info(
            "📧 **Email**  \n"
            "vynox.support@gmail.com"
        )

    with c2:
        st.info(
            "🌐 **LinkedIn**  \n"
            "https://www.linkedin.com/company/vynox"
        )
    with c3:
        st.info(
            "🌐 **Phone**  \n"
            "+91 80000 40000"
        )

    st.divider()

    # FOOTER NOTE
    st.caption(
        "© 2026 VYNOX | AI-Powered Placement Readiness Platform | All Rights Reserved"
    )

