import streamlit as st
from db import create_booking, confirm_booking_after_payment
import random
import datetime as dt
import string
from utils.map_utils import display_location_map
from utils.qr_generator import generate_qr_code
from stripe_config import create_checkout_session
from notifications import send_pending_email, send_confirmed_email_with_qr




def show():
    # ============================================
    # CSS MINIMALISTE
    # ============================================
    st.markdown("""
    <style>
        h1, h2, h3 { color: #FFD700 !important; font-family: 'Georgia', serif !important; font-weight: 300 !important; letter-spacing: 2px !important; }
        p, div, span, label { color: #E8EAF0 !important; font-family: 'Arial', sans-serif !important; }
        .card { background: rgba(26, 42, 74, 0.5) !important; border: 1px solid rgba(255, 215, 0, 0.1) !important; border-radius: 12px !important; padding: 20px !important; }
        .stButton button { background: #FFD700 !important; color: #0A1628 !important; font-weight: 600 !important; border: none !important; border-radius: 8px !important; padding: 12px 30px !important; }
        .stButton button:hover { background: #F4A460 !important; }
        .qr-container { background: #0A1628; padding: 20px; border-radius: 12px; border: 2px solid #FFD700; text-align: center; max-width: 300px; margin: 0 auto; }
        .qr-container img { border-radius: 8px; }
        .qr-container p { color: #FFD700; font-weight: bold; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Reserver un creneau</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #90CAF9;'>Choisissez votre destination et reservez en un clic</p>", unsafe_allow_html=True)
    
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Veuillez vous connecter pour reserver.")
        return
    
    # LISTE COMPLÈTE DES AÉROPORTS 
    airports = {
        "Europe": [
            "Nice Côte d'Azur (NCE) - France",
            "Paris Le Bourget (LBG) - France",
            "Cannes-Mandelieu (CEQ) - France",
            "Monaco Héliport (MCM) - Monaco",
            "Genève (GVA) - Suisse",
            "Milan Linate (LIN) - Italie",
            "Rome Ciampino (CIA) - Italie",
            "London Biggin Hill (BQH) - Royaume-Uni",
            "Farnborough (FAB) - Royaume-Uni",
            "Barcelone (BCN) - Espagne",
            "Palma de Majorque (PMI) - Espagne",
            "Cascais (CAT) - Portugal",
            "Munich (MUC) - Allemagne",
            "Vienne (VIE) - Autriche"
        ],
        "Moyen-Orient & Asie": [
            "Dubaï Al Maktoum (DWC) - EAU",
            "Dubaï International (DXB) - EAU",
            "Doha Hamad (DOH) - Qatar",
            "Riyad (RUH) - Arabie Saoudite",
            "Singapour Changi (SIN) - Singapour",
            "Tokyo Narita (NRT) - Japon"
        ],
        "Amerique": [
            "Teterboro (TEB) - New York, USA",
            "Van Nuys (VNY) - Los Angeles, USA",
            "Miami Opa-Locka (OPF) - Miami, USA",
            "Palm Beach (PBI) - Floride, USA",
            "Toronto Buttonville (YKZ) - Canada",
            "Mexico City (MEX) - Mexique"
        ],
        "Afrique": [
            "Le Cap (CPT) - Afrique du Sud",
            "Marrakech (RAK) - Maroc",
            "Nairobi Wilson (WIL) - Kenya",
            "Tunis Carthage (TUN) - Tunisie",
            "Djerba (DJE) - Tunisie",
        ]
    }
    
    ports = {
        "Europe": [
            "Port de Monaco - Monaco",
            "Port de Cannes - France",
            "Port de Saint-Tropez - France",
            "Port de Marseille - France",
            "Port de Nice - France",
            "Porto Cervo - Sardaigne, Italie",
            "Port de Capri - Italie",
            "Port Hercule - Monaco",
            "Port de Barcelone - Espagne",
            "Port de Palma - Majorque, Espagne",
            "Port de Mykonos - Grèce",
            "Port de Santorin - Grèce",
            "Port de Split - Croatie",
            "Port de Bodrum - Turquie"
        ],
        "Amerique": [
            "Miami Marina - Floride, USA",
            "Newport Harbor - Californie, USA",
            "Marina del Rey - Los Angeles, USA",
            "Nassau Marina - Bahamas",
            "Tortola Marina - Îles Vierges Britanniques",
            "George Town - Grand Cayman"
        ],
        "Asie & Oceanie": [
            "ONE°15 Marina - Singapour",
            "Royal Phuket Marina - Thaïlande",
            "Dubaï Marina - EAU",
            "Sydney Harbour - Australie"
        ]
    }
    
    # Type de transport
    booking_type = st.radio(
        "Type de transport",
        ["Aviation (Jet)", "Maritime (Yacht)"],
        horizontal=True
    )
    
    st.divider()
    
    if booking_type == "Aviation (Jet)":
        region = st.selectbox("Region", list(airports.keys()))
        location = st.selectbox("Aeroport", airports[region])
        
        st.markdown("### Details du creneau")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            display_location_map(location)
        with col2:
            st.markdown(f"""
            <div class="card">
                <p style="color:#FFD700;font-weight:bold;font-size:16px;">{location}</p>
                <p style="color:#B8C6E0;font-size:13px;margin-top:10px;">
                    Aeroport prive<br>
                    Ouvert 24h/24<br>
                    Stationnement disponible
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <p style="color:#B8C6E0;font-size:12px;">CRENEAU</p>
                <p style="color:#FFD700;font-size:16px;font-weight:bold;">Place en jet</p>
                <p style="color:#6C6F78;font-size:11px;">6 places</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <p style="color:#B8C6E0;font-size:12px;">DUREE</p>
                <p style="color:#FFD700;font-size:16px;font-weight:bold;">A la demande</p>
                <p style="color:#6C6F78;font-size:11px;">Vol partage</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <p style="color:#B8C6E0;font-size:12px;">PRIX</p>
                <p style="color:#FFD700;font-size:16px;font-weight:bold;">A partir de 350€</p>
                <p style="color:#6C6F78;font-size:11px;">Par place</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("En quoi consiste ce creneau ?"):
            st.markdown("""
            | Detail | Description |
            |--------|-------------|
            | Type | Jet prive leger |
            | Places | 6 |
            | Depart | Aeroport selectionne |
            | Duree | 1 heure |
            | Confort | Sieges en cuir |
            | Wi-Fi | Haut debit |
            """)
            
    else:
        region = st.selectbox("Region", list(ports.keys()))
        location = st.selectbox("Port", ports[region])
        
        st.markdown("### Details du creneau")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            display_location_map(location)
        with col2:
            st.markdown(f"""
            <div class="card">
                <p style="color:#FFD700;font-weight:bold;font-size:16px;">{location}</p>
                <p style="color:#B8C6E0;font-size:13px;margin-top:10px;">
                    Port prive<br>
                    Ouvert 24h/24<br>
                    Stationnement disponible
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <p style="color:#B8C6E0;font-size:12px;">CRENEAU</p>
                <p style="color:#FFD700;font-size:16px;font-weight:bold;">Place sur yacht</p>
                <p style="color:#6C6F78;font-size:11px;">10 places</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <p style="color:#B8C6E0;font-size:12px;">DUREE</p>
                <p style="color:#FFD700;font-size:16px;font-weight:bold;">Demi-journee</p>
                <p style="color:#6C6F78;font-size:11px;">Sortie en mer</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="card" style="text-align:center;">
                <p style="color:#B8C6E0;font-size:12px;">PRIX</p>
                <p style="color:#FFD700;font-size:16px;font-weight:bold;">A partir de 150€</p>
                <p style="color:#6C6F78;font-size:11px;">Par place</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.expander("En quoi consiste ce creneau ?"):
            st.markdown("""
            | Detail | Description |
            |--------|-------------|
            | Type | Yacht de luxe |
            | Places | 10 |
            | Depart | Port selectionne |
            | Duree | Demi-journee (4h) |
            | Confort | Cabines climatisees |
            | Service | Champagne inclus |
            """)
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", dt.date.today())
    with col2:
        time = st.time_input("Heure", dt.time(10, 0))
    
    duration = st.slider("Duree (minutes)", 30, 180, 60, 15)
    
    st.divider()
   
    
    # ============================================
    # RECAPITULATIF
    # ============================================
    if "Aviation" in booking_type:
        price = 350
        amount = 35000
    else:
        price = 150
        amount = 15000
    
    st.markdown("### Recapitulatif")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Type :** {booking_type}")
    with col2:
        st.markdown(f"**Lieu :** {location}")
    with col3:
        st.markdown(f"**Date :** {date.strftime('%d/%m/%Y')} a {time.strftime('%H:%M')}")
    
    st.caption(f"💰 Prix : {price}€ par place")
    
   
    
    # ============================================
    # RESERVATION + PAIEMENT STRIPE
    # ============================================
    if st.button("Reserver et payer", type="primary", use_container_width=True):
        # 1. Générer un ID de réservation
        booking_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # 2. Créer la réservation en "pending"
        booking_result = create_booking(
            st.session_state.user['localId'],
            booking_type,
            location,
            date.isoformat(),
            time.strftime("%H:%M"),
            duration
        )
        
        if booking_result:
            # 3. Envoyer email "En attente" (SANS QR)
            email_data = {
                "booking_id": booking_id,
                "location": location,
                "date": date.strftime('%d/%m/%Y'),
                "time": time.strftime('%H:%M'),
                "price": price,
                "duration": duration
            }
            user_email = st.session_state.user.get('email')
            if user_email:
                send_pending_email(user_email, email_data)
                st.info("📧 Email de confirmation envoye !")
            
            # 4. PAIEMENT STRIPE
            session = create_checkout_session(
                booking_id=booking_id,
                amount=amount,
                currency="eur",
                success_url="http://localhost:8501/?paiement=success",
                cancel_url="http://localhost:8501/?paiement=cancel"
            )
            
            if session:
                st.markdown("### Paiement securise")
                st.markdown(f"""
                <div style="background:#1A2A4A;border-radius:12px;padding:20px;text-align:center;border:1px solid rgba(255,215,0,0.15);">
                    <p style="color:#B8C6E0;font-size:16px;">Montant : <strong style="color:#FFD700;font-size:20px;">{price}€</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <a href="{session.url}" target="_blank">
                    <button style="background:#FFD700;color:#0A1628;border:none;padding:15px 40px;border-radius:8px;font-weight:bold;font-size:18px;cursor:pointer;width:100%;margin-top:10px;">
                        Payer {price}€
                    </button>
                </a>
                """, unsafe_allow_html=True)
                
                st.caption("🔒 Paiement securise par Stripe")
                
                # 5. APRÈS paiement réussi, confirmer la réservation
                # Cette partie sera gérée par le webhook Stripe ou le retour de paiement
                if confirm_booking_after_payment(booking_id, st.session_state.user['localId']):
                    st.success("✅ Paiement reussi ! Reservation confirmee.")
            else:
                st.error("Erreur lors de la creation du paiement.")