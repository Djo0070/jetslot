import stripe
import os
from dotenv import load_dotenv
import streamlit as st

# Charger .env en local (ignoré sur Streamlit Cloud)
load_dotenv()

# ============================================
# RÉCUPÉRATION DES CLÉS (local + cloud)
# ============================================

def get_stripe_secret_key():
    """Récupère la clé Stripe depuis st.secrets ou .env"""
    # Priorité 1 : st.secrets (Streamlit Cloud)
    if hasattr(st, 'secrets'):
        try:
            key = st.secrets.get("STRIPE_SECRET_KEY")
            if key:
                return key
        except:
            pass
    
    # Priorité 2 : os.getenv (fichier .env local)
    return os.getenv("STRIPE_SECRET_KEY")

def get_stripe_publishable_key():
    """Récupère la clé publique Stripe depuis st.secrets ou .env"""
    if hasattr(st, 'secrets'):
        try:
            key = st.secrets.get("STRIPE_PUBLISHABLE_KEY")
            if key:
                return key
        except:
            pass
    return os.getenv("STRIPE_PUBLISHABLE_KEY")

# ============================================
# CONFIGURATION STRIPE
# ============================================

# Configuration Stripe (fonctionne local et cloud)
STRIPE_SECRET_KEY = get_stripe_secret_key()
STRIPE_PUBLISHABLE_KEY = get_stripe_publishable_key()

stripe.api_key = STRIPE_SECRET_KEY

# ============================================
# FONCTIONS STRIPE (inchangées)
# ============================================

def create_payment_intent(amount, currency="eur", booking_id=None):
    """
    Crée un PaymentIntent Stripe pour un paiement sécurisé
    
    Args:
        amount (int): Montant en centimes (ex: 1500 = 15€)
        currency (str): Devise (eur, usd, etc.)
        booking_id (str): ID de la réservation (optionnel)
    
    Returns:
        dict: Le PaymentIntent créé, ou None en cas d'erreur
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
            metadata={
                "booking_id": booking_id or "unknown"
            }
        )
        return intent
    except stripe.error.StripeError as e:
        print(f"❌ Erreur Stripe : {e}")
        return None

def create_checkout_session(booking_id, amount, currency="eur", success_url=None, cancel_url=None):
    """
    Crée une session Stripe Checkout (paiement redirigé)
    
    Args:
        booking_id (str): ID de la réservation
        amount (int): Montant en centimes
        currency (str): Devise
        success_url (str): URL après paiement réussi
        cancel_url (str): URL après annulation
    
    Returns:
        dict: La session Stripe, ou None en cas d'erreur
    """
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        "name": f"Réservation JetSlot #{booking_id[:8]}",
                        "description": "Réservation de créneau pour jet privé ou yacht"
                    },
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=success_url or "https://jetslot.streamlit.app/?paiement=success",
            cancel_url=cancel_url or "https://jetslot.streamlit.app/?paiement=cancel",
            metadata={
                "booking_id": booking_id
            }
        )
        return session
    except stripe.error.StripeError as e:
        print(f"❌ Erreur Stripe Checkout : {e}")
        return None