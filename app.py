import streamlit as st

st.set_page_config(page_title="VYNOX", layout="wide")

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# HERO SECTION
st.markdown("""
<div class="hero">
    <h1>Welcome to VYNOX</h1>
    <p>AI-powered Placement Readiness Assessment System</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("🚀 Check Your Placement Readiness", use_container_width=True):
        st.experimental_set_query_params(page="assessment")
        st.experimental_rerun()

# HOW IT WORKS - Custom Replacement
st.subheader("How It Works")

custom_workflow = [
    ("📝 Take Assessment", "Answer placement-oriented questions designed by experts."),
    ("📈 Get AI Score", "Receive a detailed placement readiness score."),
    ("🎯 Personalized Roadmap", "Learn which skills to improve and which courses to take.")
]

cols = st.columns(len(custom_workflow))
for col, wf in zip(cols, custom_workflow):
    with col:
        st.markdown(f"""
        <div class="card">
            <h4>{wf[0]}</h4>
            <p>{wf[1]}</p>
        </div>
        """, unsafe_allow_html=True)

# EXPLORE TECH DOMAINS - Custom Replacement
st.subheader("Explore Your Career Paths")

custom_domains = [
    ("🌐 Web Dev", "Frontend & backend fundamentals"),
    ("🤖 AI & ML", "Machine Learning & AI basics"),
    ("📱 App Development", "Mobile app development essentials"),
    ("🔒 Cybersecurity", "Security & ethical hacking"),
    ("☁️ Cloud Computing", "Cloud tools & services"),
    ("⛓ Blockchain", "Blockchain fundamentals"),
    ("🖥 Embedded Systems", "IoT & hardware interfacing"),
    ("🎮 Game Development", "Game design & development")
]

cols = st.columns(4)  # 4 per row for better layout
for i, domain in enumerate(custom_domains):
    with cols[i % 4]:
        st.markdown(f"""
        <div class="card">
            <h4>{domain[0]}</h4>
            <p>{domain[1]}</p>
        </div>
        """, unsafe_allow_html=True)

