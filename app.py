import streamlit as st
import sys
import os
from db import db, init_firestore
import base64
from views.home import get_logo_base64

# ============================================
# CONNEXION AUTOMATIQUE
# ============================================
from auth import auto_login

if "user" not in st.session_state:
    st.session_state.user = None

if "firebase_token" not in st.session_state:
    st.session_state.firebase_token = None

if st.session_state.user is None:
    auto_login()

# ============================================
# CACHE POUR FIRESTORE (une seule initialisation)
# ============================================
@st.cache_resource
def get_firestore():
    """Initialise Firestore une seule fois et la met en cache."""
    success = init_firestore()
    return success

# Appeler une fois pour initialiser
firestore_ok = get_firestore()

# ============================================
# CACHE POUR LES DONNÉES
# ============================================
@st.cache_data(ttl=300)
def get_cached_bookings(user_id):
    from db import get_bookings
    return get_bookings(user_id)

@st.cache_data(ttl=600)
def get_cached_slots():
    from db import get_available_slots
    return get_available_slots()

# ============================================
# INITIALISATION
# ============================================
if "mode" not in st.session_state:
    st.session_state.mode = None

sys.path.append(os.path.dirname(__file__))
views_path = os.path.join(os.path.dirname(__file__), "views")
if views_path not in sys.path:
    sys.path.insert(0, views_path)

query_params = st.query_params
page = query_params.get("page", "")
no_sidebar_pages = ["experience", "how_it_works", "pricing"]

# ============================================
# CONFIGURATION DE LA PAGE
# ============================================
st.set_page_config(
    page_title="MyJetSlot - Yacht & Marine",
    page_icon="🚤",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None  
)

# ============================================
# CSS GLOBAL (inchangé)
# ============================================
st.markdown("""
<style>
    section[data-testid="stSidebar"] .stMarkdown:has(a[href*="pages"]) {
        display: none !important;
    }
    .st-emotion-cache-1y4p8pa {
        display: none !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 22, 40, 0.95) 0%, rgba(26, 42, 74, 0.92) 100%) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 215, 0, 0.15) !important;
        box-shadow: 4px 0 40px rgba(0, 0, 0, 0.5) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: transparent !important;
    }
    
    .stRadio label {
        color: #B8C6E0 !important;
        font-size: 14px !important;
        padding: 10px 16px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        font-weight: 400 !important;
        letter-spacing: 0.5px !important;
        margin: 2px 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        cursor: pointer !important;
    }
    .stRadio label input[type="radio"] {
        display: none !important;
    }
    .stRadio label div[data-baseweb="radio"] {
        display: none !important;
    }
    .stRadio > div:first-child {
        display: none !important;
    }
    .stRadio > div > p {
        display: none !important;
    }
    .stRadio label .st-emotion-cache-1g3h8it {
        display: none !important;
    }
    .stRadio label:hover {
        background: rgba(255, 215, 0, 0.08) !important;
        transform: translateX(5px) !important;
        color: #FFD700 !important;
    }
    .stRadio .stRadioSelected {
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.15), rgba(255, 215, 0, 0.05)) !important;
        border-left: 3px solid #FFD700 !important;
        color: #FFD700 !important;
        font-weight: 600 !important;
        border-radius: 0 10px 10px 0 !important;
    }
    
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.3), transparent) !important;
        margin: 15px 0 !important;
    }
    .stAlert {
        background: rgba(255, 215, 0, 0.05) !important;
        border: 1px solid rgba(255, 215, 0, 0.15) !important;
        border-radius: 10px !important;
    }
    
    .stButton button {
        background: transparent !important;
        border: none !important;
        color: #FFD700 !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        letter-spacing: 1px !important;
        padding: 8px 16px !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
        width: auto !important;
        text-transform: none !important;
    }
    .stButton button:hover {
        background: rgba(255, 215, 0, 0.04) !important;
        border-radius: 4px !important;
        color: #FFD700 !important;
        transform: scale(1.02);
    }
    .stButton button:active,
    .stButton button:focus {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .stSidebar .stButton button {
        color: #FFD700 !important;
        font-size: 13px !important;
        padding: 6px 12px !important;
    }
    .stSidebar .stButton button:hover {
        background: rgba(255, 215, 0, 0.06) !important;
        border-radius: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# IMPORT DES PAGES (import conditionnel plus tard pour vitesse)
# ============================================
def load_page(module_name):
    """Charge une page dynamiquement pour éviter les imports inutiles."""
    try:
        if module_name == "home":
            from views import home
            return home
        elif module_name == "book":
            from views import book
            return book
        elif module_name == "book_pilot":
            from views import book_pilot
            return book_pilot
        elif module_name == "history":
            from views import history
            return history
        elif module_name == "profile":
            from views import profile
            return profile
        elif module_name == "signup":
            from views import signup
            return signup
        elif module_name == "settings":
            from views import settings
            return settings
        elif module_name == "experience":
            from views import experience
            return experience
        elif module_name == "how_it_works":
            from views import how_it_works
            return how_it_works
        elif module_name == "pricing":
            from views import pricing
            return pricing
        else:
            return None
    except ImportError:
        return None

# ============================================
# LOGO (inchangé)
# ============================================
def show_logo():
    svg_code = '''
    <svg width="180" height="60" viewBox="0 0 180 60" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="goldNav" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FFD700"/>
                <stop offset="50%" stop-color="#F4A460"/>
                <stop offset="100%" stop-color="#DAA520"/>
            </linearGradient>
        </defs>
        <path d="M5 35 L15 28 L30 25 L50 25 L65 28 L75 35 L65 42 L50 45 L30 45 L15 42 L5 35Z" fill="url(#goldNav)"/>
        <path d="M0 48 L20 44 L40 48 L60 44 L80 48" stroke="url(#goldNav)" stroke-width="2" fill="none" opacity="0.5"/>
        <text x="0" y="22" font-family="'Georgia', serif" font-weight="700" font-size="22" fill="url(#goldNav)" letter-spacing="2">MYJETSLOT</text>
        <text x="0" y="10" font-family="'Arial', sans-serif" font-weight="400" font-size="7" fill="#B8C6E0" letter-spacing="2">YACHT &amp; MARINE</text>
    </svg>
    '''
    b64 = base64.b64encode(svg_code.encode()).decode()
    img_tag = f'<img src="data:image/svg+xml;base64,{b64}" style="width:100%; max-width:180px; display:block; margin:0 auto;">'
    st.markdown(img_tag, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
show_sidebar = st.session_state.mode is not None and page not in no_sidebar_pages

if show_sidebar:
    with st.sidebar:
        st.markdown(get_logo_base64(), unsafe_allow_html=True)
        if st.session_state.mode == "client":
            menu = st.radio(
                "",
                ["Accueil", "Reserver", "Historique", "Profil", "Creer un compte", "Paramètres"],
                label_visibility="collapsed"
            )
        else:
            menu = st.radio(
                "",
                ["Accueil", "Stationnement", "Reservations recues", "Creer un compte", "Paramètres"],
                label_visibility="collapsed"
            )
        
        st.markdown('<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,215,0,0.15), transparent); margin: 20px 0 15px 0;">', unsafe_allow_html=True)
        if st.button(" Changer d'espace", use_container_width=True):
            st.session_state.mode = None
            st.rerun()
        st.markdown('<hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,215,0,0.15), transparent); margin: 20px 0 15px 0;">', unsafe_allow_html=True)
        
        if st.session_state.user:
            user_email = st.session_state.user.get('email', 'Connecté')
            st.markdown(f"""
            <div style="background: rgba(255, 215, 0, 0.05); border: 1px solid rgba(255, 215, 0, 0.15); border-radius: 10px; padding: 12px 15px; text-align: center;">
                <span style="color: #FFD700; font-size: 14px;">✅ Connecté</span>
                <p style="color: #B8C6E0; font-size: 12px; margin: 4px 0 0 0; opacity: 0.7;">{user_email}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Se deconnecter", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        else:
            st.markdown("""
            <div style="background: rgba(255, 215, 0, 0.03); border: 1px solid rgba(255, 215, 0, 0.08); border-radius: 10px; padding: 12px 15px; text-align: center;">
                <span style="color: #6C6F78; font-size: 13px;">Non connecte</span>
                <p style="color: #4A4F58; font-size: 11px; margin: 4px 0 0 0;">Connectez-vous pour reserver</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# ROUTAGE (avec imports conditionnels pour vitesse)
# ============================================
if page == "experience":
    page_module = load_page("experience")
    if page_module:
        page_module.show()
elif page == "how_it_works":
    page_module = load_page("how_it_works")
    if page_module:
        page_module.show()
elif page == "pricing":
    page_module = load_page("pricing")
    if page_module:
        page_module.show()
elif st.session_state.mode is None:
    page_module = load_page("home")
    if page_module:
        page_module.show()
else:
    if st.session_state.mode == "client":
        if menu == "Accueil":
            page_module = load_page("home")
        elif menu == "Reserver":
            page_module = load_page("book")
        elif menu == "Historique":
            page_module = load_page("history")
        elif menu == "Profil":
            page_module = load_page("profile")
        elif menu == "Creer un compte":
            page_module = load_page("signup")
        elif menu == "Paramètres":
            page_module = load_page("settings")
        else:
            page_module = None
        if page_module:
            page_module.show()
    elif st.session_state.mode == "prestataire":
        if menu == "Accueil":
            page_module = load_page("home")
        elif menu == "Stationnement":
            page_module = load_page("book_pilot")
        elif menu == "Reservations recues":
            st.info("🛠️ Page Réservations reçues en construction")
            page_module = None
        elif menu == "Creer un compte":
            page_module = load_page("signup")
        elif menu == "Paramètres":
            page_module = load_page("settings")
        else:
            page_module = None
        if page_module:
            page_module.show()

# ============================================
# FOOTER
# ============================================
if show_sidebar:
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 15px 0 5px 0;">
        <p style="color: #4A4F58; font-size: 11px; letter-spacing: 1px;">
            <span style="color: #FFD700; opacity: 0.6;">◆</span> MyJetSlot Yacht &amp; Marine <span style="color: #FFD700; opacity: 0.6;">◆</span>
        </p>
        <p style="color: #3A3F48; font-size: 10px; letter-spacing: 0.5px; margin-top: 3px;">
            Tunisie &nbsp;·&nbsp; © 2026
        </p>
    </div>
    """, unsafe_allow_html=True)