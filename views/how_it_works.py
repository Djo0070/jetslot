import streamlit as st
import base64

def get_howitworks_hero_base64():
    try:
        with open("static/images/howitworks-hero.jpg", "rb") as f:
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

        .hiw-hero {
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

        .hiw-hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 22, 40, 0.6);
            z-index: 1;
        }

        .hiw-hero-content {
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 40px 20px;
            width: 100%;
        }

        .hiw-hero-content .badge {
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

        .hiw-hero-content h1 {
            font-family: 'Georgia', serif;
            font-size: 3rem;
            font-weight: 300;
            color: #FFD700;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .hiw-hero-content p {
            font-family: 'Arial', sans-serif;
            font-size: 1.1rem;
            color: #B8C6E0;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.7;
        }

        .hiw-container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 20px 40px 20px;
        }

        .hiw-steps {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 10px;
        }

        .hiw-step {
            background: linear-gradient(145deg, rgba(26, 42, 74, 0.5), rgba(10, 22, 40, 0.85));
            border: 1px solid rgba(255, 215, 0, 0.04);
            border-radius: 16px;
            padding: 35px 25px;
            text-align: center;
            transition: all 0.4s ease;
        }

        .hiw-step:hover {
            transform: translateY(-6px);
            border-color: rgba(255, 215, 0, 0.12);
            box-shadow: 0 10px 40px rgba(255, 215, 0, 0.04);
        }

        .hiw-step .number {
            font-family: 'Georgia', serif;
            font-size: 2.8rem;
            color: #FFD700;
            font-weight: 300;
            letter-spacing: 2px;
        }

        .hiw-step .title {
            font-family: 'Georgia', serif;
            font-size: 1.4rem;
            color: #FFD700;
            margin-top: 10px;
        }

        .hiw-step .desc {
            font-family: 'Arial', sans-serif;
            font-size: 0.95rem;
            color: #B8C6E0;
            line-height: 1.7;
            opacity: 0.8;
            margin-top: 8px;
        }

        /* ===== BOUTONS TRANSPARENTS ===== */
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

        .back-btn {
            margin: 20px 0 0 0;
        }

        @media (max-width: 768px) {
            .hiw-steps { grid-template-columns: 1fr; }
            .hiw-hero-content h1 { font-size: 2.2rem; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== BOUTON RETOUR =====
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("← Retour", key="back_howitworks"):
            st.query_params.clear()
            st.rerun()

    # ===== HERO =====
    hero_bg = get_howitworks_hero_base64()
    if hero_bg:
        st.markdown(f"""
        <div class="hiw-hero" style="background: url('{hero_bg}') center/cover no-repeat;">
            <div class="hiw-hero-overlay"></div>
            <div class="hiw-hero-content">
                <span class="badge">In 3 Simple Steps</span>
                <h1>How It Works</h1>
                <p>Three simple steps to luxury yacht rental</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hiw-hero" style="background: linear-gradient(135deg, #1A2A4A, #0A1628);">
            <div class="hiw-hero-overlay" style="background: rgba(10, 22, 40, 0.2);"></div>
            <div class="hiw-hero-content">
                <span class="badge">In 3 Simple Steps</span>
                <h1>How It Works</h1>
                <p>Three simple steps to luxury yacht rental</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ===== CONTENU =====
    st.markdown('<div class="hiw-container">', unsafe_allow_html=True)
    st.markdown('<div class="hiw-steps">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="hiw-step">
            <div class="number">01</div>
            <div class="title">Choose</div>
            <div class="desc">Select your destination and available yacht slot. Find the perfect yacht for your Mediterranean journey.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="hiw-step">
            <div class="number">02</div>
            <div class="title">Book</div>
            <div class="desc">Secure your spot in seconds. Our streamlined booking process makes luxury yacht rental effortless.</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="hiw-step">
            <div class="number">03</div>
            <div class="title">Sail</div>
            <div class="desc">Enjoy your premium yacht experience. Simply present your QR code at the marina and let your journey begin.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)