import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")

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
            success_url=success_url or "https://ton-site.com/success",
            cancel_url=cancel_url or "https://ton-site.com/cancel",
            metadata={
                "booking_id": booking_id
            }
        )
        return session
    except stripe.error.StripeError as e:
        print(f"❌ Erreur Stripe Checkout : {e}")
        return None