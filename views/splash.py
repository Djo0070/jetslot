import streamlit as st

def show():
    st.markdown("""
    <style>
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes floatYacht {
            0% { transform: translateX(-30px) translateY(0px); }
            50% { transform: translateX(30px) translateY(-10px); }
            100% { transform: translateX(-30px) translateY(0px); }
        }
        @keyframes waveMove {
            0% { transform: translateX(0); }
            100% { transform: translateX(-200px); }
        }
        @keyframes shimmer {
            0% { background-position: -300% center; }
            100% { background-position: 300% center; }
        }
        @keyframes progress {
            0% { width: 0%; }
            100% { width: 100%; }
        }

        .splash-container {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(180deg, #0A1628 0%, #0F2A4A 45%, #1A3A5A 70%, #0F2A4A 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 99999;
            overflow: hidden;
            width: 100vw;
            height: 100vh;
            animation: fadeIn 0.6s ease-out;
        }

        .sea-container {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 200%;
            height: 40%;
            overflow: hidden;
        }
        .wave {
            position: absolute;
            bottom: -5%;
            left: 0;
            width: 200%;
            height: 120%;
            border-radius: 50% 50% 0 0 / 40% 40% 0 0;
            animation: waveMove 8s linear infinite;
        }
        .wave:nth-child(1) {
            background: radial-gradient(ellipse at 30% 100%, rgba(255,215,0,0.05) 0%, transparent 70%);
            animation-duration: 6s;
        }
        .wave:nth-child(2) {
            background: radial-gradient(ellipse at 70% 100%, rgba(255,215,0,0.03) 0%, transparent 70%);
            animation-duration: 8s;
            animation-delay: -2s;
            bottom: -10%;
        }
        .wave:nth-child(3) {
            background: radial-gradient(ellipse at 50% 100%, rgba(255,215,0,0.02) 0%, transparent 70%);
            animation-duration: 10s;
            animation-delay: -4s;
            bottom: -15%;
        }

        .scene {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 90%;
            max-width: 600px;
        }

        .yacht-wrapper {
            width: 100%;
            display: flex;
            justify-content: center;
            animation: floatYacht 4s ease-in-out infinite;
        }
        .yacht-wrapper svg {
            width: 320px;
            max-width: 90%;
            height: auto;
            filter: drop-shadow(0 20px 50px rgba(0,0,0,0.5));
        }

        .divider {
            width: 120px;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,215,0,0.3), transparent);
            margin: 15px 0 12px 0;
        }

        .splash-title {
            font-family: 'Georgia', serif;
            font-size: 3.5rem;
            font-weight: 300;
            background: linear-gradient(135deg, #FFD700 0%, #F4A460 30%, #DAA520 60%, #FFD700 100%);
            background-size: 300% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: 10px;
            animation: slideUp 1.2s ease-out, shimmer 6s linear infinite;
        }
        .splash-title .highlight {
            -webkit-text-fill-color: #F4A460;
        }

        .splash-subtitle {
            font-family: 'Arial', sans-serif;
            font-size: 0.7rem;
            color: rgba(255,215,0,0.2);
            letter-spacing: 8px;
            text-transform: uppercase;
            animation: slideUp 1.6s ease-out;
            margin-top: 4px;
        }

        .progress-wrapper {
            margin-top: 40px;
            width: 200px;
            text-align: center;
            z-index: 2;
        }
        .progress-track {
            width: 100%;
            height: 1.5px;
            background: rgba(255,215,0,0.06);
            border-radius: 2px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #DAA520, #FFD700);
            border-radius: 2px;
            animation: progress 2.5s ease-in-out forwards;
        }
        .progress-label {
            font-family: 'Arial', sans-serif;
            font-size: 8px;
            color: rgba(255,215,0,0.1);
            letter-spacing: 4px;
            margin-top: 8px;
        }

        @media (max-width: 768px) {
            .yacht-wrapper svg { width: 220px; }
            .splash-title { font-size: 2.4rem; letter-spacing: 6px; }
            .splash-subtitle { font-size: 0.55rem; letter-spacing: 4px; }
            .scene { width: 95%; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ============================================
    # HTML COMPLET AVEC SVG INTÉGRÉ (SANS VARIABLE)
    # ============================================
    st.markdown("""
    <div class="splash-container">
        <div class="sea-container">
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
        </div>
        <div class="scene">
            <div class="yacht-wrapper">
                <svg viewBox="0 0 400 160" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="hull" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#FFFFFF"/>
                            <stop offset="40%" stop-color="#E8ECF1"/>
                            <stop offset="100%" stop-color="#B8C0CA"/>
                        </linearGradient>
                        <linearGradient id="deck" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#F5F7FA"/>
                            <stop offset="100%" stop-color="#D5DAE0"/>
                        </linearGradient>
                        <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#FFD700"/>
                            <stop offset="50%" stop-color="#F4A460"/>
                            <stop offset="100%" stop-color="#DAA520"/>
                        </linearGradient>
                        <filter id="shadow">
                            <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.4"/>
                        </filter>
                    </defs>
                    <path d="M20 130 Q60 120 100 130 Q140 140 180 130 Q220 120 260 130 Q300 140 340 130 Q370 120 390 130 L390 160 L20 160Z" fill="rgba(255,215,0,0.04)"/>
                    <path d="M40 110 L80 100 L140 96 L260 96 L320 100 L360 108 L370 114 L360 120 L320 128 L260 132 L140 132 L80 128 L40 120Z" fill="url(#hull)" filter="url(#shadow)"/>
                    <line x1="50" y1="116" x2="355" y2="116" stroke="#A0A8B4" stroke-width="0.8"/>
                    <path d="M120 100 L180 100 L200 94 L250 94 L270 100 L280 104 L250 104 L200 100 L120 100Z" fill="url(#deck)"/>
                    <circle cx="100" cy="112" r="5" fill="#1A2A4A" stroke="#B0B8C4" stroke-width="0.8"/>
                    <circle cx="140" cy="112" r="5" fill="#1A2A4A" stroke="#B0B8C4" stroke-width="0.8"/>
                    <circle cx="180" cy="112" r="5" fill="#1A2A4A" stroke="#B0B8C4" stroke-width="0.8"/>
                    <circle cx="220" cy="112" r="5" fill="#1A2A4A" stroke="#B0B8C4" stroke-width="0.8"/>
                    <circle cx="260" cy="112" r="5" fill="#1A2A4A" stroke="#B0B8C4" stroke-width="0.8"/>
                    <circle cx="300" cy="112" r="5" fill="#1A2A4A" stroke="#B0B8C4" stroke-width="0.8"/>
                    <path d="M60 108 L340 108" stroke="url(#gold)" stroke-width="2" opacity="0.5"/>
                    <path d="M200 94 L240 94 L250 88 L270 88 L280 94 L250 94 L200 94Z" fill="#DDE2E8"/>
                    <path d="M220 94 L230 86 L260 86 L270 94Z" fill="#E8ECF1" stroke="#B0B8C4" stroke-width="0.5"/>
                    <path d="M10 126 Q50 118 90 126 Q130 134 170 126 Q210 118 250 126 Q290 134 330 126 Q360 120 390 126" stroke="#FFD700" stroke-width="1.5" fill="none" opacity="0.15"/>
                    <path d="M0 138 Q40 130 80 138 Q120 146 160 138 Q200 130 240 138 Q280 146 320 138 Q350 132 380 138" stroke="#FFD700" stroke-width="1" fill="none" opacity="0.08"/>
                    <path d="M80 104 L200 102 L200 106 L80 108Z" fill="white" opacity="0.1"/>
                </svg>
            </div>
            <div class="divider"></div>
            <div class="splash-title">My<span class="highlight">Jet</span>Slot</div>
            <div class="splash-subtitle">Private Aviation &amp; Yacht</div>
            <div class="progress-wrapper">
                <div class="progress-track">
                    <div class="progress-bar"></div>
                </div>
                <div class="progress-label">CHARGEMENT</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)