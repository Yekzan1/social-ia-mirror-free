import streamlit as st
import random

def render_mirror_status(username):
    st.markdown("### 🧬 VOTRE MIROIR")
    
    # Simulation d'état du Miroir IA
    moods = ["Analytique", "Créatif", "Observateur", "Productif", "En veille"]
    status = random.choice(moods)
    synchro = random.randint(85, 99)
    
    st.markdown(f"""
    <div class='glass-panel'>
        <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 15px;'>
            <div style='position: relative;'>
                <div style='width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #a855f7); display: flex; align-items: center; justify-content: center; font-size: 1.5rem;'>
                    👤
                </div>
                <div style='position: absolute; bottom: 0; right: 0; width: 12px; height: 12px; border-radius: 50%; background: #10b981; border: 2px solid #030712;'></div>
            </div>
            <div>
                <div style='font-weight: 800; font-size: 0.9rem;'>Miroir_{username}</div>
                <div style='font-size: 0.7rem; color: #10b981;'>SYNCHRONISÉ</div>
            </div>
        </div>
        
        <div style='margin-top: 10px;'>
            <div style='display: flex; justify-content: space-between; font-size: 0.75rem; margin-bottom: 5px;'>
                <span style='color: #94a3b8;'>Niveau de Synchro</span>
                <span style='color: #6366f1; font-weight: 700;'>{synchro}%</span>
            </div>
            <div style='width: 100%; height: 4px; background: rgba(255,255,255,0.05); border-radius: 10px;'>
                <div style='width: {synchro}%; height: 100%; background: linear-gradient(90deg, #6366f1, #a855f7); border-radius: 10px;'></div>
            </div>
        </div>
        
        <div style='margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 12px;'>
            <div style='font-size: 0.7rem; color: #64748b; text-transform: uppercase; font-weight: 800;'>État Cognitif</div>
            <div style='font-size: 0.9rem; font-weight: 600; color: #f8fafc;'>{status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
