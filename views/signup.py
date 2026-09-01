import streamlit as st
import pyrebase
import os
from dotenv import load_dotenv
import re
import time
import random
import string
from google.cloud import firestore
from db import db
from auth import generate_verification_code, send_verification_email, verify_email_code, create_user_with_verification

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

def show():
    st.markdown("""
    <style>
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .signup-container {
            animation: slideUp 0.6s ease-out;
            max-width: 450px;
            margin: 20px auto;
            padding: 40px;
            background: linear-gradient(135deg, rgba(26, 42, 74, 0.8), rgba(10, 22, 40, 0.95));
            border-radius: 16px;
            border: 1px solid rgba(255, 215, 0, 0.12);
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        
        .signup-title {
            text-align: center;
            color: #FFD700;
            font-size: 28px;
            font-weight: 300;
            letter-spacing: 4px;
            margin-bottom: 5px;
        }
        
        .signup-subtitle {
            text-align: center;
            color: #B8C6E0;
            font-size: 14px;
            opacity: 0.6;
            margin-bottom: 30px;
            letter-spacing: 1px;
        }
        
        .stTextInput > div > div > input {
            background: rgba(10, 22, 40, 0.8) !important;
            border: 1px solid rgba(255, 215, 0, 0.15) !important;
            border-radius: 8px !important;
            color: #E8EAF0 !important;
            padding: 12px 15px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #FFD700 !important;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.05) !important;
        }
        
        .stButton button {
            background: #FFD700 !important;
            color: #0A1628 !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 16px !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        
        .stButton button:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 4px 30px rgba(255, 215, 0, 0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="signup-container">
        <div class="signup-title">✈️ JetSlot</div>
        <div class="signup-subtitle">Connectez-vous ou creez un compte</div>
    """, unsafe_allow_html=True)
    
    # ============================================
    # TABS : CONNEXION / INSCRIPTION
    # ============================================
    tab1, tab2 = st.tabs(["🔑 Se connecter", "📝 Creer un compte"])
    
    # ============================================
    # TAB 1 : CONNEXION
    # ============================================
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="jean@jetslot.com")
            password = st.text_input("Mot de passe", type="password", placeholder="Votre mot de passe")
            
            remember = st.checkbox("🔒 Se souvenir de moi", value=True)
            
            submitted_login = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submitted_login:
                if not email or not password:
                    st.error("❌ Veuillez remplir tous les champs")
                else:
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        
                        if remember:
                            st.session_state.firebase_token = user.get("idToken")
                        
                        if db is not None:
                            try:
                                user_doc = db.collection("users").document(user['localId']).get()
                                if user_doc.exists:
                                    user_data = user_doc.to_dict()
                                    user['name'] = user_data.get('name', email.split('@')[0])
                            except:
                                pass
                        
                        st.session_state.user = user
                        st.success("✅ Connexion réussie !")
                        st.rerun()
                    except Exception as e:
                        error_msg = str(e)
                        if "EMAIL_NOT_FOUND" in error_msg:
                            st.error("❌ Email non trouve")
                        elif "INVALID_PASSWORD" in error_msg:
                            st.error("❌ Mot de passe incorrect")
                        else:
                            st.error(f"❌ Erreur : {error_msg}")
    
    # ============================================
    # TAB 2 : INSCRIPTION
    # ============================================
    with tab2:
        # Si une vérification est en cours, afficher le formulaire de code
        if st.session_state.get("show_verification"):
            st.markdown("### ✅ Vérification du compte")
            st.info(f"📧 Un code a été envoyé à {st.session_state.pending_email}")
            
            code = st.text_input("Code de vérification (6 chiffres)", max_chars=6)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Vérifier", use_container_width=True):
                    if verify_email_code(st.session_state.pending_email, code):
                        st.session_state.show_verification = False
                        st.session_state.pending_email = None
                        st.success("✅ Compte activé ! Vous pouvez maintenant vous connecter.")
                        st.rerun()
            
            with col2:
                if st.button("Renvoyer le code", use_container_width=True):
                    # Générer un nouveau code
                    new_code = generate_verification_code()
                    # Mettre à jour le code dans le stockage (via la fonction dédiée)
                    from auth import update_verification_code
                    update_verification_code(st.session_state.pending_email, new_code)
                    send_verification_email(st.session_state.pending_email, new_code)
                    st.success("📧 Nouveau code envoyé !")
            return  # Ne pas afficher le formulaire d'inscription
        
        # Sinon afficher le formulaire d'inscription
        with st.form("signup_form"):
            full_name = st.text_input("Nom complet", placeholder="Jean Dupont")
            email = st.text_input("Adresse email", placeholder="jean@jetslot.com")
            password = st.text_input("Mot de passe", type="password", placeholder="Minimum 6 caracteres")
            confirm = st.text_input("Confirmer", type="password", placeholder="Retapez votre mot de passe")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                accept = st.checkbox("")
            with col2:
                st.markdown("""
                <span style="color:#B8C6E0;font-size:13px;">
                    J'accepte les <a href="#" style="color:#FFD700;text-decoration:none;">conditions generales</a>
                </span>
                """, unsafe_allow_html=True)
            
            submitted_signup = st.form_submit_button("Creer mon compte", use_container_width=True)
            
            if submitted_signup:
                if not full_name:
                    st.error("❌ Veuillez entrer votre nom")
                elif not email:
                    st.error("❌ Veuillez entrer votre email")
                elif len(password) < 6:
                    st.error("❌ Mot de passe trop court (minimum 6 caracteres)")
                elif password != confirm:
                    st.error("❌ Les mots de passe ne correspondent pas")
                elif not accept:
                    st.error("❌ Vous devez accepter les conditions")
                else:
                    # Appeler la fonction qui crée l'utilisateur et envoie le code
                    result = create_user_with_verification(email, password, full_name)
                    if result and result.get("status") == "pending":
                        st.session_state.pending_email = email
                        st.session_state.show_verification = True
                        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)