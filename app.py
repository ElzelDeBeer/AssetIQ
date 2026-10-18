import streamlit as st

st.set_page_config(page_title="AssetIQ AI", page_icon="⚙️", layout="wide")

pages = [
    st.Page("views/home.py", title="Home", default=True),
    st.Page("views/dashboard.py", title="Dashboard"),
    st.Page("views/evidence.py", title="Model evidence (AI4I)"),
]
st.navigation(pages).run()
