import streamlit as st
import datetime as dt
import re
import random
import string
from utils.map_utils import display_location_map
from utils.qr_generator import generate_qr_code, get_qr_html, create_booking_qr_data
from stripe_config import create_checkout_session
from notifications import send_parking_confirmation_email_with_qr, send_airport_notification_email, send_parking_pending_email
from db import db

# ============================================
# DICTIONNAIRE DES PRIX RÉELS
# ============================================
PRICES = {
    "jet": {
        "poids": [
            {"label": "Moins de 5 700 kg", "min": 150, "max": 400, "default": 250},
            {"label": "5 700 - 15 000 kg", "min": 250, "max": 700, "default": 450},
            {"label": "15 000 - 30 000 kg", "min": 400, "max": 1200, "default": 700},
            {"label": "Plus de 30 000 kg", "min": 600, "max": 2000, "default": 1200},
        ]
    },
    "yacht": {
        "longueur": [
            {"label": "Moins de 20m", "min": 150, "max": 400, "default": 250},
            {"label": "20-30m", "min": 250, "max": 700, "default": 450},
            {"label": "30-40m", "min": 400, "max": 1200, "default": 700},
            {"label": "40-50m", "min": 600, "max": 1800, "default": 1000},
            {"label": "50-60m", "min": 800, "max": 2500, "default": 1500},
            {"label": "Plus de 60m", "min": 1200, "max": 4000, "default": 2200},
        ]
    }
}

def get_price_range(parking_type, weight_or_length):
    """Retourne la fourchette de prix selon le type et la taille"""
    if parking_type == "Jet prive":
        for p in PRICES["jet"]["poids"]:
            if p["label"] == weight_or_length:
                return p
    else:
        for p in PRICES["yacht"]["longueur"]:
            if p["label"] == weight_or_length:
                return p
    return {"min": 150, "max": 400, "default": 250}

# ============================================
# FONCTIONS POUR LA NOTIFICATION À L'AÉROPORT
# ============================================
def get_airport_email(location):
    """Récupère l'email de l'aéroport/port concerné"""
    # À remplacer par une vraie base de données plus tard
    airport_emails = {
        "Nice Côte d'Azur (NCE) - France": "parking@nice.aeroport.fr",
        "Paris Le Bourget (LBG) - France": "parking@paris-lebourget.fr",
        "Monaco Héliport (MCM) - Monaco": "parking@monaco-heliport.mc",
        "Tunis Carthage (TUN) - Tunisie": "aneyondpro@gmail.com",
        "Djerba (DJE) - Tunisie": "parking@djerba-airport.tn",
        "Port de Monaco": "parking@monaco-port.mc",
        "Port de Cannes": "parking@cannes-port.fr",
        "Port de Saint-Tropez": "parking@sainttropez-port.fr",
        "Port de Tunis": "parking@tunis-port.tn",
        "Port de Sousse": "parking@sousse-port.tn",
    }
    return airport_emails.get(location)

def notify_airport(booking_data, location):
    """Envoie une notification à l'aéroport/port concerné"""
    airport_email = get_airport_email(location)
    
    if airport_email:
        try:
            send_airport_notification_email(airport_email, booking_data)
            return True
        except Exception as e:
            st.warning(f"⚠️ Erreur d'envoi à l'aéroport : {e}")
            return False
    else:
        st.warning(f"⚠️ Aucun email trouvé pour {location}")
        return False

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
        .price-hint {
            background: rgba(255, 215, 0, 0.05);
            border-radius: 8px;
            padding: 10px 15px;
            border-left: 3px solid #FFD700;
            margin-top: 5px;
        }
        .price-hint p {
            color: #B8C6E0;
            font-size: 12px;
            margin: 0;
        }
        .price-hint strong {
            color: #FFD700;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Reserver un stationnement</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #90CAF9;'>Pour les propriétaires de jets prives et yachts</p>", unsafe_allow_html=True)
    
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("Veuillez vous connecter pour reserver un stationnement.")
        return
    
    # ============================================
    # FORMULAIRE
    # ============================================
    st.divider()
    st.markdown("### Type de stationnement")
    parking_type = st.radio("Selectionnez le type", ["Jet prive", "Yacht"], horizontal=True, index=0)
    st.divider()
    
    st.markdown("### Informations du vehicule")
    st.caption("Tous les champs sont obligatoires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if parking_type == "Jet prive":
            jet_brands = ["Selectionnez une marque...", "Bombardier", "Cessna", "Dassault", "Embraer", "Gulfstream", "Pilatus", "Textron Aviation"]
            brand = st.selectbox("Marque du jet *", jet_brands, index=0)
            
            if brand == "Bombardier":
                models = ["Challenger 300", "Challenger 350", "Challenger 600", "Global 5000", "Global 6000", "Global 7500"]
            elif brand == "Cessna":
                models = ["Citation CJ3", "Citation CJ4", "Citation XLS", "Citation Latitude", "Citation Longitude"]
            elif brand == "Dassault":
                models = ["Falcon 2000", "Falcon 7X", "Falcon 8X", "Falcon 900"]
            elif brand == "Embraer":
                models = ["Phenom 300", "Praetor 500", "Praetor 600", "Legacy 500", "Lineage 1000"]
            elif brand == "Gulfstream":
                models = ["G280", "G450", "G500", "G550", "G600", "G650", "G700"]
            elif brand == "Pilatus":
                models = ["PC-12", "PC-24"]
            elif brand == "Textron Aviation":
                models = ["King Air 350", "Cessna Caravan", "Cessna 206"]
            else:
                models = ["Selectionnez d'abord une marque"]
            
            model = st.selectbox("Modele *", models, index=0 if len(models) > 0 else None)
            
            tail_number = st.text_input("Numero d'immatriculation *", placeholder="Ex: N12345, F-GABC")
            if tail_number:
                tail_pattern = r'^[A-Z0-9\-]{5,10}$'
                if not re.match(tail_pattern, tail_number.upper()):
                    st.warning("Format invalide")
            
            weight = st.selectbox("Poids maximum (MTOW)", ["Moins de 5 700 kg", "5 700 - 15 000 kg", "15 000 - 30 000 kg", "Plus de 30 000 kg"])
            
        else:
            yacht_brands = ["Selectionnez une marque...", "Azimut", "Benetti", "Ferretti", "Heesen", "Lürssen", "Oceanco", "Princess", "Sanlorenzo", "Sunseeker", "Wally"]
            brand = st.selectbox("Marque du yacht *", yacht_brands, index=0)
            
            if brand == "Azimut":
                models = ["Azimut 60", "Azimut 66", "Azimut 72", "Azimut 78", "Azimut 88"]
            elif brand == "Benetti":
                models = ["Benetti 50", "Benetti 55", "Benetti 65", "Benetti 80", "Benetti 100"]
            elif brand == "Ferretti":
                models = ["Ferretti 670", "Ferretti 720", "Ferretti 750", "Ferretti 850"]
            elif brand == "Heesen":
                models = ["Heesen 40", "Heesen 45", "Heesen 55", "Heesen 65"]
            elif brand == "Lürssen":
                models = ["Lürssen 60", "Lürssen 70", "Lürssen 80", "Lürssen 100"]
            elif brand == "Oceanco":
                models = ["Oceanco 65", "Oceanco 75", "Oceanco 85", "Oceanco 100"]
            elif brand == "Princess":
                models = ["Princess 70", "Princess 75", "Princess 88", "Princess 95"]
            elif brand == "Sanlorenzo":
                models = ["Sanlorenzo 64", "Sanlorenzo 72", "Sanlorenzo 82", "Sanlorenzo 100"]
            elif brand == "Sunseeker":
                models = ["Sunseeker 65", "Sunseeker 74", "Sunseeker 86", "Sunseeker 95"]
            elif brand == "Wally":
                models = ["Wally 60", "Wally 70", "Wally 80"]
            else:
                models = ["Selectionnez d'abord une marque"]
            
            model = st.selectbox("Modele *", models, index=0 if len(models) > 0 else None)
            yacht_name = st.text_input("Nom du yacht *", placeholder="Ex: MY Lady, Sea Dream")
            length = st.selectbox("Longueur hors tout", ["Moins de 20m", "20-30m", "30-40m", "40-50m", "50-60m", "Plus de 60m"])
            tonnage = st.selectbox("Tonnage", ["Moins de 100 t", "100-300 t", "300-500 t", "500-1000 t", "Plus de 1000 t"])
    
    with col2:
        if parking_type == "Jet prive":
            st.markdown("### Caracteristiques du jet")
            year = st.number_input("Annee de fabrication", min_value=1970, max_value=dt.date.today().year, value=2015)
            range_km = st.selectbox("Autonomie (km)", ["Moins de 2 500", "2 500 - 4 000", "4 000 - 6 000", "6 000 - 9 000", "Plus de 9 000"])
            passengers = st.number_input("Nombre de passagers", min_value=2, max_value=30, value=8)
        else:
            st.markdown("### Caracteristiques du yacht")
            year = st.number_input("Annee de fabrication", min_value=1970, max_value=dt.date.today().year, value=2010)
            cabins = st.number_input("Nombre de cabines", min_value=1, max_value=30, value=4)
            passengers = st.number_input("Passagers max", min_value=2, max_value=50, value=10)
    
    st.divider()
    
    # ============================================
    # LOCALISATION
    # ============================================
    st.markdown("### Localisation du stationnement")
    
    if parking_type == "Jet prive":
        locations = {"Europe": ["Nice Côte d'Azur (NCE) - France", "Paris Le Bourget (LBG) - France", "Monaco Héliport (MCM) - Monaco"], "Afrique": ["Tunis Carthage (TUN) - Tunisie", "Djerba (DJE) - Tunisie"]}
    else:
        locations = {"Europe": ["Port de Monaco", "Port de Cannes", "Port de Saint-Tropez"], "Afrique": ["Port de Tunis", "Port de Sousse"]}
    
    region = st.selectbox("Region", list(locations.keys()))
    location = st.selectbox("Lieu", locations[region])
    
    st.divider()
    
    # ============================================
    # CRENEAU
    # ============================================
    st.markdown("### Creneau de stationnement")
    
    col1, col2 = st.columns(2)
    with col1:
        arrival_date = st.date_input("Date d'arrivee", dt.date.today())
        arrival_time = st.time_input("Heure d'arrivee", dt.time(10, 0))
    with col2:
        departure_date = st.date_input("Date de depart", dt.date.today() + dt.timedelta(days=1))
        departure_time = st.time_input("Heure de depart", dt.time(14, 0))
    
    duration_days = (departure_date - arrival_date).days
    if duration_days < 0:
        st.error("La date de depart doit etre apres la date d'arrivee")
        return
    
    st.caption(f"Duree : {duration_days} jour(s)")
    st.divider()
    
    # ============================================
    # TARIFS (avec prix dynamique et prix logiques)
    # ============================================
    st.markdown("### Tarifs")
    
    # Récupérer la fourchette de prix selon le type et la taille
    if parking_type == "Jet prive":
        price_range = get_price_range(parking_type, weight)
    else:
        price_range = get_price_range(parking_type, length)
    
    # --- PRIX PAR JOUR AVEC VALEURS RÉALISTES ---
    col1, col2 = st.columns(2)
    
    with col1:
        price_per_day = st.number_input(
            "💰 Prix par jour (€)",
            min_value=price_range["min"],
            max_value=price_range["max"],
            value=price_range["default"],
            step=50,
            help=f"Fourchette recommandée : {price_range['min']}€ - {price_range['max']}€"
        )
    
    with col2:
        st.markdown(f"""
        <div class="price-hint">
            <p>📊 <strong>Prix recommandé</strong> : {price_range['default']}€</p>
            <p style="font-size:11px;color:#6C6F78;margin-top:2px;">
                Fourchette : {price_range['min']}€ - {price_range['max']}€
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # --- PRIX DYNAMIQUE ---
    dynamic_pricing = st.checkbox(
        "📊 Activer le prix dynamique",
        help="Le prix s'ajuste automatiquement en fonction de la demande"
    )
    
    if dynamic_pricing:
        col1, col2 = st.columns(2)
        with col1:
            base_price = st.number_input(
                "💰 Prix de base (€)",
                min_value=price_range["min"],
                max_value=price_range["max"],
                value=price_per_day,
                step=50,
                help="Prix minimum en basse saison"
            )
        with col2:
            max_price = st.number_input(
                "📈 Prix maximum (€)",
                min_value=base_price,
                max_value=price_range["max"] * 2,
                value=min(base_price * 2, price_range["max"] * 2),
                step=50,
                help="Prix maximum en haute saison"
            )
        
        st.info("📊 Le prix s'ajustera automatiquement entre {}€ et {}€ selon la demande".format(base_price, max_price))
        price_per_day = base_price
    else:
        st.success(f"💰 Prix fixe : {price_per_day}€ par jour")
    
    # --- CALCUL DU TOTAL ---
    total_price = price_per_day * max(duration_days, 1)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='card'>
            <p style='color:#B8C6E0;'>💰 Prix par jour</p>
            <p style='color:#FFD700;font-size:24px;font-weight:bold;'>{price_per_day}€</p>
            <p style='color:#6C6F78;font-size:11px;'>
                {'Prix dynamique (variable)' if dynamic_pricing else 'Prix fixe'}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='card'>
            <p style='color:#B8C6E0;'>💳 Total</p>
            <p style='color:#FFD700;font-size:24px;font-weight:bold;'>{total_price}€</p>
            <p style='color:#6C6F78;font-size:11px;'>{max(duration_days, 1)} jour(s)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ============================================
    # PARTIE PRESTATAIRE
    # ============================================
    st.markdown("### Informations du prestataire")
    
    prestataire_type = st.radio(
        "Type de prestataire",
        ["Particulier", "Entreprise / Société"],
        horizontal=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if prestataire_type == "Particulier":
            prestataire_nom = st.text_input("Nom du proprietaire *", placeholder="Jean Dupont")
            prestataire_telephone = st.text_input("Telephone *", placeholder="+33 6 12 34 56 78")
            prestataire_email = st.text_input("Email *", placeholder="jean@email.com")
        else:
            prestataire_nom = st.text_input("Nom de l'entreprise *", placeholder="Jet Luxury SAS")
            prestataire_siret = st.text_input("Numero SIRET *", placeholder="123 456 789 00012")
            prestataire_telephone = st.text_input("Telephone *", placeholder="+33 1 23 45 67 89")
            prestataire_email = st.text_input("Email *", placeholder="contact@entreprise.com")
    
    with col2:
        st.markdown("""
        <div style="
            background: rgba(26, 42, 74, 0.5);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 215, 0, 0.1);
            height: 100%;
        ">
            <p style="color: #6C6F78; font-size: 12px;">Information importante</p>
            <p style="color: #B8C6E0; font-size: 13px; margin-top: 10px;">
                Ces informations permettront aux clients de vous contacter.<br>
                Elles seront affichees sur la page de reservation.
            </p>
            <p style="color: #6C6F78; font-size: 12px; margin-top: 15px;">
                Vos donnees sont securisees
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("Conditions particulieres (optionnel)"):
        conditions_prestataire = st.text_area(
            "Informations complementaires",
            placeholder="Ex: Acces 24h/24, personnel dedie, service VIP..."
        )
    
    st.divider()
    
    # ============================================
    # CONFIRMATION
    # ============================================
    st.markdown("### Confirmation legale")
    st.warning("La reservation de stationnement engage votre responsabilite.")
    
    confirmed = st.checkbox("Je certifie etre le proprietaire/exploitant autorise de ce vehicule.")
    if not confirmed:
        st.error("Vous devez confirmer pour reserver.")
        st.stop()
    
    # ============================================
    # RECAPITULATIF
    # ============================================
    st.markdown("### Recapitulatif")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Type :** {parking_type}")
        st.markdown(f"**Lieu :** {location}")
        st.markdown(f"**Arrivee :** {arrival_date.strftime('%d/%m/%Y')} a {arrival_time.strftime('%H:%M')}")
    with col2:
        st.markdown(f"**Depart :** {departure_date.strftime('%d/%m/%Y')} a {departure_time.strftime('%H:%M')}")
        st.markdown(f"**Duree :** {max(duration_days, 1)} jour(s)")
        st.markdown(f"**Total :** {total_price}€")
    
    if parking_type == "Jet prive":
        st.markdown(f"**Jet :** {brand} {model} ({tail_number})")
        vehicle_name = f"{brand} {model} - {tail_number}"
    else:
        st.markdown(f"**Yacht :** {brand} {model} ({yacht_name})")
        vehicle_name = f"{brand} {model} - {yacht_name}"
    
    st.markdown("### Informations du prestataire")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Type :** {prestataire_type}")
        st.markdown(f"**Nom :** {prestataire_nom}")
        st.markdown(f"**Telephone :** {prestataire_telephone}")
    with col2:
        st.markdown(f"**Email :** {prestataire_email}")
        if prestataire_type == "Entreprise / Société":
            st.markdown(f"**SIRET :** {prestataire_siret}")
        if conditions_prestataire:
            st.markdown(f"**Conditions :** {conditions_prestataire[:50]}...")
    
    st.divider()
    
    # ============================================
    # PAIEMENT STRIPE + NOTIFICATION AÉROPORT
    # ============================================
    if st.button("Payer et reserver", type="primary", use_container_width=True):
        booking_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # 1. PAIEMENT STRIPE
        amount = total_price * 100
        session = create_checkout_session(
            booking_id=booking_id,
            amount=amount,
            currency="eur",
            success_url="http://localhost:8501/?paiement=success",
            cancel_url="http://localhost:8501/?paiement=cancel"
        )
        
        if session:
            # 2. CRÉER LA RÉSERVATION EN BASE DE DONNÉES (statut: pending)
            if db is not None:
                try:
                    booking_ref = db.collection("bookings").document(booking_id)
                    booking_ref.set({
                        "userId": st.session_state.user['localId'],
                        "type": f"Stationnement - {parking_type}",
                        "location": location,
                        "arrival_date": arrival_date.isoformat(),
                        "arrival_time": arrival_time.strftime("%H:%M"),
                        "departure_date": departure_date.isoformat(),
                        "departure_time": departure_time.strftime("%H:%M"),
                        "duration_days": max(duration_days, 1),
                        "total_price": total_price,
                        "vehicle_name": vehicle_name,
                        "status": "pending",
                        "prestataire_nom": prestataire_nom,
                        "prestataire_email": prestataire_email,
                        "prestataire_telephone": prestataire_telephone,
                        "dynamic_pricing": dynamic_pricing,
                        "created_at": firestore.SERVER_TIMESTAMP
                    })
                except Exception as e:
                    st.warning(f"⚠️ Erreur sauvegarde : {e}")
            
            # 3. ENVOYER LA NOTIFICATION À L'AÉROPORT
            airport_notified = notify_airport({
                "booking_id": booking_id,
                "location": location,
                "arrival_date": arrival_date.strftime('%d/%m/%Y'),
                "arrival_time": arrival_time.strftime('%H:%M'),
                "departure_date": departure_date.strftime('%d/%m/%Y'),
                "departure_time": departure_time.strftime('%H:%M'),
                "duration_days": max(duration_days, 1),
                "total_price": total_price,
                "vehicle_name": vehicle_name,
                "prestataire_nom": prestataire_nom,
                "prestataire_telephone": prestataire_telephone,
                "prestataire_email": prestataire_email,
            }, location)
            
            if airport_notified:
                st.success("📧 Demande de stationnement envoyée à l'aéroport/port !")
            else:
                st.info("📧 Une confirmation vous sera envoyée après validation.")
            
            # 4. ENVOYER UN EMAIL AU PRESTATAIRE (en attente)
            from notifications import send_parking_pending_email
            
            email_data = {
                "booking_id": booking_id,
                "parking_type": parking_type,
                "location": location,
                "arrival_date": arrival_date.strftime('%d/%m/%Y'),
                "arrival_time": arrival_time.strftime('%H:%M'),
                "departure_date": departure_date.strftime('%d/%m/%Y'),
                "departure_time": departure_time.strftime('%H:%M'),
                "duration_days": str(max(duration_days, 1)),
                "total_price": str(total_price),
                "vehicle_name": vehicle_name,
                "price_type": "Dynamique" if dynamic_pricing else "Fixe",
                "prestataire_nom": prestataire_nom,
                "prestataire_type": prestataire_type,
                "prestataire_telephone": prestataire_telephone,
                "prestataire_email": prestataire_email,
                "status": "pending"
            }
            
            user_email = st.session_state.user.get('email')
            if user_email:
                send_parking_pending_email(user_email, email_data)
                st.success("📧 Un email de confirmation vous a été envoyé.")
            
            # 5. AFFICHER LE QR CODE (UNIQUEMENT APRÈS VALIDATION)
            # Pour l'instant, on l'affiche en mode "en attente"
            st.markdown("""
            <div style="background:#1A2A4A;border-radius:12px;padding:20px;border:1px solid #F4A460;text-align:center;">
                <h3 style="color:#F4A460;">⏳ En attente de validation</h3>
                <p style="color:#B8C6E0;font-size:14px;">
                    Votre demande de stationnement a été envoyée.<br>
                    Vous recevrez un QR Code une fois la réservation confirmée par l'aéroport.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Erreur lors de la creation du paiement.")