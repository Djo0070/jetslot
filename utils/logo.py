import streamlit as st

def get_logo_html():
    return """
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    @keyframes glowPulse {
        0% { filter: drop-shadow(0 0 5px rgba(255,215,0,0.2)); }
        50% { filter: drop-shadow(0 0 25px rgba(255,215,0,0.5)); }
        100% { filter: drop-shadow(0 0 5px rgba(255,215,0,0.2)); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .logo-container {
        animation: fadeInUp 1.2s ease-out;
        display: inline-block;
        position: relative;
        margin: 0 auto;
        text-align: center;
        width: 100%;
    }
    .logo-svg-wrapper {
        animation: float 4s ease-in-out infinite;
        display: inline-block;
    }
    .logo-svg-wrapper svg {
        display: block;
        width: 280px;
        max-width: 100%;
        height: auto;
        animation: glowPulse 3s ease-in-out infinite;
    }
    @media (max-width: 600px) {
        .logo-svg-wrapper svg { width: 220px; }
    }
    </style>
    <div class="logo-container">
        <div class="logo-svg-wrapper">
            <svg viewBox="0 0 320 110" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FFF8DC"/>
                        <stop offset="20%" stop-color="#FFD700"/>
                        <stop offset="50%" stop-color="#F4A460"/>
                        <stop offset="80%" stop-color="#DAA520"/>
                        <stop offset="100%" stop-color="#B8860B"/>
                    </linearGradient>
                    <linearGradient id="goldShine" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.6"/>
                        <stop offset="50%" stop-color="#FFD700" stop-opacity="0.3"/>
                        <stop offset="100%" stop-color="#B8860B" stop-opacity="0"/>
                    </linearGradient>
                    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#0A1628"/>
                        <stop offset="50%" stop-color="#14203E"/>
                        <stop offset="100%" stop-color="#1A2A4A"/>
                    </linearGradient>
                    <filter id="shadow3d" x="-10%" y="-10%" width="130%" height="130%">
                        <feDropShadow dx="3" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.6"/>
                        <feDropShadow dx="-1" dy="-1" stdDeviation="2" flood-color="#FFD700" flood-opacity="0.15"/>
                    </filter>
                    <filter id="glow3d" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur stdDeviation="3" result="blur"/>
                        <feMerge>
                            <feMergeNode in="blur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <rect x="0" y="0" width="320" height="110" rx="16" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="1.5" filter="url(#shadow3d)"/>
                <ellipse cx="160" cy="55" rx="130" ry="35" fill="url(#goldGrad)" opacity="0.03"/>
                <text x="30" y="62" font-family="'Georgia', serif" font-weight="700" font-size="58" fill="url(#goldGrad)" letter-spacing="-4" filter="url(#glow3d)">M</text>
                <text x="78" y="62" font-family="'Georgia', serif" font-weight="700" font-size="58" fill="url(#goldGrad)" letter-spacing="-4" filter="url(#glow3d)">J</text>
                <text x="30" y="62" font-family="'Georgia', serif" font-weight="700" font-size="58" fill="url(#goldShine)" letter-spacing="-4" opacity="0.3" transform="translate(0, -2)">M</text>
                <text x="78" y="62" font-family="'Georgia', serif" font-weight="700" font-size="58" fill="url(#goldShine)" letter-spacing="-4" opacity="0.3" transform="translate(0, -2)">J</text>
                <circle cx="68" cy="40" r="3" fill="url(#goldGrad)" opacity="0.5"/>
                <circle cx="68" cy="48" r="3" fill="url(#goldGrad)" opacity="0.3"/>
                <circle cx="68" cy="56" r="3" fill="url(#goldGrad)" opacity="0.15"/>
                <g transform="translate(0, -4)" filter="url(#shadow3d)">
                    <path d="M105 32 L118 25 L126 25 L122 32 L132 32 L129 37 L122 37 L118 43 L105 43 L109 37 L101 37 L105 32Z" fill="url(#goldGrad)"/>
                    <path d="M105 32 L118 25 L126 25 L122 32 L132 32 L129 37 L122 37 L118 43 L105 43 L109 37 L101 37 L105 32Z" fill="url(#goldShine)" opacity="0.2"/>
                    <path d="M132 34 L148 34" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.3"/>
                    <path d="M132 36 L155 36" stroke="url(#goldGrad)" stroke-width="1" opacity="0.15"/>
                </g>
                <g filter="url(#shadow3d)">
                    <path d="M100 52 L115 48 L130 52 L145 48 L160 52" stroke="url(#goldGrad)" stroke-width="2.5" fill="none" stroke-linecap="round"/>
                    <path d="M100 52 L115 48 L130 52 L145 48 L160 52" stroke="url(#goldShine)" stroke-width="1" fill="none" opacity="0.3"/>
                </g>
                <g filter="url(#shadow3d)">
                    <text x="170" y="45" font-family="'Georgia', serif" font-weight="700" font-size="22" fill="url(#goldGrad)" letter-spacing="6" filter="url(#glow3d)">MYJETSLOT</text>
                    <text x="170" y="45" font-family="'Georgia', serif" font-weight="700" font-size="22" fill="url(#goldShine)" letter-spacing="6" opacity="0.3" transform="translate(0, -1)"/>
                </g>
                <text x="170" y="62" font-family="'Arial', sans-serif" font-weight="400" font-size="9" fill="#B8C6E0" letter-spacing="4.5">PRIVATE AVIATION &amp; YACHT</text>
                <line x1="30" y1="75" x2="290" y2="75" stroke="url(#goldGrad)" stroke-width="0.8" opacity="0.15"/>
                <line x1="30" y1="77" x2="290" y2="77" stroke="url(#goldGrad)" stroke-width="0.4" opacity="0.08"/>
                <rect x="25" y="72" width="6" height="6" rx="1" fill="url(#goldGrad)" opacity="0.25"/>
                <rect x="289" y="72" width="6" height="6" rx="1" fill="url(#goldGrad)" opacity="0.25"/>
            </svg>
        </div>
    </div>
    """

def show_logo():
    """Affiche le logo 3D animé dans Streamlit"""
    st.markdown(get_logo_html(), unsafe_allow_html=True)