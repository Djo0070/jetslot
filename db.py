import datetime
import os
import json
import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account

# --- Initialisation de Firestore ---
db = None
 
def init_firestore():
    """Initialise la connexion à Firestore"""
    global db
    
    # Méthode 1 : via fichier JSON local (développement)
    cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
    if os.path.exists(cred_path):
        try:
            cred = service_account.Credentials.from_service_account_file(cred_path)
            db = firestore.Client(credentials=cred, project="aneyond-3bbc5")
            st.success("✅ Firestore connecté (fichier local)")
            return True
        except Exception as e:
            st.warning(f"Erreur Firestore (fichier) : {e}")
    
    # Méthode 2 : via st.secrets (Streamlit Cloud) ou variable d'environnement
    firebase_cred_str = None
    
    # 2a : Essayer depuis st.secrets (Streamlit Cloud)
    if hasattr(st, 'secrets'):
        firebase_cred_str = st.secrets.get("FIREBASE_SERVICE_ACCOUNT")
    
    # 2b : Si pas trouvé, essayer depuis os.getenv (développement local avec .env)
    if not firebase_cred_str:
        firebase_cred_str = os.getenv("FIREBASE_SERVICE_ACCOUNT")
    
    if firebase_cred_str:
        try:
            # Nettoyer la chaîne : enlever les guillemets simples superflus
            firebase_cred_str = firebase_cred_str.strip()
            # Si la chaîne commence par des guillemets simples, les remplacer par des doubles
            if firebase_cred_str.startswith("'") and firebase_cred_str.endswith("'"):
                firebase_cred_str = firebase_cred_str[1:-1]
            # Remplacer les guillemets simples à l'intérieur (mais normalement c'est du JSON valide)
            # Essayer de parser directement
            firebase_cred = json.loads(firebase_cred_str)
            cred = service_account.Credentials.from_service_account_info(firebase_cred)
            db = firestore.Client(credentials=cred, project=firebase_cred["project_id"])
            st.success("✅ Firestore connecté (secret)")
            return True
        except json.JSONDecodeError as e:
            st.warning(f"Erreur de parsing JSON (secret) : {e}")
            # Tentative de réparation : remplacer les \n par des retours à la ligne réels
            try:
                # Si le JSON a des \n littéraux, on les remplace par des vrais sauts de ligne
                fixed_str = firebase_cred_str.replace('\\n', '\n')
                firebase_cred = json.loads(fixed_str)
                cred = service_account.Credentials.from_service_account_info(firebase_cred)
                db = firestore.Client(credentials=cred, project=firebase_cred["project_id"])
                st.success("✅ Firestore connecté (secret réparé)")
                return True
            except Exception as e2:
                st.warning(f"Erreur de réparation JSON : {e2}")
        except Exception as e:
            st.warning(f"Erreur Firestore (secret) : {e}")
    
    # Si rien ne fonctionne, mode simulation
    st.warning("⚠️ Firestore non configuré. Mode simulation (données non persistantes).")
    db = None
    return False

# Initialiser au chargement
init_firestore()

# Statuts possibles pour une réservation
STATUS = {
    "pending": "En attente de validation",
    "confirmed": "Confirmée",
    "refused": "Refusée",
    "cancelled": "Annulée"
}


# --- FONCTIONS RÉSERVATIONS ---
def get_bookings(user_id):
    """Récupère les réservations d'un utilisateur"""
    if not user_id:
        st.error("❌ user_id manquant")
        return []
    
    # Mode simulation - Données factices
    if db is None:
        st.info("🔧 Mode simulation - Réservations factices")
        return [
            {
                "id": "sim1",
                "userId": user_id,
                "type": "Aviation (Jet)",
                "location": "Nice Côte d'Azur (NCE) - France",
                "date": "2026-07-20",
                "time": "10:30",
                "duration": 60,
                "status": "confirmed"
            },
            {
                "id": "sim2",
                "userId": user_id,
                "type": "Maritime (Yacht)",
                "location": "Port de Monaco - Monaco",
                "date": "2026-07-25",
                "time": "14:00",
                "duration": 120,
                "status": "pending"
            }
            
        ]
    
    try:
        # Récupérer toutes les réservations de l'utilisateur
        bookings_ref = db.collection("bookings").where("userId", "==", user_id)
        bookings = bookings_ref.stream()
        
        result = []
        for b in bookings:
            data = b.to_dict()
            data["id"] = b.id
            result.append(data)
        
        # Trier par date (plus récent d'abord)
        result.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        if result:
            st.success(f"✅ {len(result)} réservation(s) trouvée(s)")
        else:
            st.info("📭 Aucune réservation trouvée dans Firestore")
        
        return result
        
    except Exception as e:
        st.error(f"❌ Erreur de récupération des réservations : {e}")
        return []

def create_booking(user_id, booking_type, location, date, time, duration=60):
    """Crée une nouvelle réservation"""
    if not user_id:
        st.error("❌ Utilisateur non connecté")
        return None
    
    # Récupérer l'email de l'utilisateur
    user_email = None
    user_name = "Client"
    
    if st.session_state.user:
        user_email = st.session_state.user.get("email")
        if user_email:
            user_name = user_email.split('@')[0]
    
    # Préparer les données
    booking_data = {
        "userId": user_id,
        "type": booking_type,
        "location": location,
        "date": date,
        "time": time,
        "duration": duration,
        "status": "pending"
    }
    
    # --- Mode simulation ---
    if db is None:
        import random
        import string
        booking_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        booking_data["id"] = booking_id
        st.info(f"🔧 [SIMULATION] Réservation créée : {booking_id}")
        
        # Envoyer email en simulation
        if user_email:
            try:
                from notifications import send_confirmation_email
                send_confirmation_email(user_email, booking_data)
            except Exception as e:
                st.warning(f"⚠️ Erreur email (simu) : {e}")
        
        return booking_id
    
    # --- Mode réel (Firestore) ---
    try:
        # Ajouter created_at seulement si Firestore est connecté
        booking_data["created_at"] = firestore.SERVER_TIMESTAMP
        
        doc_ref = db.collection("bookings").document()
        doc_ref.set(booking_data)
        booking_id = doc_ref.id
        
        st.success(f"✅ Réservation #{booking_id} sauvegardée dans Firestore")
        
        # Envoyer email de confirmation
        if user_email:
            try:
                from notifications import send_confirmation_email
                booking_data["id"] = booking_id
                booking_data["user_name"] = user_name
                send_confirmation_email(user_email, booking_data)
            except Exception as e:
                st.warning(f"⚠️ Erreur email : {e}")
        
        return booking_id
        
    except Exception as e:
        st.error(f"❌ Erreur de création dans Firestore : {e}")
        return None

def cancel_booking(booking_id, user_id):
    """Annule une réservation"""
    if not booking_id:
        st.error("❌ ID de réservation manquant")
        return False
    
    if not user_id:
        st.error("❌ Utilisateur non identifié")
        return False
    
    # Mode simulation
    if db is None:
        st.info("🔧 [SIMULATION] Annulation effectuée")
        return True
    
    try:
        # Récupérer la réservation
        booking_ref = db.collection("bookings").document(booking_id)
        booking = booking_ref.get()
        
        if not booking.exists:
            st.error(f"❌ Réservation #{booking_id} introuvable dans Firestore")
            return False
        
        booking_data = booking.to_dict()
        
        # Vérifier les permissions
        if booking_data.get("userId") != user_id:
            st.error("⛔ Vous n'êtes pas autorisé à annuler cette réservation")
            return False
        
        # Vérifier si déjà annulée
        if booking_data.get("status") == "cancelled":
            st.warning("ℹ️ Cette réservation est déjà annulée")
            return True
        
        # Annuler
        booking_ref.update({
            "status": "cancelled",
            "cancelled_at": firestore.SERVER_TIMESTAMP
        })
        
        st.success(f"✅ Réservation #{booking_id} annulée dans Firestore")
        return True
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'annulation : {e}")
        return False

def refuse_booking(booking_id, user_id):
    """Refuse une réservation"""
    if not booking_id or not user_id:
        return False
    
    if db is None:
        return False
    
    try:
        booking_ref = db.collection("bookings").document(booking_id)
        booking = booking_ref.get()
        
        if not booking.exists:
            return False
        
        booking_data = booking.to_dict()
        if booking_data.get("userId") != user_id:
            return False
        
        booking_ref.update({
            "status": "refused",
            "refused_at": firestore.SERVER_TIMESTAMP
        })
        
        # Envoyer email de refus au client
        user_email = st.session_state.user.get('email')
        if user_email:
            from notifications import send_refused_email
            booking_data["id"] = booking_id
            send_refused_email(user_email, booking_data)
        
        return True
    except Exception as e:
        st.error(f"Erreur refus : {e}")
        return False    

def confirm_booking_after_payment(booking_id, user_id):
    """Confirme une réservation APRÈS paiement réussi"""
    if db is None:
        return False
    
    try:
        booking_ref = db.collection("bookings").document(booking_id)
        booking = booking_ref.get()
        
        if not booking.exists:
            return False
        
        booking_data = booking.to_dict()
        if booking_data.get("userId") != user_id:
            return False
        
        # Mettre à jour le statut
        booking_ref.update({
            "status": "confirmed",
            "confirmed_at": firestore.SERVER_TIMESTAMP
        })
        
        # Générer le QR Code
        from utils.qr_generator import generate_qr_code
        from notifications import send_confirmed_email_with_qr
        
        qr_data = f"""
JETSLOT - RESERVATION
ID: {booking_id}
Type: {booking_data.get('type', '')}
Lieu: {booking_data.get('location', '')}
Date: {booking_data.get('date', '')} a {booking_data.get('time', '')}
"""
        qr_base64 = generate_qr_code(qr_data)
        
        # Envoyer email avec QR
        user_email = st.session_state.user.get('email')
        if user_email:
            booking_data["id"] = booking_id
            booking_data["booking_id"] = booking_id
            send_confirmed_email_with_qr(user_email, booking_data, qr_base64)
        
        return True
    except Exception as e:
        st.error(f"Erreur confirmation : {e}")
        return False

def create_user_document(user_id, email, name):
    """Crée un document utilisateur dans Firestore avec verified=False"""
    if db is None:
        return False
    
    try:
        db.collection("users").document(user_id).set({
            "email": email,
            "name": name,
            "verified": False,
            "created_at": firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        st.error(f"Erreur création utilisateur : {e}")
        return False
    

def is_user_verified(user_id):
    """Vérifie si un utilisateur a validé son email"""
    if db is None:
        return False
    
    try:
        user_doc = db.collection("users").document(user_id).get()
        if user_doc.exists:
            data = user_doc.to_dict()
            return data.get("verified", False)
        return False
    except Exception as e:
        st.error(f"Erreur vérification : {e}")
        return False

def verify_user(user_id):
    """Marque l'utilisateur comme vérifié"""
    if db is None:
        return False
    
    try:
        db.collection("users").document(user_id).update({
            "verified": True,
            "verified_at": firestore.SERVER_TIMESTAMP
        })
        return True
    except Exception as e:
        st.error(f"Erreur vérification : {e}")
        return False
    

# ============================================
# FIDÉLITÉ
# ============================================

def update_loyalty_level(user_id):
    """Met à jour le niveau de fidélité d'un utilisateur"""
    if db is None:
        return None
    
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        
        if not user.exists:
            return None
        
        user_data = user.to_dict()
        total_bookings = user_data.get("loyalty", {}).get("total_bookings", 0)
        
        # Déterminer le niveau
        if total_bookings >= 30:
            level = "Platinum"
            discount = 15
        elif total_bookings >= 15:
            level = "Gold"
            discount = 10
        elif total_bookings >= 5:
            level = "Silver"
            discount = 5
        else:
            level = "Bronze"
            discount = 0
        
        # Mettre à jour
        user_ref.update({
            "loyalty.level": level,
            "loyalty.discount": discount,
        })
        
        return {"level": level, "discount": discount}
        
    except Exception as e:
        st.error(f"Erreur mise à jour fidélité : {e}")
        return None

def add_miles(user_id, booking_price):
    """Ajoute des miles à un utilisateur (100 miles = 1€ réservé)"""
    if db is None:
        return False
    
    try:
        miles_to_add = int(booking_price * 100 / 10)  # 100 miles pour 10€
        
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        
        if not user.exists:
            return False
        
        current_miles = user.to_dict().get("loyalty", {}).get("miles", 0)
        
        user_ref.update({
            "loyalty.miles": current_miles + miles_to_add,
            "loyalty.total_bookings": firestore.Increment(1)
        })
        
        # Mettre à jour le niveau
        update_loyalty_level(user_id)
        
        return True
        
    except Exception as e:
        st.error(f"Erreur ajout miles : {e}")
        return False

def get_loyalty_card(user_id):
    """Récupère les infos de fidélité d'un utilisateur"""
    if db is None:
        return None
    
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        
        if not user.exists:
            return None
        
        user_data = user.to_dict()
        loyalty = user_data.get("loyalty", {})
        
        return {
            "name": user_data.get("name", "Client"),
            "email": user_data.get("email", ""),
            "level": loyalty.get("level", "Bronze"),
            "total_bookings": loyalty.get("total_bookings", 0),
            "miles": loyalty.get("miles", 0),
            "discount": loyalty.get("discount", 0),
            "member_since": loyalty.get("member_since", ""),
            "next_level": get_next_level_info(loyalty.get("total_bookings", 0))
        }
        
    except Exception as e:
        st.error(f"Erreur récupération carte : {e}")
        return None

def get_next_level_info(total_bookings):
    """Retourne les infos du prochain niveau"""
    levels = [
        {"name": "Silver", "bookings_needed": 5, "discount": 5},
        {"name": "Gold", "bookings_needed": 15, "discount": 10},
        {"name": "Platinum", "bookings_needed": 30, "discount": 15},
    ]
    
    for level in levels:
        if total_bookings < level["bookings_needed"]:
            return {
                "level": level["name"],
                "bookings_needed": level["bookings_needed"],
                "bookings_remaining": level["bookings_needed"] - total_bookings,
                "discount": level["discount"]
            }
    
    return None

def initialize_loyalty(user_id):
    """Initialise le champ fidélité pour un utilisateur"""
    if db is None or not user_id:
        return False
    
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        
        # Si le document n'existe pas, le créer
        if not user.exists:
            user_ref.set({
                "loyalty": {
                    "level": "Bronze",
                    "total_bookings": 0,
                    "miles": 0,
                    "discount": 0,
                    "member_since": datetime.datetime.now().strftime("%d/%m/%Y")
                }
            })
            return True
        
        # Si le document existe, vérifier si loyalty existe déjà
        user_data = user.to_dict()
        if "loyalty" in user_data and user_data["loyalty"]:
            return True
        
        # Ajouter le champ loyalty avec merge=True (ne supprime pas les autres champs)
        user_ref.set({
            "loyalty": {
                "level": "Bronze",
                "total_bookings": 0,
                "miles": 0,
                "discount": 0,
                "member_since": datetime.datetime.now().strftime("%d/%m/%Y")
            }
        }, merge=True)
        return True
        
    except Exception as e:
        st.error(f"Erreur initialisation fidélité : {e}")
        return False