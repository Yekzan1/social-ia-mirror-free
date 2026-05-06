import streamlit as st
import time
import base64
import os
from database.repository import Repository
from core.security import validate_email, validate_password_strength

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def login_page():
    repo = Repository()
    
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'landing'

    # Load logo
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "logo.png")
    logo_base64 = get_base64_image(logo_path)
    
    # Render Auth Container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Hero Section
    if logo_base64:
        st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{logo_base64}" class="hero-logo"></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align: center; font-size: 5rem; margin-bottom: 20px;">🧠</div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="hero-title">It\'s happening now</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">A private space for the people who truly matter.</p>', unsafe_allow_html=True)

    # Main Card
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    if st.session_state.auth_mode == 'landing':
        render_landing_view(repo)
    elif st.session_state.auth_mode == 'login':
        render_login_view(repo)
    elif st.session_state.auth_mode == 'signup':
        render_signup_view(repo)

    st.markdown('</div>', unsafe_allow_html=True) # End main-card

    # Footer
    st.markdown('''
        <div class="security-text">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
            Your data is protected with enterprise-grade security. [Powered by Private AI Protocol 2.1]
        </div>
        <div style="text-align: center; margin-top: 16px; font-size: 0.8rem; color: #71767b;">
            <a href="#" style="color: inherit; margin: 0 10px;">Cookies Policy</a> | 
            <a href="#" style="color: inherit; margin: 0 10px;">Terms</a>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # End auth-container

def render_landing_view(repo):
    st.markdown('<h2 style="color: white; font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem; text-align: center;">Join the circle today.</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        if st.button("Sign up with Google", key="landing_google", use_container_width=True):
            handle_social_login("Google", repo)
            
        if st.button("Sign up with Apple", key="landing_apple", use_container_width=True):
            handle_social_login("Apple", repo)
            
        if st.button("Sign up with Microsoft", key="landing_ms", use_container_width=True):
            handle_social_login("Microsoft", repo)
            
        st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
        
        if st.button("Create account", key="go_signup", type="primary", use_container_width=True):
            st.session_state.auth_mode = 'signup'
            st.rerun()
            
        st.markdown('<p style="font-size: 0.75rem; color: #71767b; margin-top: 1rem; text-align: center;">By signing up, you agree to the Terms of Service and Privacy Policy.</p>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: 40px; text-align: left;">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">Already have an account?</p>', unsafe_allow_html=True)
        if st.button("Sign in", key="go_login", use_container_width=True):
            st.session_state.auth_mode = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def render_login_view(repo):
    # This view matches the provided image exactly
    if st.button("Continue with Google", key="login_google", use_container_width=True):
        handle_social_login("Google", repo)
        
    if st.button("Continue with Microsoft", key="login_ms", use_container_width=True):
        handle_social_login("Microsoft", repo)
        
    if st.button("Continue with GitHub", key="login_github", use_container_width=True):
        handle_social_login("GitHub", repo)
        
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
    
    # Email field
    email = st.text_input("Email", placeholder="name@company.com", label_visibility="visible", key="login_email")
    
    # Password field
    password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="visible", key="login_pwd")
    
    # Sign in button (Primary with gradient)
    if st.button("Sign in →", key="login_submit", type="primary", use_container_width=True):
        if not email or not password:
            st.error("Please fill in all fields.")
            return
            
        with st.spinner("Authenticating..."):
            user = repo.get_user_by_credentials(email, password)
            if user:
                st.session_state.user = user
                st.success("Welcome back!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    st.markdown('''
        <div class="form-footer">
            <a href="#">Forgot password?</a>
            <p style="color: #71767b;">Don't have an account? <a href="javascript:window.parent.postMessage({type: 'streamlit:rerun', auth_mode: 'signup'}, '*');" onclick="return false;">Sign up</a></p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Manual trigger for sign up since links are tricky in Streamlit
    if st.button("Don't have an account? Sign up", key="switch_to_signup_btn", use_container_width=True):
        st.session_state.auth_mode = 'signup'
        st.rerun()

    if st.button("← Back to Landing", key="back_to_landing", use_container_width=True):
        st.session_state.auth_mode = 'landing'
        st.rerun()

def render_signup_view(repo):
    st.markdown('<h2 style="color: white; font-size: 1.8rem; font-weight: 800; margin-bottom: 2rem;">Create your account</h2>', unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="Choose a username", key="signup_user")
    email = st.text_input("Email", placeholder="name@company.com", key="signup_email")
    password = st.text_input("Password", type="password", placeholder="Create a strong password", key="signup_pwd")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat your password", key="signup_confirm")
    
    if st.button("Create account", key="signup_submit", type="primary", use_container_width=True):
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
            
        with st.spinner("Securing your profile..."):
            user = repo.create_user(username, email, password)
            if user:
                st.session_state.user = user
                st.success("Account created successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("An error occurred. Username or email might be taken.")

    if st.button("← Already have an account? Sign in", key="back_to_login_signup", use_container_width=True):
        st.session_state.auth_mode = 'login'
        st.rerun()

def handle_social_login(provider, repo):
    with st.spinner(f"Connecting to {provider}..."):
        time.sleep(1.5) # Simulate OAuth
        user = repo.handle_social_login(provider)
        if user:
            st.session_state.user = user
            st.success(f"Successfully connected with {provider}!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error(f"Failed to connect with {provider}.")
