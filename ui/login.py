import streamlit as st
import time
from database.repository import Repository
from core.security import validate_email, validate_password_strength
import base64
import os

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def login_page():
    repo = Repository()
    
    # Session state for switching between login and signup
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
    
    # Custom Header Removal (already in main but double check)
    st.markdown("""
        <style>
            [data-testid="stHeader"] {visibility: hidden;}
            .block-container {padding-top: 2rem;}
        </style>
    """, unsafe_allow_html=True)

    # Main Auth Container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Logo & Hero
    # Use the logo in the ui directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "logo.png")
    logo_base64 = get_base64_image(logo_path)
    
    if logo_base64:
        st.markdown(f'''
            <div class="logo-wrapper">
                <img src="data:image/png;base64,{logo_base64}" class="logo-img">
                <h1 class="hero-title">MindLoop</h1>
                <p class="hero-subtitle">Connect with your digital reflection.</p>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="logo-wrapper">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
                <h1 class="hero-title">MindLoop</h1>
                <p class="hero-subtitle">Connect with your digital reflection.</p>
            </div>
        ''', unsafe_allow_html=True)

    # Social Login Area
    if st.session_state.auth_mode == 'login':
        st.markdown('<h2 style="color: white; font-size: 1.5rem; margin-bottom: 1.5rem; text-align: center;">Sign in to MindLoop</h2>', unsafe_allow_html=True)
    else:
        st.markdown('<h2 style="color: white; font-size: 1.5rem; margin-bottom: 1.5rem; text-align: center;">Create your account</h2>', unsafe_allow_html=True)

    # Social Buttons (Styled via custom HTML + Streamlit buttons hack or pure HTML)
    # Using columns for better alignment if needed, but the request was for large buttons like X
    
    if st.button("Continue with Google", key="btn_google", use_container_width=True):
        handle_social_login("Google", repo)
        
    if st.button("Continue with Apple", key="btn_apple", use_container_width=True):
        handle_social_login("Apple", repo)
        
    if st.button("Continue with Microsoft", key="btn_ms", use_container_width=True):
        handle_social_login("Microsoft", repo)

    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)

    # Credentials Form
    if st.session_state.auth_mode == 'login':
        render_login_form(repo)
    else:
        render_signup_form(repo)

    # Footer
    if st.session_state.auth_mode == 'login':
        st.markdown('''
            <div class="auth-footer">
                <a href="#">Forgot password?</a><br><br>
                <span style="color: #71767b;">Don't have an account? </span>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("Sign up", key="toggle_signup", kind="secondary"):
            st.session_state.auth_mode = 'signup'
            st.rerun()
    else:
        st.markdown('''
            <div class="auth-footer">
                <span style="color: #71767b;">Already have an account? </span>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("Sign in", key="toggle_login", kind="secondary"):
            st.session_state.auth_mode = 'login'
            st.rerun()

    # Security Badge
    st.markdown('''
        <div class="security-badge">
            <div style="display: flex; align-items: center; gap: 8px;">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <span>Enterprise-grade encryption active</span>
            </div>
            <span>[Protected by Private AI Protocol 2.1]</span>
            <div style="margin-top: 10px; display: flex; gap: 15px;">
                <a href="#" style="color: #444; text-decoration: none;">Terms of Service</a>
                <a href="#" style="color: #444; text-decoration: none;">Privacy Policy</a>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_login_form(repo):
    email_user = st.text_input("Email or Username", placeholder="Enter your email or username", key="login_email")
    password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pwd")
    
    if st.button("Log in", type="primary", use_container_width=True):
        if not email_user or not password:
            st.error("Please fill in all fields.")
            return
            
        with st.spinner("Authenticating..."):
            user = repo.get_user_by_credentials(email_user, password)
            if user:
                st.session_state.user = user
                st.success("Successfully logged in!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid email or password.")

def render_signup_form(repo):
    username = st.text_input("Username", placeholder="Choose a username", key="signup_user")
    email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Create a strong password", key="signup_pwd")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password", key="signup_confirm")
    
    if st.button("Create account", type="primary", use_container_width=True):
        # Validation
        if not all([username, email, password, confirm_password]):
            st.error("All fields are required.")
            return
            
        if not validate_email(email):
            st.error("Please enter a valid email address.")
            return
            
        if password != confirm_password:
            st.error("Passwords do not match.")
            return
            
        is_strong, msg = validate_password_strength(password)
        if not is_strong:
            st.error(msg)
            return
            
        # Check if user exists
        if repo.get_user_by_username(username):
            st.error("Username already taken.")
            return
            
        with st.spinner("Creating your secure profile..."):
            user = repo.create_user(username, email, password)
            if user:
                st.session_state.user = user
                st.success("Account created successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("An error occurred while creating your account.")

def handle_social_login(provider, repo):
    with st.spinner(f"Connecting to {provider}..."):
        time.sleep(1) # Simulate OAuth flow
        user = repo.handle_social_login(provider)
        if user:
            st.session_state.user = user
            st.success(f"Connected with {provider}!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error(f"Failed to connect with {provider}.")
