import streamlit as st

st.set_page_config(page_title="Resources", layout="wide")

st.title("📚 Personalized Learning Resources")

st.markdown("""
### Recommended Resources
- Web Dev: MDN Web Docs, FreeCodeCamp
- Data Science: Kaggle, StatQuest
- Aptitude: IndiaBix
- Interviews: Striver SDE Sheet
""")

if st.button("🏠 Back to Home"):
    st.switch_page("app.py")
