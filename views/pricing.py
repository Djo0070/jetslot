import streamlit as st
import base64

def get_pricing_hero_base64():
    try:
        with open("static/images/pricing-hero.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    except FileNotFoundError:
        return None

def show():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Georgia&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        .pricing-hero {
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            margin-bottom: 40px;
            width: 100%;
            min-height: 280px;
            background: #0A1628;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .pricing-hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 22, 40, 0.6);
            z-index: 1;
        }

        .pricing-hero-content {
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 40px 20px;
            width: 100%;
        }

        .pricing-hero-content .badge {
            font-family: 'Arial', sans-serif;
            font-size: 11px;
            color: #FFD700;
            letter-spacing: 4px;
            text-transform: uppercase;
            border: 1px solid rgba(255, 215, 0, 0.15);
            padding: 4px 16px;
            border-radius: 20px;
            background: rgba(255, 215, 0, 0.03);
            display: inline-block;
            margin-bottom: 15px;
        }

        .pricing-hero-content h1 {
            font-family: 'Georgia', serif;
            font-size: 3rem;
            font-weight: 300;
            color: #FFD700;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .pricing-hero-content p {
            font-family: 'Arial', sans-serif;
            font-size: 1.1rem;
            color: #B8C6E0;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.7;
        }

        .pricing-container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 20px 40px 20px;
        }

        .pricing-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 10px;
        }

        .pricing-card {
            background: linear-gradient(145deg, rgba(26, 42, 74, 0.5), rgba(10, 22, 40, 0.85));
            border: 1px solid rgba(255, 215, 0, 0.04);
            border-radius: 16px;
            padding: 35px 25px;
            text-align: center;
            transition: all 0.4s ease;
        }

        .pricing-card:hover {
            transform: translateY(-6px);
            border-color: rgba(255, 215, 0, 0.12);
            box-shadow: 0 10px 40px rgba(255, 215, 0, 0.04);
        }

        .pricing-card.featured {
            border-color: rgba(255, 215, 0, 0.2);
            background: linear-gradient(145deg, rgba(255, 215, 0, 0.04), rgba(26, 42, 74, 0.6));
        }

        .pricing-card .badge {
            font-family: 'Arial', sans-serif;
            font-size: 10px;
            color: #FFD700;
            background: rgba(255, 215, 0, 0.08);
            padding: 3px 14px;
            border-radius: 12px;
            letter-spacing: 1px;
            display: inline-block;
            margin-bottom: 12px;
            text-transform: uppercase;
        }

        .pricing-card .plan {
            font-family: 'Georgia', serif;
            font-size: 1.5rem;
            color: #FFD700;
            letter-spacing: 1px;
        }

        .pricing-card .price {
            font-family: 'Georgia', serif;
            font-size: 3rem;
            color: #FFD700;
            margin: 10px 0 4px 0;
        }

        .pricing-card .period {
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            color: #6C6F78;
            letter-spacing: 1px;
        }

        .pricing-card .features {
            list-style: none;
            padding: 0;
            margin: 20px 0;
            text-align: left;
        }

        .pricing-card .features li {
            font-family: 'Arial', sans-serif;
            font-size: 0.9rem;
            color: #B8C6E0;
            padding: 6px 0;
            border-bottom: 1px solid rgba(255, 215, 0, 0.03);
            opacity: 0.8;
        }

        .pricing-card .features li::before {
            content: "◆ ";
            color: #FFD700;
            font-weight: bold;
        }

        /* ===== BOUTONS TRANSPARENTS ===== */
        .pricing-card .stButton button {
            background: transparent !important;
            color: #FFD700 !important;
            border: 1px solid rgba(255, 215, 0, 0.2) !important;
            padding: 8px 28px !important;
            border-radius: 30px !important;
            font-family: 'Arial', sans-serif !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            margin-top: 10px !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        .pricing-card .stButton button:hover {
            background: rgba(255, 215, 0, 0.05) !important;
            border-color: #FFD700 !important;
            transform: scale(1.02);
        }

        .back-btn {
            margin: 20px 0 0 0;
        }

        /* ===== BOUTON RETOUR TRANSPARENT ===== */
        .stButton button {
            background: transparent !important;
            border: none !important;
            color: #FFD700 !important;
            font-family: 'Arial', sans-serif !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            letter-spacing: 1px !important;
            padding: 6px 12px !important;
            box-shadow: none !important;
        }
        .stButton button:hover {
            background: rgba(255, 215, 0, 0.04) !important;
            border-radius: 6px !important;
        }

        @media (max-width: 768px) {
            .pricing-grid { grid-template-columns: 1fr; }
            .pricing-hero-content h1 { font-size: 2.2rem; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== BOUTON RETOUR =====
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("← Retour", key="back_pricing"):
            st.query_params.clear()
            st.rerun()

    # ===== HERO =====
    hero_bg = get_pricing_hero_base64()
    if hero_bg:
        st.markdown(f"""
        <div class="pricing-hero" style="background: url('{hero_bg}') center/cover no-repeat;">
            <div class="pricing-hero-overlay"></div>
            <div class="pricing-hero-content">
                <span class="badge">Transparent Pricing</span>
                <h1>Simple. Transparent. Fair.</h1>
                <p>Choose the plan that fits your yacht journey</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="pricing-hero" style="background: linear-gradient(135deg, #1A2A4A, #0A1628);">
            <div class="pricing-hero-overlay" style="background: rgba(10, 22, 40, 0.2);"></div>
            <div class="pricing-hero-content">
                <span class="badge">Transparent Pricing</span>
                <h1>Simple. Transparent. Fair.</h1>
                <p>Choose the plan that fits your yacht journey</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ===== CONTENU =====
    st.markdown('<div class="pricing-container">', unsafe_allow_html=True)
    st.markdown('<div class="pricing-grid">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan">Starter</div>
            <div class="price">€99</div>
            <div class="period">per month</div>
            <ul class="features">
                <li>1 yacht slot per month</li>
                <li>Premium yacht selection</li>
                <li>Basic support</li>
                <li>Email notifications</li>
            </ul>
        """, unsafe_allow_html=True)
        if st.button("Get Started", key="starter_btn"):
            st.session_state.mode = "client"
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="pricing-card featured">
            <span class="badge">Most Popular</span>
            <div class="plan">Pro</div>
            <div class="price">€299</div>
            <div class="period">per month</div>
            <ul class="features">
                <li>5 yacht slots per month</li>
                <li>Premium yacht selection</li>
                <li>Priority support</li>
                <li>QR Code access</li>
                <li>5% loyalty discount</li>
            </ul>
        """, unsafe_allow_html=True)
        if st.button("Choose Pro", key="pro_btn"):
            st.session_state.mode = "client"
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="pricing-card">
            <div class="plan">Unlimited</div>
            <div class="price">€799</div>
            <div class="period">per month</div>
            <ul class="features">
                <li>Unlimited yacht slots</li>
                <li>Premium & luxury yachts</li>
                <li>VIP support</li>
                <li>QR Code access</li>
                <li>15% loyalty discount</li>
                <li>Priority booking</li>
            </ul>
        """, unsafe_allow_html=True)
        if st.button("Go Unlimited", key="unlimited_btn"):
            st.session_state.mode = "client"
            st.switch_page("app.py")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)