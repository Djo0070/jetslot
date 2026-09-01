import streamlit as st

def show():
    st.markdown("<h1 style='text-align: center;'>📋 Informations et Tarifs</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### ✈️ Aviation Privée
    
    | Type de jet | Capacité | Prix par place (1h) | Prix total |
    |-------------|----------|---------------------|------------|
    | **Jet léger** (Citation CJ3) | 6 places | 350 € | 2 100 € |
    | **Jet moyen** (Falcon 2000) | 8 places | 600 € | 4 800 € |
    | **Jet long-courrier** (Gulfstream G650) | 14 places | 1 200 € | 16 800 € |
    
    ### 🚤 Yacht
    
    | Type de yacht | Capacité | Prix par place (1/2 journée) | Prix total |
    |---------------|----------|------------------------------|------------|
    | **Yacht standard** | 10 places | 150 € | 1 500 € |
    | **Yacht de luxe** | 12 places | 400 € | 4 800 € |
    | **Super yacht** | 20 places | 800 € | 16 000 € |
    
    ### 💳 Commission JetSlot
    
    JetSlot prélève une commission de **5%** sur chaque réservation.
    
    | Prix réservation | Commission JetSlot | Revenu prestataire |
    |------------------|-------------------|-------------------|
    | 350 € | 17,50 € | 332,50 € |
    | 600 € | 30 € | 570 € |
    | 1 200 € | 60 € | 1 140 € |
    | 2 100 € | 105 € | 1 995 € |
    
    ### 📝 Conditions générales
    
    - 🔒 Paiement sécurisé par Stripe
    - 📧 Confirmation par email immédiate
    - 🕐 Annulation possible jusqu'à 48h avant
    - 💳 Paiement en ligne obligatoire pour valider la réservation
    """)