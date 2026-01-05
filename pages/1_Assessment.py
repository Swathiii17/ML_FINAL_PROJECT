import streamlit as st

st.set_page_config(page_title="Assessment", layout="wide")

st.title("🧠 Placement Readiness Assessment")

questions = {
    "Web Development": [
        ("What does HTML stand for?", "Hyper Text Markup Language"),
        ("What is CSS used for?", "Styling web pages")
    ],
    "Data Science": [
        ("What is overfitting?", "Model performs well on training but poor on test"),
        ("Mean of [2,4,6]?", "4")
    ],
}

score = 0
total = 0

for domain, qs in questions.items():
    st.subheader(domain)
    for q, ans in qs:
        user = st.text_input(q)
        if user:
            total += 1
            if ans.lower() in user.lower():
                score += 1

if st.button("Submit Assessment"):
    if total == 0:
        st.warning("Answer at least one question.")
    else:
        st.session_state["score"] = int((score / total) * 100)
        st.switch_page("pages/2_Dashboard.py")
