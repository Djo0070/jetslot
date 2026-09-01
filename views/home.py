import streamlit as st
import base64
import datetime

def get_logo_base64(size="normal"):
    if size == "small":
        svg_code = '''
        <svg width="140" height="45" viewBox="0 0 140 45" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="goldSmall" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FFD700"/>
                    <stop offset="50%" stop-color="#F4A460"/>
                    <stop offset="100%" stop-color="#DAA520"/>
                </linearGradient>
            </defs>
            <text x="0" y="22" font-family="'Georgia', serif" font-weight="700" font-size="22" fill="url(#goldSmall)" letter-spacing="-2">M</text>
            <text x="20" y="22" font-family="'Georgia', serif" font-weight="700" font-size="22" fill="url(#goldSmall)" letter-spacing="-2">J</text>
            <text x="0" y="32" font-family="'Arial', sans-serif" font-weight="700" font-size="6" fill="url(#goldSmall)" letter-spacing="2.5">MYJETSLOT</text>
            <text x="0" y="39" font-family="'Arial', sans-serif" font-weight="400" font-size="4" fill="#6C6F78" letter-spacing="1.5">PRIVATE AVIATION &amp; YACHT</text>
        </svg>
        '''
    else:
        svg_code = '''
        <svg width="180" height="60" viewBox="0 0 180 60" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="goldNav" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FFD700"/>
                    <stop offset="50%" stop-color="#F4A460"/>
                    <stop offset="100%" stop-color="#DAA520"/>
                </linearGradient>
            </defs>
            <text x="0" y="28" font-family="'Georgia', serif" font-weight="700" font-size="28" fill="url(#goldNav)" letter-spacing="-2">M</text>
            <text x="26" y="28" font-family="'Georgia', serif" font-weight="700" font-size="28" fill="url(#goldNav)" letter-spacing="-2">J</text>
            <text x="0" y="42" font-family="'Arial', sans-serif" font-weight="700" font-size="8" fill="url(#goldNav)" letter-spacing="3">MYJETSLOT</text>
            <text x="0" y="52" font-family="'Arial', sans-serif" font-weight="400" font-size="5" fill="#6C6F78" letter-spacing="2">PRIVATE AVIATION &amp; YACHT</text>
        </svg>
        '''
    b64 = base64.b64encode(svg_code.encode()).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" style="height:{45 if size == "small" else 60}px; width:auto;">'


def get_hero_image_base64():
    try:
        with open("static/images/hero-bg.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    except FileNotFoundError:
        return None


def show():
    # ============================================
    # CSS STYLE VAUNT
    # ============================================
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Georgia&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 30px;
        }
        
        /* ===== HEADER ===== */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 25px 0 20px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.05);
            margin-bottom: 30px;
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .header-right {
            display: flex;
            align-items: center;
            gap: 25px;
        }
        
        .weather {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #B8C6E0;
            font-family: 'Arial', sans-serif;
            font-size: 14px;
        }
        
        .weather .temp {
            font-size: 18px;
            font-weight: 600;
            color: #FFD700;
        }
        
        .weather .condition {
            color: #6C6F78;
            font-size: 12px;
        }
        
        /* ===== CHOIX CLIENT / PRESTATAIRE ===== */
        .choice-section {
            margin: 20px 0 40px 0;
            padding: 30px 0;
            border-top: 1px solid rgba(255, 215, 0, 0.04);
            border-bottom: 1px solid rgba(255, 215, 0, 0.04);
        }
        
        .choice-title-section {
            font-family: 'Georgia', serif;
            font-size: 1.4rem;
            font-weight: 300;
            color: #FFD700;
            text-align: center;
            letter-spacing: 2px;
            margin-bottom: 20px;
        }
        
        .choice-container {
            display: flex;
            gap: 40px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .choice-card {
            background: rgba(26, 42, 74, 0.3);
            border: 1px solid rgba(255, 215, 0, 0.06);
            border-radius: 12px;
            padding: 25px 30px;
            text-align: center;
            transition: all 0.4s ease;
            flex: 1;
            max-width: 280px;
            min-width: 200px;
        }
        
        .choice-card:hover {
            border-color: rgba(255, 215, 0, 0.15);
            transform: translateY(-3px);
        }
        
        .choice-card .choice-title {
            font-family: 'Georgia', serif;
            font-size: 1.3rem;
            color: #FFD700;
            font-weight: 600;
            letter-spacing: 1.5px;
            margin-bottom: 4px;
        }
        
        .choice-card .choice-desc {
            font-family: 'Arial', sans-serif;
            font-size: 0.85rem;
            color: #B8C6E0;
            opacity: 0.7;
            line-height: 1.5;
            margin-bottom: 15px;
        }
        
        /* ===== HERO ===== */
        .hero-wrapper {
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 60px;
            width: 100%;
            min-height: 550px;
            background: #0A1628;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 22, 40, 0.55);
            z-index: 1;
        }
        
        .hero {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 60px 40px;
            width: 100%;
            min-height: 550px;
        }
        
        .hero .badge {
            font-family: 'Arial', sans-serif;
            font-size: 11px;
            color: #FFD700;
            letter-spacing: 4px;
            text-transform: uppercase;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 215, 0, 0.15);
            padding: 6px 18px;
            border-radius: 20px;
            background: rgba(255, 215, 0, 0.03);
        }
        
        .hero h1 {
            font-family: 'Georgia', serif;
            font-size: 4.5rem;
            font-weight: 300;
            color: #FFFFFF;
            letter-spacing: 4px;
            line-height: 1.1;
            margin-bottom: 15px;
        }
        
        .hero h1 .highlight {
            color: #FFD700;
        }
        
        .hero .subtitle {
            font-family: 'Arial', sans-serif;
            font-size: 1.15rem;
            color: #B8C6E0;
            max-width: 650px;
            line-height: 1.8;
            margin-bottom: 30px;
        }
        
        .hero .cta-group {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        /* ===== SECTIONS ===== */
        .section {
            margin: 70px 0;
        }
        
        .section-title {
            font-family: 'Georgia', serif;
            font-size: 2.2rem;
            font-weight: 300;
            color: #FFD700;
            letter-spacing: 2px;
            margin-bottom: 15px;
        }
        
        .section-title-center {
            text-align: center;
            font-size: 2.4rem;
        }
        
        .section-subtitle {
            font-family: 'Arial', sans-serif;
            font-size: 1.05rem;
            color: #B8C6E0;
            line-height: 1.8;
            max-width: 750px;
            margin-bottom: 30px;
        }
        
        .section-subtitle-center {
            text-align: center;
            margin-left: auto;
            margin-right: auto;
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
        }
        
        .grid-3 {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 30px;
        }
        
        .card {
            background: rgba(26, 42, 74, 0.4);
            border: 1px solid rgba(255, 215, 0, 0.04);
            border-radius: 12px;
            padding: 30px 25px;
            transition: all 0.4s ease;
        }
        
        .card:hover {
            border-color: rgba(255, 215, 0, 0.12);
            transform: translateY(-4px);
        }
        
        .card .number {
            font-family: 'Georgia', serif;
            font-size: 1.8rem;
            color: #FFD700;
            font-weight: 300;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        
        .card .icon {
            font-size: 2rem;
            margin-bottom: 10px;
        }
        
        .card .title {
            font-family: 'Georgia', serif;
            font-size: 1.2rem;
            color: #FFD700;
            margin-bottom: 8px;
        }
        
        .card .desc {
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            color: #B8C6E0;
            line-height: 1.6;
        }
        
        .card .list {
            list-style: none;
            padding: 0;
            margin-top: 10px;
        }
        
        .card .list li {
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            color: #B8C6E0;
            padding: 6px 0;
            padding-left: 20px;
            position: relative;
            line-height: 1.6;
        }
        
        .card .list li::before {
            content: "✦";
            position: absolute;
            left: 0;
            color: #FFD700;
            font-size: 12px;
        }
        
        /* ===== TEMOIGNAGES ===== */
        .testimonial {
            background: rgba(26, 42, 74, 0.3);
            border-left: 3px solid #FFD700;
            padding: 25px 30px;
            border-radius: 0 12px 12px 0;
        }
        
        .testimonial .text {
            font-family: 'Georgia', serif;
            font-size: 1.05rem;
            color: #B8C6E0;
            line-height: 1.8;
            font-style: italic;
        }
        
        .testimonial .author {
            font-family: 'Arial', sans-serif;
            font-size: 12px;
            color: #6C6F78;
            margin-top: 10px;
            letter-spacing: 1px;
        }
        
        .testimonial .author strong {
            color: #FFD700;
        }
        
        /* ===== STATS ===== */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat {
            text-align: center;
            padding: 20px;
            background: rgba(26, 42, 74, 0.3);
            border-radius: 12px;
            border: 1px solid rgba(255, 215, 0, 0.04);
        }
        
        .stat .number {
            font-family: 'Georgia', serif;
            font-size: 2.8rem;
            color: #FFD700;
            font-weight: 300;
        }
        
        .stat .label {
            font-family: 'Arial', sans-serif;
            font-size: 12px;
            color: #6C6F78;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-top: 5px;
        }
        
        /* ===== CTA BANNER ===== */
        .cta-banner {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.05), rgba(26, 42, 74, 0.5));
            border: 1px solid rgba(255, 215, 0, 0.08);
            border-radius: 16px;
            padding: 50px 40px;
            text-align: center;
            margin: 30px 0;
        }
        
        .cta-banner h2 {
            font-family: 'Georgia', serif;
            font-size: 2.2rem;
            font-weight: 300;
            color: #FFD700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }
        
        .cta-banner p {
            font-family: 'Arial', sans-serif;
            font-size: 1rem;
            color: #B8C6E0;
            max-width: 600px;
            margin: 0 auto 25px auto;
            line-height: 1.6;
        }
        
        /* ===== PAGE CARDS ===== */
        .page-card {
            background: rgba(26, 42, 74, 0.4);
            border: 1px solid rgba(255, 215, 0, 0.06);
            border-radius: 16px;
            padding: 35px 30px;
            transition: all 0.4s ease;
            text-align: center;
        }
        
        .page-card:hover {
            border-color: rgba(255, 215, 0, 0.15);
            transform: translateY(-6px);
            box-shadow: 0 10px 40px rgba(255, 215, 0, 0.05);
        }
        
        .page-card .icon {
            font-size: 2.2rem;
            margin-bottom: 10px;
            color: #FFD700;
            display: block;
        }
        
        .page-card .title {
            font-family: 'Georgia', serif;
            font-size: 1.5rem;
            color: #FFD700;
            margin-bottom: 10px;
        }
        
        .page-card .desc {
            font-family: 'Arial', sans-serif;
            font-size: 0.95rem;
            color: #B8C6E0;
            line-height: 1.7;
            margin-bottom: 20px;
        }
        
        /* ===== FOOTER ===== */
        .footer {
            text-align: center;
            padding: 30px 0 20px 0;
            border-top: 1px solid rgba(255, 215, 0, 0.03);
            margin-top: 40px;
        }
        
        .footer p {
            color: #3A3F48;
            font-size: 10px;
            letter-spacing: 1px;
        }
        
        /* ============================================
           TOUS LES BOUTONS STREAMLIT = TRANSPARENTS
           ============================================ */
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
        
        /* ===== BOUTONS SPÉCIFIQUES DANS LES CARTES ===== */
        .choice-card .stButton button,
        .page-card .stButton button,
        .cta-banner .stButton button {
            background: transparent !important;
            border: none !important;
            color: #FFD700 !important;
            padding: 6px 12px !important;
            font-size: 13px !important;
            font-weight: 400 !important;
        }
        
        .choice-card .stButton button:hover,
        .page-card .stButton button:hover,
        .cta-banner .stButton button:hover {
            background: rgba(255, 215, 0, 0.04) !important;
            border-radius: 4px !important;
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 1024px) {
            .grid-4 { grid-template-columns: 1fr 1fr; }
        }
        
        @media (max-width: 768px) {
            .header { flex-direction: column; gap: 15px; padding: 15px 0; }
            .header-right { flex-wrap: wrap; justify-content: center; }
            .hero h1 { font-size: 2.8rem; }
            .hero h1 .highlight { display: block; }
            .grid-2 { grid-template-columns: 1fr; }
            .grid-3 { grid-template-columns: 1fr; }
            .stats-container { grid-template-columns: 1fr 1fr; }
            .choice-container { flex-direction: column; align-items: center; }
            .choice-card { max-width: 100%; width: 100%; }
            .hero { padding: 40px 20px; min-height: 400px; }
            .hero .cta-group { flex-direction: column; align-items: center; }
            .hero .cta-group .stButton button { width: 100%; }
            .cta-banner { padding: 30px 20px; }
            .cta-banner h2 { font-size: 1.6rem; }
        }
        
        @media (max-width: 500px) {
            .hero h1 { font-size: 2rem; }
            .hero { padding: 30px 15px; min-height: 350px; }
            .stats-container { grid-template-columns: 1fr; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ============================================
    # MÉTÉO
    # ============================================
    weather_icon = "☀️"
    temperature = 32
    condition = "Très ensoleillé"

    # ============================================
    # HEADER SANS BOUTONS DE NAVIGATION
    # ============================================
    st.markdown(f"""
    <div class="main-container">
        <div class="header">
            <div class="header-left">
                {get_logo_base64("small")}
            </div>
            <div class="header-right">
                <div class="weather">
                    <span style="font-size:22px;">{weather_icon}</span>
                    <span class="temp">{temperature}°C</span>
                    <span class="condition">{condition}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ============================================
    # CHOIX CLIENT / PRESTATAIRE (EN HAUT)
    # ============================================
    st.markdown("""
    <div class="choice-section">
        <div class="choice-title-section">Choose your experience</div>
        <div class="choice-container">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-title">Client</div>
            <div class="choice-desc">Reserve a place on a luxury yacht</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Reserve now", key="client_btn_top", use_container_width=True):
            st.session_state.mode = "client"
            st.switch_page("app.py")

    with col2:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-title">Provider</div>
            <div class="choice-desc">Manage your slots and reservations</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Access pro space", key="prestataire_btn_top", use_container_width=True):
            st.session_state.mode = "prestataire"
            st.switch_page("app.py")

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # HERO AVEC IMAGE
    # ============================================
    hero_bg = get_hero_image_base64()
    
    if hero_bg:
        st.markdown(f"""
        <div class="hero-wrapper" style="background: url('{hero_bg}') center/cover no-repeat;">
            <div class="hero-overlay"></div>
            <div class="hero">
                <span class="badge">Step aboard</span>
                <h1>
                    Explore the<br><span class="highlight">Mediterranean</span>
                </h1>
                <p class="subtitle">
                    The first platform to book premium yacht slots in Tunisia.<br>
                    A luxury experience accessible in just a few clicks.
                </p>
                <div class="cta-group">
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2, gap="small")
        with col_btn1:
            if st.button("Book a slot", key="hero_book", use_container_width=True):
                st.session_state.mode = "client"
                st.switch_page("app.py")
        with col_btn2:
            if st.button("Discover more", key="hero_discover", use_container_width=True):
                st.query_params["page"] = "experience"
                st.rerun()
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hero-wrapper" style="background: linear-gradient(135deg, #1A2A4A, #0A1628);">
            <div class="hero-overlay" style="background: rgba(10, 22, 40, 0.3);"></div>
            <div class="hero">
                <span class="badge">Step aboard</span>
                <h1>
                    Explore the<br><span class="highlight">Mediterranean</span>
                </h1>
                <p class="subtitle">
                    The first platform to book premium yacht slots in Tunisia.<br>
                    A luxury experience accessible in just a few clicks.
                </p>
                <div class="cta-group">
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns(2, gap="small")
        with col_btn1:
            if st.button("Book a slot", key="hero_book_fallback", use_container_width=True):
                st.session_state.mode = "client"
                st.switch_page("app.py")
        with col_btn2:
            if st.button("Discover more", key="hero_discover_fallback", use_container_width=True):
                st.query_params["page"] = "experience"
                st.rerun()
        
        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ============================================
    # STATS
    # ============================================
    st.markdown("""
    <div class="stats-container">
        <div class="stat">
            <div class="number">50+</div>
            <div class="label">Yachts disponibles</div>
        </div>
        <div class="stat">
            <div class="number">12</div>
            <div class="label">Destinations</div>
        </div>
        <div class="stat">
            <div class="number">98%</div>
            <div class="label">Satisfaction client</div>
        </div>
        <div class="stat">
            <div class="number">24/7</div>
            <div class="label">Conciergerie</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # SECTION : CARDS POUR ACCÉDER AUX PAGES
    # ============================================
    st.markdown("""
    <div class="section">
        <h2 class="section-title section-title-center">Discover MyJetSlot</h2>
        <p class="section-subtitle section-subtitle-center">
            Explore our platform and find the perfect experience for your next voyage.
        </p>
        <div class="grid-3">
    """, unsafe_allow_html=True)

    col_exp, col_how, col_price = st.columns(3)
    
    with col_exp:
        st.markdown("""
        <div class="page-card">
            <span class="icon"></span>
            <div class="title">The Experience</div>
            <div class="desc">
                Luxury redefined. Discover our premium yacht slots and seamless booking process.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn more", key="card_experience", use_container_width=True):
            st.query_params["page"] = "experience"
            st.rerun()

    with col_how:
        st.markdown("""
        <div class="page-card">
            <span class="icon"></span>
            <div class="title">How It Works</div>
            <div class="desc">
                Book your dream yacht in three simple steps. From selection to boarding.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn more", key="card_how_it_works", use_container_width=True):
            st.query_params["page"] = "how_it_works"
            st.rerun()

    with col_price:
        st.markdown("""
        <div class="page-card">
            <span class="icon"></span>
            <div class="title">Pricing</div>
            <div class="desc">
                Transparent pricing with no hidden fees. Choose the plan that suits you.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Learn more", key="card_pricing", use_container_width=True):
            st.query_params["page"] = "pricing"
            st.rerun()

    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # SECTION : TEMOIGNAGE
    # ============================================
    st.markdown("""
    <div class="section">
        <div class="testimonial">
            <p class="text">
                "MyJetSlot makes luxury yacht rentals in Tunisia accessible to everyone. 
                A game‑changer for Mediterranean travel."
            </p>
            <div class="author">— <strong>Tunisia Travel</strong> Review</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # SECTION : HOW IT WORKS (raccourci)
    # ============================================
    st.markdown("""
    <div class="section">
        <h2 class="section-title">How it works</h2>
        <p class="section-subtitle">
            Book your dream yacht in three simple steps.
        </p>
        <div class="grid-3">
            <div class="card">
                <div class="number">01</div>
                <div class="title">Choose</div>
                <div class="desc">Browse available yachts and select your preferred date and destination.</div>
            </div>
            <div class="card">
                <div class="number">02</div>
                <div class="title">Book</div>
                <div class="desc">Secure your booking with our fast, secure payment system.</div>
            </div>
            <div class="card">
                <div class="number">03</div>
                <div class="title">Sail</div>
                <div class="desc">Arrive, board, and set sail. Everything is taken care of.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # CTA BANNER
    # ============================================
    st.markdown("""
    <div class="cta-banner">
        <h2>Ready to set sail?</h2>
        <p>Join MyJetSlot today and discover a new way to experience the Mediterranean.</p>
    """, unsafe_allow_html=True)
    
    if st.button("Book your first slot", key="cta_banner_btn", use_container_width=False):
        st.session_state.mode = "client"
        st.switch_page("app.py")
    
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

    # ============================================
    # FOOTER
    # ============================================
    st.markdown("""
    <div class="footer">
        <p>MyJetSlot — Yacht &amp; Marine Reservation &nbsp;·&nbsp; © 2026</p>
    </div>
    """, unsafe_allow_html=True)