import streamlit as st
import folium
from streamlit_folium import folium_static

# Coordonnées des aéroports et ports
AIRPORT_COORDINATES = {
    "Nice Côte d'Azur (NCE) - France": {"lat": 43.6584, "lng": 7.2158},
    "Paris Le Bourget (LBG) - France": {"lat": 48.9694, "lng": 2.4433},
    "Monaco Héliport (MCM) - Monaco": {"lat": 43.7324, "lng": 7.4190},
    "Genève (GVA) - Suisse": {"lat": 46.2406, "lng": 6.1088},
    "Dubaï Al Maktoum (DWC) - Émirats Arabes Unis": {"lat": 24.8964, "lng": 55.1614},
    "Tunis Carthage (TUN) - Tunisie": {"lat": 36.8500, "lng": 10.2270},
    "Miami Opa-Locka (OPF) - USA": {"lat": 25.9069, "lng": -80.2744},
    "Djerba (DJE) - Tunisie": {"lat": 33.8750, "lng": 10.7750},
    "Marrakech (RAK) - Maroc": {"lat": 31.6069, "lng": -8.0363},
    "Barcelone (BCN) - Espagne": {"lat": 41.2971, "lng": 2.0785},
}

PORT_COORDINATES = {
    "Port de Monaco - Monaco": {"lat": 43.7324, "lng": 7.4190},
    "Port de Cannes - France": {"lat": 43.5528, "lng": 7.0177},
    "Port de Saint-Tropez - France": {"lat": 43.2692, "lng": 6.6385},
    "Port de Marseille - France": {"lat": 43.3125, "lng": 5.3693},
    "Port de Nice - France": {"lat": 43.6957, "lng": 7.2704},
    "Port de Barcelone - Espagne": {"lat": 41.3745, "lng": 2.1868},
    "Port de Mykonos - Grèce": {"lat": 37.4467, "lng": 25.3289},
    "Dubaï Marina - Émirats Arabes Unis": {"lat": 25.0820, "lng": 55.1454},
}

def get_coordinates(location_name):
    """Récupère les coordonnées d'un lieu"""
    if location_name in AIRPORT_COORDINATES:
        return AIRPORT_COORDINATES[location_name]
    elif location_name in PORT_COORDINATES:
        return PORT_COORDINATES[location_name]
    return {"lat": 0, "lng": 0}

def display_location_map(location_name, lat=None, lng=None):
    """Affiche une carte avec le lieu"""
    
    # Si lat/lng non fournis, on les cherche
    if lat is None or lng is None:
        coords = get_coordinates(location_name)
        lat = coords.get("lat", 0)
        lng = coords.get("lng", 0)
    
    if lat == 0 and lng == 0:
        st.warning("📍 Coordonnées non disponibles pour ce lieu")
        return
    
    # Créer la carte
    m = folium.Map(
        location=[lat, lng],
        zoom_start=13,
        tiles="CartoDB dark_matter",
        control_scale=True
    )
    
    # Ajouter un marqueur personnalisé
    folium.Marker(
        [lat, lng],
        popup=f"""
        <div style="font-family: Georgia; font-size: 14px;">
            <b style="color: #FFD700;">{location_name}</b>
        </div>
        """,
        tooltip=location_name,
        icon=folium.Icon(color="gold", icon="plane", prefix="fa")
    ).add_to(m)
    
    # Ajouter un cercle autour du lieu
    folium.Circle(
        location=[lat, lng],
        radius=500,
        color="#FFD700",
        fill=True,
        fill_color="#FFD700",
        fill_opacity=0.08,
    ).add_to(m)
    
    # Afficher la carte
    folium_static(m, width=700, height=350)