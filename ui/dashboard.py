import streamlit as st
from database.repository import Repository
from ai_engine.rag_engine import RAGEngine
import datetime

def dashboard_page():
    repo = Repository()
    ai = RAGEngine()
    user = st.session_state.user

    # Layout: 3 Columns
    col_nav, col_main, col_side = st.columns([0.8, 2, 1.2])

    # --- LEFT COLUMN: NAVIGATION ---
    with col_nav:
        st.markdown(f"""
            <div class="logo-container" style="font-size: 1.5rem; text-align: left;">MindLoop</div>
            <div style="margin-top: 2rem;">
                <p style="font-weight: 700; color: #8a2be2;">@{user['username']}</p>
                <p style="font-size: 0.8rem; color: #71767b;">{user['xp']} XP • Level {user['xp'] // 100 + 1}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        if st.button("🏠 Home", use_container_width=True): pass
        if st.button("🔍 Explore", use_container_width=True): pass
        if st.button("🔔 Alerts", use_container_width=True): pass
        if st.button("✉️ Messages", use_container_width=True): pass
        if st.button("👤 Profile", use_container_width=True): pass
        
        st.write("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # --- CENTER COLUMN: MAIN FEED ---
    with col_main:
        st.markdown('<h2 style="margin-top: 0;">Main Feed</h2>', unsafe_allow_html=True)
        
        # Post Creator
        with st.container():
            st.markdown('<div class="post-card" style="margin-bottom: 2rem;">', unsafe_allow_html=True)
            new_content = st.text_area("What's on your mind?", height=100, placeholder="Share something new...")
            c1, c2 = st.columns([3, 1])
            with c1:
                subject = st.selectbox("Subject", ["General", "SISR", "SLAM", "Cyber", "Management"], label_visibility="collapsed")
            with c2:
                if st.button("Loop It", kind="primary", use_container_width=True):
                    if new_content:
                        repo.add_post(user['id'], new_content, subject)
                        st.success("Posted!")
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Feed
        feed = repo.get_feed()
        if not feed:
            st.info("The loop is quiet. Be the first to post!")
        else:
            for post in feed:
                st.markdown(f"""
                    <div class="post-card animate-fade">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-weight: 700; color: #8a2be2;">@{post['author_name']}</span>
                            <span style="font-size: 0.8rem; color: #71767b;">{post['subject']}</span>
                        </div>
                        <p style="font-size: 1.1rem; line-height: 1.6;">{post['content']}</p>
                        <div style="margin-top: 1rem; font-size: 0.9rem; color: #71767b;">
                            <span>💬 0</span> &nbsp; <span>🔄 0</span> &nbsp; <span>❤️ 0</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # --- RIGHT COLUMN: TRENDS & AI ---
    with col_side:
        st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0;">Sentient Insights</h3>', unsafe_allow_html=True)
        
        # AI Interaction
        if feed:
            last_post = feed[0]
            ai_comment = ai.generate_augmented_response(last_post['content'], last_post['subject'])
            st.markdown(f"""
                <div style="background: rgba(138, 43, 226, 0.1); border-left: 3px solid #8a2be2; padding: 1rem; border-radius: 8px;">
                    <p style="font-size: 0.9rem; font-style: italic; color: #eff3f4;">
                        "Analyzing latest loop from @{last_post['author_name']}: {ai_comment[:150]}..."
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### Trending Loops")
        trends = [
            {"topic": "#SISR_Exam", "loops": "1.2k"},
            {"topic": "#MindLoopV5", "loops": "850"},
            {"topic": "#CyberSecurity", "loops": "2.1k"},
            {"topic": "#SLAM_Robot", "loops": "400"},
        ]
        for trend in trends:
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <span style="font-weight: 600;">{trend['topic']}</span>
                    <span style="color: #71767b;">{trend['loops']} loops</span>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
