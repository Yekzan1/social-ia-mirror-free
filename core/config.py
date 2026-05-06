import os
import streamlit as st
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    PROJECT_NAME = "MindLoop"
    VERSION = "5.0.0-PREMIUM"
    
    # Supabase Credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "")
    
    # UI Constants
    PRIMARY_COLOR = "#8a2be2"
    SECONDARY_COLOR = "#00c2ff"
    DARK_BG = "#050505"
    
    # AI Configuration
    AI_MODEL_URL = "https://text.pollinations.ai/"
    
    # Branding
    SLOGAN = "It's happening now"
    SUBTITLE = "A private space for the people who truly matter."

    @staticmethod
    def setup_page():
        st.set_page_config(
            page_title=f"{Config.PROJECT_NAME} | {Config.SLOGAN}",
            page_icon="🔮",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
