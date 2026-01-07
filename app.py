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

# HOW IT WORKS
st.subheader("How It Works")
c1, c2, c3 = st.columns(3)

def card(title, text):
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)

with c1:
    card("🧠 Skill Assessment", "Answer placement-oriented questions.")
with c2:
    card("📊 Readiness Score", "AI evaluates your performance.")
with c3:
    card("📚 Learning Roadmap", "Get resources to improve weak areas.")

# DOMAINS
st.subheader("Explore Tech Domains")
domains = [
    ("🌐 Web Development", "Frontend & backend interview skills"),
    ("📊 Data Science", "ML & statistics fundamentals"),
    ("📱 Mobile Development", "Android & cross-platform basics"),
    ("🔐 Cybersecurity", "SOC & analyst readiness"),
    ("☁️ Cloud Engineering", "Cloud tools & concepts"),
    ("⛓ Blockchain", "Core blockchain concepts")
]

cols = st.columns(3)
for i, d in enumerate(domains):
    with cols[i % 3]:
        card(d[0], d[1])

# STATS
st.markdown("---")
s1, s2, s3, s4 = st.columns(4)
stats = [
    ("500+", "Questions Designed"),
    ("8", "Career Domains"),
    ("92%", "Model Confidence"),
    ("85%", "Validation Accuracy")
]

for col, stat in zip([s1, s2, s3, s4], stats):
    with col:
        st.markdown(f"""
        <div class="stat">
            <h3>{stat[0]}</h3>
            <p>{stat[1]}</p>
        </div>
        """, unsafe_allow_html=True)

