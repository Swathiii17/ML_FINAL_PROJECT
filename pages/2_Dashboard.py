import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

st.title("📊 Your Readiness Dashboard")

score = st.session_state.get("score", None)

if score is None:
    st.warning("Please complete the assessment first.")
    st.stop()

st.metric("Placement Readiness Score", f"{score}%")

if score >= 80:
    st.success("Excellent! You are placement ready.")
elif score >= 50:
    st.info("Good progress. Some improvement needed.")
else:
    st.error("Needs improvement. Follow the roadmap.")

st.progress(score)

if st.button("📚 View Learning Resources"):
    st.switch_page("pages/3_Resources.py")
