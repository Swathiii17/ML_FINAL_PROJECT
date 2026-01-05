import streamlit as st

st.set_page_config(
    page_title="Placement Readiness System",
    layout="wide"
)
st.markdown("""
<style>
body {
    background-color: #f4f6f8;
}

.block-container {
    padding: 2rem 3rem;
}

h1, h2, h3 {
    color: #0a2540;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 12px 25px;
    font-size: 16px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <h1 style="text-align:center;">Placement Readiness System</h1>
    <p style="text-align:center; font-size:18px;">
    Analyze your skills, predict placement readiness, and improve your career path
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("<h2>Student Information</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    name = st.text_input("Student Name")
    cgpa = st.number_input("CGPA", 0.0, 10.0)
    internships = st.number_input("Number of Internships", 0, 10)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    python_skill = st.selectbox("Python Skill Level", ["Beginner", "Intermediate", "Advanced"])
    ml_skill = st.selectbox("Machine Learning Level", ["Beginner", "Intermediate", "Advanced"])
    communication = st.selectbox("Communication Skill", ["Poor", "Average", "Good"])
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<h2>Placement Readiness Result</h2>", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

if st.button("Check Placement Readiness"):
    st.success("You are Moderately Placement Ready ✅")
    st.info("Improve ML skills and communication for better chances.")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""
<hr>
<p style="text-align:center;">
© 2026 Placement Readiness System | Built with Streamlit
</p>
""", unsafe_allow_html=True)
