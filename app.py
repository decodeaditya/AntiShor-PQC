import streamlit as st

st.set_page_config(page_title="Shor's Algorithm and Post Quantum cryptography Demo", page_icon="🛡️", layout="wide")

pages = {
    "Navigate": [
        st.Page("shors_demo_page.py", title="Shor's Demo",url_path="shors_demo"),
        st.Page("pqc_page.py", title="Post Quantum Cryptography",url_path="post-quantum-cryptography"),
    ]
}

pg = st.navigation(pages, position='sidebar')
pg.run()
