# data/locations.py
# Coordonnées des aéroports et ports

AIRPORT_COORDINATES = {
    "Nice Côte d'Azur (NCE)": {"lat": 43.6584, "lng": 7.2158},
    "Paris Le Bourget (LBG)": {"lat": 48.9694, "lng": 2.4433},
    "Monaco Héliport (MCM)": {"lat": 43.7324, "lng": 7.4190},
    "Genève (GVA)": {"lat": 46.2406, "lng": 6.1088},
    "Dubaï Al Maktoum (DWC)": {"lat": 24.8964, "lng": 55.1614},
    "Tunis Carthage (TUN)": {"lat": 36.8500, "lng": 10.2270},
    "Miami Opa-Locka (OPF)": {"lat": 25.9069, "lng": -80.2744},
    # Ajoute d'autres aéroports...
}

PORT_COORDINATES = {
    "Port de Monaco": {"lat": 43.7324, "lng": 7.4190},
    "Port de Cannes": {"lat": 43.5528, "lng": 7.0177},
    "Port de Saint-Tropez": {"lat": 43.2692, "lng": 6.6385},
    "Port de Marseille": {"lat": 43.3125, "lng": 5.3693},
    # Ajoute d'autres ports...
}

def get_coordinates(location_name):
    """Récupère les coordonnées d'un lieu"""
    if location_name in AIRPORT_COORDINATES:
        return AIRPORT_COORDINATES[location_name]
    elif location_name in PORT_COORDINATES:
        return PORT_COORDINATES[location_name]
    return {"lat": 0, "lng": 0}