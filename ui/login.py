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
    
    # Session state for switching between landing, login and signup
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'landing'
    
    # Custom Header Removal
    st.markdown("""
        <style>
            [data-testid="stHeader"] {visibility: hidden;}
            .block-container {padding-top: 1rem;}
        </style>
    """, unsafe_allow_html=True)

    # Main Auth Container
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Logo & Hero
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, "logo.png")
    logo_base64 = get_base64_image(logo_path)
    
    if logo_base64:
        st.markdown(f'''
            <div class="logo-wrapper">
                <img src="data:image/png;base64,{logo_base64}" style="width: 80px; margin-bottom: 2rem;">
                <h1 class="hero-title">MindLoop</h1>
                <p class="hero-subtitle">Connect with your digital reflection.</p>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="logo-wrapper">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🧠</div>
                <h1 class="hero-title">MindLoop</h1>
                <p class="hero-subtitle">Connect with your digital reflection.</p>
            </div>
        ''', unsafe_allow_html=True)

    # --- LANDING STATE ---
    if st.session_state.auth_mode == 'landing':
        st.markdown('<h2 style="color: white; font-size: 2rem; font-weight: 800; margin-bottom: 2.5rem; text-align: center; letter-spacing: -0.04em;">Ça se passe maintenant.</h2>', unsafe_allow_html=True)
        
        # Social Buttons
        if st.button("S'inscrire avec Google", key="landing_google", use_container_width=True):
            handle_social_login("Google", repo)
            
        if st.button("S'inscrire avec Apple", key="landing_apple", use_container_width=True):
            handle_social_login("Apple", repo)
            
        st.markdown('<div class="divider">ou</div>', unsafe_allow_html=True)
        
        if st.button("Créer un compte", key="go_signup", type="primary", use_container_width=True):
            st.session_state.auth_mode = 'signup'
            st.rerun()
            
        st.markdown('<p style="font-size: 0.7rem; color: #71767b; margin-top: 0.5rem;">En vous inscrivant, vous acceptez les Conditions d\'utilisation et la Politique de confidentialité.</p>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: 4rem;">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem;">Vous avez déjà un compte ?</p>', unsafe_allow_html=True)
        if st.button("Se connecter", key="go_login", use_container_width=True):
            st.session_state.auth_mode = 'login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- LOGIN STATE ---
    elif st.session_state.auth_mode == 'login':
        st.markdown('<h2 style="color: white; font-size: 1.8rem; font-weight: 800; margin-bottom: 2rem; text-align: left;">Connectez-vous à MindLoop</h2>', unsafe_allow_html=True)
        
        if st.button("Continuer avec Google", key="login_google", use_container_width=True):
            handle_social_login("Google", repo)
            
        if st.button("Continuer avec Apple", key="login_apple", use_container_width=True):
            handle_social_login("Apple", repo)
            
        st.markdown('<div class="divider">ou</div>', unsafe_allow_html=True)
        
        render_login_form(repo)
        
        if st.button("Retour", key="back_to_landing_l", kind="secondary"):
            st.session_state.auth_mode = 'landing'
            st.rerun()

    # --- SIGNUP STATE ---
    elif st.session_state.auth_mode == 'signup':
        st.markdown('<h2 style="color: white; font-size: 1.8rem; font-weight: 800; margin-bottom: 2rem; text-align: left;">Créer votre compte</h2>', unsafe_allow_html=True)
        render_signup_form(repo)
        
        if st.button("Retour", key="back_to_landing_s", kind="secondary"):
            st.session_state.auth_mode = 'landing'
            st.rerun()

    # Security Badge
    st.markdown('''
        <div class="security-badge">
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 1rem;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <span>Chiffrement de niveau entreprise</span>
            </div>
            <span>MindLoop Pro © 2026</span><br>
            <div style="margin-top: 10px; display: flex; justify-content: center; gap: 20px;">
                <a href="#">Conditions</a>
                <a href="#">Confidentialité</a>
                <a href="#">Cookies</a>
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
