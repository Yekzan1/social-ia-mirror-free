import streamlit as st
import sys
import os
from core.config import Config
from ui.login import login_page
from ui.dashboard import dashboard_page

def main():
    # Setup page configuration
    Config.setup_page()
    
    # Load custom premium styles
    current_dir = os.path.dirname(os.path.abspath(__file__))
    style_path = os.path.join(current_dir, "ui", "styles.css")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    
    # Session State Initialization
    if 'user' not in st.session_state:
        st.session_state.user = None

    # Routing Logic
    if st.session_state.user is None:
        login_page()
    else:
        dashboard_page()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"A critical error occurred: {e}")
        if st.button("Recover Session"):
            st.session_state.user = None
            st.rerun()
