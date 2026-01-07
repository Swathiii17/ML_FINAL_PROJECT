import streamlit as st
import pandas as pd
import pickle
import joblib

st.set_page_config(page_title="Placement Assessment", layout="wide")

# Load Data
students_df = pd.read_csv('student_profiles.csv')
courses_df = pd.read_csv('courses.csv')
jobs_df = pd.read_csv('jobs.csv')

# Load Models & Encoders
joblib.dump(placement_model, 'placement_model.pkl')
joblib.dump(le_domain, 'le_domain.pkl')
joblib.dump(le_dsa, 'le_dsa.pkl')
joblib.dump(le_github, 'le_github.pkl')
joblib.dump(le_major, 'le_major.pkl')
joblib.dump(le_target, 'le_target.pkl')

# ---------------------------
st.title("🎯 Placement Readiness Assessment")

# Student selection
st.sidebar.header("Select Your Profile")
student_names = students_df['name'].tolist()
selected_student = st.sidebar.selectbox("Choose your profile:", student_names)
student_data = students_df[students_df['name'] == selected_student].iloc[0]

st.subheader(f"Welcome, {selected_student}!")
st.write("### 📝 Your Profile")
st.write(f"**Domain:** {student_data['domain']}")
st.write(f"**DSA Skill:** {student_data['dsa']}")
st.write(f"**GitHub Experience:** {student_data['github']}")
st.write(f"**Major:** {student_data['major']}")
st.write(f"**Target Company:** {student_data['target']}")

# Update inputs
st.subheader("Update Your Skills / Preferences")
domain_input = st.selectbox("Domain", options=students_df['domain'].unique(), index=list(students_df['domain'].unique()).index(student_data['domain']))
dsa_input = st.selectbox("DSA Skill Level", options=students_df['dsa'].unique(), index=list(students_df['dsa'].unique()).index(student_data['dsa']))
github_input = st.selectbox("GitHub Experience", options=students_df['github'].unique(), index=list(students_df['github'].unique()).index(student_data['github']))
major_input = st.selectbox("Major", options=students_df['major'].unique(), index=list(students_df['major'].unique()).index(student_data['major']))
target_input = st.selectbox("Target Company", options=students_df['target'].unique(), index=list(students_df['target'].unique()).index(student_data['target']))

# Encode
features = [[
    le_domain.transform([domain_input])[0],
    le_dsa.transform([dsa_input])[0],
    le_github.transform([github_input])[0],
    le_major.transform([major_input])[0],
    le_target.transform([target_input])[0]
]]

# Predict
if st.button("Predict Readiness"):
    readiness_score = placement_model.predict(features)[0]
    st.success(f"Your predicted placement readiness score is: **{readiness_score}**")

    # Recommend courses
    st.subheader("📚 Recommended Courses")
    recommended_courses = courses_df[(courses_df['domain']==domain_input)]
    st.table(recommended_courses[['course_name','provider','duration']])

    # Recommend jobs
    st.subheader("💼 Suitable Job Openings")
    recommended_jobs = jobs_df[jobs_df['required_domain']==domain_input]
    st.table(recommended_jobs[['job_title','company','location','required_skills']])
