import streamlit as st
import base64

def get_experience_hero_base64():
    try:
        with open("static/images/experience-hero.jpg", "rb") as f:
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

        .exp-hero {
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

        .exp-hero-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(10, 22, 40, 0.6);
            z-index: 1;
        }

        .exp-hero-content {
            position: relative;
            z-index: 2;
            text-align: center;
            padding: 40px 20px;
            width: 100%;
        }

        .exp-hero-content .badge {
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

        .exp-hero-content h1 {
            font-family: 'Georgia', serif;
            font-size: 3rem;
            font-weight: 300;
            color: #FFD700;
            letter-spacing: 2px;
            margin-bottom: 8px;
        }

        .exp-hero-content p {
            font-family: 'Arial', sans-serif;
            font-size: 1.1rem;
            color: #B8C6E0;
            max-width: 600px;
            margin: 0 auto;
            line-height: 1.7;
        }

        .experience-container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 20px 40px 20px;
        }

        .exp-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 10px;
        }

        .exp-card {
            background: linear-gradient(145deg, rgba(26, 42, 74, 0.5), rgba(10, 22, 40, 0.85));
            border: 1px solid rgba(255, 215, 0, 0.04);
            border-radius: 16px;
            padding: 30px;
            transition: all 0.4s ease;
        }

        .exp-card:hover {
            transform: translateY(-6px);
            border-color: rgba(255, 215, 0, 0.12);
            box-shadow: 0 10px 40px rgba(255, 215, 0, 0.04);
        }

        .exp-card .icon {
            font-size: 2rem;
            display: block;
            margin-bottom: 10px;
            color: #FFD700;
            font-weight: 300;
            letter-spacing: 2px;
        }

        .exp-card .title {
            font-family: 'Georgia', serif;
            font-size: 1.3rem;
            color: #FFD700;
            letter-spacing: 1px;
        }

        .exp-card .desc {
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
            .exp-grid { grid-template-columns: 1fr; }
            .exp-hero-content h1 { font-size: 2.2rem; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ===== BOUTON RETOUR =====
    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("← Retour", key="back_experience"):
            st.query_params.clear()
            st.rerun()

    # ===== HERO =====
    hero_bg = get_experience_hero_base64()
    if hero_bg:
        st.markdown(f"""
        <div class="exp-hero" style="background: url('{hero_bg}') center/cover no-repeat;">
            <div class="exp-hero-overlay"></div>
            <div class="exp-hero-content">
                <span class="badge">Luxury Redefined</span>
                <h1>The MyJetSlot Experience</h1>
                <p>Simple. Transparent. Accessible.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="exp-hero" style="background: linear-gradient(135deg, #1A2A4A, #0A1628);">
            <div class="exp-hero-overlay" style="background: rgba(10, 22, 40, 0.2);"></div>
            <div class="exp-hero-content">
                <span class="badge">Luxury Redefined</span>
                <h1>The MyJetSlot Experience</h1>
                <p>Simple. Transparent. Accessible.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ===== CONTENU =====
    st.markdown('<div class="experience-container">', unsafe_allow_html=True)
    st.markdown('<div class="exp-grid">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="exp-card">
            <span class="icon"></span>
            <div class="title">Premium Yachts</div>
            <div class="desc">Experience the freedom of the open sea with our curated selection of luxury yacht slots across the Mediterranean.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="exp-card">
            <span class="icon"></span>
            <div class="title">Premium Service</div>
            <div class="desc">Enjoy white‑glove service from booking to departure. Our team ensures every detail is taken care of for a flawless experience.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="exp-card">
            <span class="icon"></span>
            <div class="title">Seamless Parking</div>
            <div class="desc">Reserve parking slots for your yacht with ease. Our platform ensures your vessel is ready when you arrive.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="exp-card">
            <span class="icon"></span>
            <div class="title">Mediterranean Adventure</div>
            <div class="desc">Explore the most beautiful destinations along the Tunisian coast. Each journey is a unique experience.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    </div>
    </div>
    """, unsafe_allow_html=True)