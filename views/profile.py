import streamlit as st
import datetime
from db import get_loyalty_card, initialize_loyalty
from auth import get_user_id
from streamlit.components.v1 import html as st_html


def show():
    # ============================================
    # CSS PREMIUM
    # ============================================
    st.markdown("""
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .profile-container {
            animation: fadeIn 0.6s ease-out;
            max-width: 700px;
            margin: 0 auto;
            padding: 30px;
            background: linear-gradient(135deg, rgba(26, 42, 74, 0.7), rgba(10, 22, 40, 0.9));
            border-radius: 16px;
            border: 1px solid rgba(255, 215, 0, 0.15);
            backdrop-filter: blur(10px);
        }
        
        .profile-avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #FFD700, #F4A460);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: 700;
            color: #0A1628;
            margin: 0 auto 15px auto;
            box-shadow: 0 4px 30px rgba(255, 215, 0, 0.3);
        }
        
        .profile-name {
            text-align: center;
            color: #FFD700;
            font-size: 24px;
            font-weight: 300;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }
        
        .profile-email {
            text-align: center;
            color: #B8C6E0;
            font-size: 14px;
            opacity: 0.7;
            margin-bottom: 25px;
        }
        
        .profile-section {
            background: rgba(10, 22, 40, 0.6);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid rgba(255, 215, 0, 0.08);
            transition: all 0.3s ease;
        }
        
        .profile-section:hover {
            border-color: rgba(255, 215, 0, 0.2);
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.05);
        }
        
        .profile-label {
            color: #6C6F78;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 5px;
        }
        
        .profile-value {
            color: #E8EAF0;
            font-size: 16px;
            font-weight: 400;
        }
        
        .divider-light {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
            margin: 20px 0;
        }

        /* ===== CARTE DE FIDÉLITÉ ===== */
        .loyalty-card {
            border-radius: 16px;
            padding: 25px;
            margin: 15px 0;
            box-shadow: 0 4px 30px rgba(0,0,0,0.3);
            animation: fadeIn 0.8s ease-out;
            background: linear-gradient(135deg, #1A2A4A, #0A1628);
        }
        
        .loyalty-card-bronze { border: 2px solid #CD7F32; }
        .loyalty-card-silver { border: 2px solid #C0C0C0; }
        .loyalty-card-gold { border: 2px solid #FFD700; background: linear-gradient(135deg, #2A1F0A, #0A1628); }
        .loyalty-card-platinum { border: 2px solid #E5E4E2; background: linear-gradient(135deg, #1A1A2E, #0A1628); }
        
        .loyalty-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .loyalty-level {
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .loyalty-level-bronze { color: #CD7F32; }
        .loyalty-level-silver { color: #C0C0C0; }
        .loyalty-level-gold { color: #FFD700; }
        .loyalty-level-platinum { color: #E5E4E2; }
        
        .loyalty-discount {
            font-size: 28px;
            font-weight: bold;
            text-align: right;
        }
        .loyalty-discount-bronze { color: #CD7F32; }
        .loyalty-discount-silver { color: #C0C0C0; }
        .loyalty-discount-gold { color: #FFD700; }
        .loyalty-discount-platinum { color: #E5E4E2; }
        
        .loyalty-stats {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.05);
        }
        
        .loyalty-stat {
            flex: 1;
        }
        .loyalty-stat-label {
            color: #6C6F78;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .loyalty-stat-value {
            color: #E8EAF0;
            font-size: 18px;
            margin: 0;
            font-weight: 600;
        }
        
        .progress-bar-container {
            margin-top: 15px;
        }
        .progress-bar-header {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
        }
        .progress-bar-header span:first-child { color: #B8C6E0; }
        .progress-bar-header span:last-child { color: #6C6F78; }
        
        .progress-bar {
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            height: 8px;
            margin-top: 5px;
            overflow: hidden;
        }
        .progress-bar-fill {
            height: 100%;
            border-radius: 8px;
            transition: width 0.5s ease;
            background: linear-gradient(90deg, #FFD700, #F4A460);
        }
        
        .progress-text {
            color: #6C6F78;
            font-size: 10px;
            margin-top: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # ============================================
    # VÉRIFICATION CONNEXION
    # ============================================
    if "user" not in st.session_state or st.session_state.user is None:
        st.warning("🔒 Veuillez vous connecter pour accéder à votre profil.")
        return
    
    user = st.session_state.user
    email = user.get('email', 'Utilisateur')
    name = email.split('@')[0] if email else 'Utilisateur'
    
    # ============================================
    # RÉCUPÉRER L'ID UTILISATEUR
    # ============================================
    user_id = get_user_id()
    
    # ============================================
    # AFFICHAGE PROFIL
    # ============================================
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    
    # Avatar
    initial = name[0].upper() if name else 'U'
    st.markdown(f"""
    <div class="profile-avatar">{initial}</div>
    <div class="profile-name">{name}</div>
    <div class="profile-email">{email}</div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
    
    # ============================================
    # CARTE DE FIDÉLITÉ
    # ============================================
    if user_id:
        st.markdown("### 💳 Carte de fidélité")
        
        # Vérifier si la carte existe déjà
        card = get_loyalty_card(user_id)
        
        if card:
            show_loyalty_card(card)
        else:
            st.info("📭 Activez votre carte de fidélité pour commencer à cumuler des miles.")
            if st.button("🎯 Activer ma carte de fidélité", use_container_width=True):
                if initialize_loyalty(user_id):
                    st.success("✅ Carte de fidélité activée !")
                    st.rerun()
                else:
                    st.error("❌ Erreur lors de l'activation.")
    
    st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
    
    # ============================================
    # STATISTIQUES
    # ============================================
    st.markdown("### 📊 Statistiques")
    
    # Récupérer les vraies statistiques
    from db import get_bookings
    bookings = get_bookings(user_id) if user_id else []
    total = len(bookings)
    confirmed = sum(1 for b in bookings if b.get('status') == 'confirmed')
    pending = sum(1 for b in bookings if b.get('status') == 'pending')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Réservations", total)
    with col2:
        st.metric("✅ Confirmées", confirmed)
    with col3:
        st.metric("⏳ En attente", pending)
    
    st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
    
    # ============================================
    # INFORMATIONS PERSONNELLES
    # ============================================
    st.markdown("### 📋 Informations personnelles")
    
    st.markdown(f"""
    <div class="profile-section">
        <div class="profile-label">Nom d'utilisateur</div>
        <div class="profile-value">{name}</div>
    </div>
    <div class="profile-section">
        <div class="profile-label">Adresse email</div>
        <div class="profile-value">{email}</div>
    </div>
    <div class="profile-section">
        <div class="profile-label">Membre depuis</div>
        <div class="profile-value">{datetime.datetime.now().strftime("%d %B %Y")}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider-light">', unsafe_allow_html=True)
    
    # ============================================
    # ACTIONS
    # ============================================
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📧 Modifier l'email", use_container_width=True):
            st.info("Fonctionnalité à venir")
    with col2:
        if st.button("🔑 Changer le mot de passe", use_container_width=True):
            st.info("Fonctionnalité à venir")
    
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================
# FONCTION : AFFICHER LA CARTE DE FIDÉLITÉ
# ============================================
from streamlit.components.v1 import html as st_html

def show_loyalty_card(card):
    """Affiche la carte de fidélité avec st.components.v1.html"""
    
    level = card.get("level", "Bronze")
    name = card.get("name", "Client")
    member_since = card.get("member_since", "Non défini")
    total_bookings = card.get("total_bookings", 0)
    miles = card.get("miles", 0)
    discount = card.get("discount", 0)
    next_level = card.get("next_level")
    
    # Couleurs selon le niveau
    colors = {
        "Bronze": {"border": "#CD7F32", "text": "#CD7F32", "bg": "#2A1A0A"},
        "Silver": {"border": "#C0C0C0", "text": "#C0C0C0", "bg": "#1A1A1A"},
        "Gold": {"border": "#FFD700", "text": "#FFD700", "bg": "#2A1F0A"},
        "Platinum": {"border": "#E5E4E2", "text": "#E5E4E2", "bg": "#1A1A2E"},
    }
    
    color = colors.get(level, colors["Bronze"])
    
    # HTML de la carte
    html_content = f"""
    <style>
        @keyframes fadeInCard {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .loyalty-card {{
            animation: fadeInCard 0.6s ease-out;
            background: linear-gradient(135deg, {color['bg']}, #0A1628);
            border: 2px solid {color['border']};
            border-radius: 16px;
            padding: 25px;
            margin: 10px 0;
            box-shadow: 0 4px 30px rgba(0,0,0,0.3);
            max-width: 600px;
        }}
        .loyalty-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .loyalty-level {{
            color: {color['text']};
            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }}
        .loyalty-label {{
            color: #6C6F78;
            font-size: 11px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        .loyalty-name {{
            color: #B8C6E0;
            font-size: 14px;
            margin: 5px 0 0 0;
        }}
        .loyalty-since {{
            color: #6C6F78;
            font-size: 11px;
        }}
        .loyalty-discount {{
            color: {color['text']};
            font-size: 28px;
            font-weight: bold;
            text-align: right;
        }}
        .loyalty-discount-label {{
            color: #6C6F78;
            font-size: 10px;
            text-align: right;
            margin: 0;
        }}
        .loyalty-stats {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.05);
        }}
        .loyalty-stat {{
            flex: 1;
        }}
        .loyalty-stat-label {{
            color: #6C6F78;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .loyalty-stat-value {{
            color: #E8EAF0;
            font-size: 18px;
            margin: 0;
            font-weight: 600;
        }}
        .progress-container {{
            margin-top: 15px;
        }}
        .progress-header {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #B8C6E0;
        }}
        .progress-header span:last-child {{
            color: #6C6F78;
        }}
        .progress-bar {{
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
            height: 8px;
            margin-top: 5px;
            overflow: hidden;
        }}
        .progress-fill {{
            height: 100%;
            border-radius: 8px;
            transition: width 0.5s ease;
            background: linear-gradient(90deg, #FFD700, #F4A460);
            width: 0%;
        }}
        .progress-text {{
            color: #6C6F78;
            font-size: 10px;
            margin-top: 5px;
        }}
    </style>
    <div class="loyalty-card">
        <div class="loyalty-header">
            <div>
                <div class="loyalty-label">CARTE DE FIDÉLITÉ</div>
                <div class="loyalty-level">{level}</div>
                <div class="loyalty-name">{name}</div>
                <div class="loyalty-since">Membre depuis {member_since}</div>
            </div>
            <div>
                <div class="loyalty-discount">{discount}%</div>
                <div class="loyalty-discount-label">RÉDUCTION</div>
            </div>
        </div>
        <div class="loyalty-stats">
            <div class="loyalty-stat">
                <div class="loyalty-stat-label">RÉSERVATIONS</div>
                <div class="loyalty-stat-value">{total_bookings}</div>
            </div>
            <div class="loyalty-stat">
                <div class="loyalty-stat-label">MILES</div>
                <div class="loyalty-stat-value">{miles}</div>
            </div>
            <div class="loyalty-stat">
                <div class="loyalty-stat-label">RÉDUCTION</div>
                <div class="loyalty-stat-value">{discount}%</div>
            </div>
        </div>
        {get_progress_html(next_level, total_bookings)}
    </div>
    """
    
    st_html(html_content, height=250)

def get_progress_html(next_level, total_bookings):
    """Retourne le HTML de la barre de progression"""
    if not next_level:
        return f"""
        <div style="margin-top:15px; padding:10px; background:rgba(255,215,0,0.05); border-radius:8px; text-align:center;">
            <span style="color:#FFD700; font-size:13px;">🏆 Niveau maximum atteint !</span>
            <p style="color:#6C6F78; font-size:11px;">Vous êtes au plus haut niveau de fidélité.</p>
        </div>
        """
    
    needed = next_level.get("bookings_needed", 1)
    remaining = next_level.get("bookings_remaining", 0)
    level_name = next_level.get("level", "Prochain niveau")
    discount_next = next_level.get("discount", 0)
    
    progress = min((total_bookings / needed) * 100, 100)
    
    return f"""
    <div class="progress-container">
        <div class="progress-header">
            <span>Prochain niveau : {level_name}</span>
            <span>{total_bookings}/{needed}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width:{progress}%;"></div>
        </div>
        <div class="progress-text">Encore {remaining} réservation(s) pour atteindre {level_name} (+{discount_next}% de réduction)</div>
    </div>
    """


def show_progress_bar(next_level, total_bookings):
    """Affiche la barre de progression vers le prochain niveau"""
    
    if not next_level:
        return f"""
        <div style="margin-top:15px; padding:10px; background:rgba(255,215,0,0.05); border-radius:8px; text-align:center;">
            <span style="color:#FFD700; font-size:13px;">🏆 Niveau maximum atteint !</span>
            <p style="color:#6C6F78; font-size:11px;">Vous êtes au plus haut niveau de fidélité.</p>
        </div>
        """
    
    needed = next_level.get("bookings_needed", 1)
    remaining = next_level.get("bookings_remaining", 0)
    level_name = next_level.get("level", "Prochain niveau")
    discount_next = next_level.get("discount", 0)
    
    progress = min((total_bookings / needed) * 100, 100)
    
    return f"""
    <div class="progress-bar-container">
        <div class="progress-bar-header">
            <span>Prochain niveau : {level_name}</span>
            <span>{total_bookings}/{needed}</span>
        </div>
        <div class="progress-bar">
            <div class="progress-bar-fill" style="width:{progress}%;"></div>
        </div>
        <div class="progress-text">Encore {remaining} réservation(s) pour atteindre {level_name} (+{discount_next}% de réduction)</div>
    </div>
    """