import pyrebase
import os
from dotenv import load_dotenv
import streamlit as st
from google.cloud import firestore
from db import db, init_firestore
import time
import random
import string

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

# Vérifier la configuration Firebase
if not all(firebase_config.values()):
    st.warning("⚠️ Configuration Firebase incomplète. Vérifie ton fichier .env")
else:
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

# S'assurer que Firestore est initialisé
if db is None:
    init_firestore()

# ============================================
# STOCKAGE TEMPORAIRE DES CODES
# ============================================
verification_codes = {}

# ============================================
# CONNEXION AUTOMATIQUE
# ============================================

def auto_login():
    """Vérifie si l'utilisateur a un token valide et le reconnecte automatiquement"""
    if st.session_state.get("user") is not None:
        return True
    
    token = st.session_state.get("firebase_token")
    if token:
        try:
            user = auth.refresh(token)
            if user:
                st.session_state.user = user
                st.session_state.firebase_token = user.get("idToken")
                return True
        except Exception:
            st.session_state.firebase_token = None
            st.session_state.user = None
            return False
    return False

# ============================================
# CONNEXION (avec vérification du compte)
# ============================================

def sign_in(email, password, remember=True):
    """Connecte un utilisateur avec email et mot de passe"""
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        
        # Vérifier si le compte est vérifié
        if db is not None:
            try:
                user_doc = db.collection("users").document(user['localId']).get()
                if user_doc.exists:
                    user_data = user_doc.to_dict()
                    if not user_data.get("verified", False):
                        st.error("❌ Veuillez vérifier votre email avant de vous connecter.")
                        st.info(f"📧 Un code a été envoyé à {email}")
                        # Renvoyer un code si le compte n'est pas vérifié
                        code = generate_verification_code()
                        verification_codes[email] = {
                            "code": code,
                            "timestamp": time.time(),
                            "user_id": user['localId']
                        }
                        send_verification_email(email, code)
                        return None
                    user['name'] = user_data.get('name', email.split('@')[0])
                else:
                    st.error("❌ Utilisateur non trouvé dans Firestore")
                    return None
            except Exception as e:
                st.warning(f"⚠️ Erreur récupération infos : {e}")
        
        # Sauvegarder le token
        if remember:
            st.session_state.firebase_token = user.get("idToken")
        
        st.session_state.user = user
        st.success("✅ Connexion réussie !")
        return user
        
    except Exception as e:
        error_msg = str(e)
        if "EMAIL_NOT_FOUND" in error_msg:
            st.error("❌ Email non trouvé")
        elif "INVALID_PASSWORD" in error_msg:
            st.error("❌ Mot de passe incorrect")
        elif "USER_DISABLED" in error_msg:
            st.error("❌ Compte désactivé")
        else:
            st.error(f"❌ Erreur de connexion : {error_msg}")
        return None

# ============================================
# INSCRIPTION (avec création du document user)
# ============================================

def sign_up(email, password, full_name=""):
    """Crée un nouvel utilisateur (sans vérification)"""
    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        if db is not None:
            try:
                db.collection("users").document(user['localId']).set({
                    "email": email,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "name": full_name or email.split('@')[0],
                    "verified": False  # Compte non vérifié
                })
                st.success("✅ Utilisateur créé dans Firestore")
            except Exception as e:
                st.warning(f"⚠️ Erreur Firestore : {e}")
        
        st.session_state.firebase_token = user.get("idToken")
        user['name'] = full_name or email.split('@')[0]
        st.session_state.user = user
        st.success("✅ Compte créé avec succès !")
        return user
        
    except Exception as e:
        error_msg = str(e)
        if "EMAIL_EXISTS" in error_msg:
            st.error("❌ Cet email est déjà utilisé")
        elif "WEAK_PASSWORD" in error_msg:
            st.error("❌ Mot de passe trop faible (minimum 6 caractères)")
        else:
            st.error(f"❌ Erreur d'inscription : {error_msg}")
        return None

# ============================================
# INSCRIPTION AVEC VÉRIFICATION PAR CODE
# ============================================

def generate_verification_code():
    """Génère un code à 6 chiffres"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code):
    """Envoie un email avec le code de vérification"""
    try:
        from notifications import send_verification_code_email
        return send_verification_code_email(email, code)
    except Exception as e:
        st.error(f"Erreur d'envoi du code : {e}")
        return False

def create_user_with_verification(email, password, full_name=""):
    """Crée un utilisateur et envoie un code de vérification"""
    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        # Créer le document user avec verified=False
        if db is not None:
            try:
                db.collection("users").document(user['localId']).set({
                    "email": email,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "name": full_name or email.split('@')[0],
                    "verified": False
                })
            except Exception as e:
                st.warning(f"⚠️ Erreur Firestore : {e}")
        
        # Générer et stocker le code
        code = generate_verification_code()
        verification_codes[email] = {
            "code": code,
            "timestamp": time.time(),
            "user_id": user['localId']
        }
        
        # Envoyer le code par email
        if send_verification_email(email, code):
            st.success("📧 Un code de vérification a été envoyé à votre email")
            return {"status": "pending", "email": email}
        else:
            return None
            
    except Exception as e:
        error_msg = str(e)
        if "EMAIL_EXISTS" in error_msg:
            st.error("❌ Cet email est déjà utilisé")
        else:
            st.error(f"❌ Erreur : {error_msg}")
        return None

def verify_email_code(email, code):
    """Vérifie le code et active le compte"""
    if email not in verification_codes:
        st.error("❌ Aucun code en attente pour cet email")
        return False
    
    stored_data = verification_codes[email]
    
    # Expiration (10 minutes)
    if time.time() - stored_data["timestamp"] > 600:
        del verification_codes[email]
        st.error("❌ Le code a expiré. Veuillez réessayer.")
        return False
    
    if stored_data["code"] == code:
        user_id = stored_data["user_id"]
        if db is not None:
            try:
                db.collection("users").document(user_id).update({
                    "verified": True,
                    "verified_at": firestore.SERVER_TIMESTAMP
                })
            except Exception as e:
                st.error(f"❌ Erreur activation compte : {e}")
                return False
        
        # Supprimer le code stocké
        del verification_codes[email]
        st.success("✅ Compte vérifié avec succès !")
        return True
    else:
        st.error("❌ Code incorrect")
        return False

def update_verification_code(email):
    """Génère un nouveau code et le renvoie par email"""
    if email not in verification_codes:
        st.error("❌ Aucune demande en attente pour cet email")
        return False
    
    # Générer un nouveau code
    new_code = generate_verification_code()
    verification_codes[email].update({
        "code": new_code,
        "timestamp": time.time()
    })
    
    # Envoyer le nouveau code
    if send_verification_email(email, new_code):
        st.success("📧 Nouveau code envoyé !")
        return True
    else:
        st.error("❌ Erreur d'envoi du nouveau code")
        return False

# ============================================
# DÉCONNEXION ET UTILITAIRES
# ============================================

def sign_out():
    """Déconnecte l'utilisateur"""
    try:
        st.session_state.user = None
        st.session_state.firebase_token = None
        if "booking_data" in st.session_state:
            del st.session_state.booking_data
        st.success("🔒 Déconnecté avec succès")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Erreur lors de la déconnexion : {e}")

def get_user():
    """Retourne l'utilisateur connecté"""
    if "user" in st.session_state and st.session_state.user is not None:
        return st.session_state.user
    return None

def is_authenticated():
    """Vérifie si l'utilisateur est connecté"""
    return st.session_state.get("user") is not None

def get_user_id():
    """Retourne l'ID de l'utilisateur connecté"""
    user = get_user()
    if user:
        return user.get('localId')
    return None

def refresh_token(token):
    """Rafraîchit le token d'authentification"""
    try:
        user = auth.refresh(token)
        return user
    except Exception:
        return None