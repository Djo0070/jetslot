import streamlit as st
import datetime

def show():
    # ============================================
    # CSS PERSONNALISÉ
    # ============================================
    st.markdown("""
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .settings-container {
            animation: fadeIn 0.5s ease-out;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px 0;
        }
        
        .settings-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 215, 0, 0.1);
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .settings-header h1 {
            color: #FFD700;
            font-size: 28px;
            font-weight: 300;
            letter-spacing: 2px;
            margin: 0;
        }
        
        .settings-header span {
            color: #B8C6E0;
            font-size: 14px;
            opacity: 0.6;
        }
        
        .settings-section {
            background: rgba(26, 42, 74, 0.4);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 215, 0, 0.05);
            transition: all 0.3s ease;
        }
        
        .settings-section:hover {
            border-color: rgba(255, 215, 0, 0.15);
            background: rgba(26, 42, 74, 0.6);
        }
        
        .settings-section-title {
            color: #FFD700;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 1px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .settings-section-title .icon {
            font-size: 18px;
        }
        
        .settings-option {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.03);
        }
        
        .settings-option:last-child {
            border-bottom: none;
        }
        
        .settings-option-label {
            color: #E8EAF0;
            font-size: 14px;
        }
        
        .settings-option-description {
            color: #6C6F78;
            font-size: 12px;
            margin-top: 2px;
        }
        
        .settings-option-control {
            min-width: 100px;
            text-align: right;
        }
        
        .settings-divider {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
            margin: 20px 0;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #FFD700, #F4A460) !important;
            color: #0A1628 !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 20px !important;
            font-size: 14px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton button:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2) !important;
        }
        
        .stButton button:active {
            transform: scale(0.98) !important;
        }
        
        .danger-zone {
            border-color: rgba(255, 68, 68, 0.2) !important;
        }
        
        .danger-zone:hover {
            border-color: rgba(255, 68, 68, 0.4) !important;
        }
        
        .danger-zone .settings-section-title {
            color: #FF4444 !important;
        }
        
        /* Toggle Switch */
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 44px;
            height: 24px;
        }
        
        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #2A3A5A;
            transition: 0.3s;
            border-radius: 24px;
        }
        
        .toggle-slider:before {
            position: absolute;
            content: "";
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background-color: #6C6F78;
            transition: 0.3s;
            border-radius: 50%;
        }
        
        .toggle-switch input:checked + .toggle-slider {
            background-color: #FFD700;
        }
        
        .toggle-switch input:checked + .toggle-slider:before {
            transform: translateX(20px);
            background-color: #0A1628;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ============================================
    # EN-TÊTE
    # ============================================
    st.markdown("""
    <div class="settings-container">
        <div class="settings-header">
            <h1>⚙️ Paramètres</h1>
            <span>JetSlot v1.0</span>
        </div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # SECTION 1 : PROFIL
    # ============================================
    st.markdown("""
    <div class="settings-section">
        <div class="settings-section-title">
            <span class="icon">👤</span> Profil
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        display_name = st.text_input("Nom d'affichage", value=st.session_state.user.get('name', '') if st.session_state.user else "")
    
    with col2:
        email = st.text_input("Email", value=st.session_state.user.get('email', '') if st.session_state.user else "", disabled=True)
    
    if st.button("Mettre à jour le profil"):
        st.success("✅ Profil mis à jour !")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 2 : PRÉFÉRENCES
    # ============================================
    st.markdown("""
    <div class="settings-section">
        <div class="settings-section-title">
            <span class="icon">🎨</span> Préférences
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div>
            <div class="settings-option-label">Mode sombre</div>
            <div class="settings-option-description">Activer le thème sombre (recommandé)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; justify-content: flex-end;">
            <label class="toggle-switch">
                <input type="checkbox" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="settings-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div>
            <div class="settings-option-label">Notifications par email</div>
            <div class="settings-option-description">Recevoir les notifications de réservation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; justify-content: flex-end;">
            <label class="toggle-switch">
                <input type="checkbox" checked>
                <span class="toggle-slider"></span>
            </label>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="settings-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div>
            <div class="settings-option-label">Langue</div>
            <div class="settings-option-description">Langue de l'application</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        lang = st.selectbox("", ["Français", "English", "العربية"], label_visibility="collapsed")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 3 : SÉCURITÉ
    # ============================================
    st.markdown("""
    <div class="settings-section">
        <div class="settings-section-title">
            <span class="icon">🔒</span> Sécurité
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div>
            <div class="settings-option-label">Double authentification</div>
            <div class="settings-option-description">Activer la sécurité renforcée</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; justify-content: flex-end;">
            <label class="toggle-switch">
                <input type="checkbox">
                <span class="toggle-slider"></span>
            </label>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="settings-divider"></div>', unsafe_allow_html=True)
    
    if st.button("🔑 Changer le mot de passe"):
        st.info("Fonctionnalité à venir")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 4 : ZONE DANGEREUSE
    # ============================================
    st.markdown("""
    <div class="settings-section danger-zone">
        <div class="settings-section-title">
            <span class="icon">⚠️</span> Zone dangereuse
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div>
            <div class="settings-option-label" style="color: #FF4444;">Supprimer le compte</div>
            <div class="settings-option-description">Cette action est irréversible</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🗑️ Supprimer", use_container_width=True):
            st.error("❌ Cette action est désactivée en mode démo")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # ============================================
    # SECTION 5 : INFORMATIONS
    # ============================================
    st.markdown("""
    <div class="settings-section">
        <div class="settings-section-title">
            <span class="icon">ℹ️</span> Informations
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <p style="color:#6C6F78;font-size:13px;">
            <strong style="color:#B8C6E0;">Version</strong><br>
            1.0.0
        </p>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <p style="color:#6C6F78;font-size:13px;">
            <strong style="color:#B8C6E0;">Membre depuis</strong><br>
            {datetime.datetime.now().strftime("%d %B %Y")}
        </p>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style="color:#4A4F58;font-size:11px;text-align:center;margin-top:10px;">
            JetSlot Technologies © 2026
        </p>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)