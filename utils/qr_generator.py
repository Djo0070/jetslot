import qrcode
import io
import base64
from PIL import Image
from io import BytesIO


import qrcode
import io
import base64
from PIL import Image

def generate_qr_code(data, size=8):
    """Génère un QR Code en base64"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # QR en OR sur fond sombre
    img = qr.make_image(fill_color="#FFD700", back_color="#0A1628")
    
    # Convertir en base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64

def create_booking_qr_data(booking_id, parking_type, location, arrival_date, arrival_time, departure_date, departure_time, vehicle_name):
    """Crée les données du QR Code"""
    return f"""
    JETSLOT - STATIONNEMENT
    ID: {booking_id}
    Type: {parking_type}
    Lieu: {location}
    Arrivee: {arrival_date} a {arrival_time}
    Depart: {departure_date} a {departure_time}
    Vehicule: {vehicle_name}
    """

def get_qr_html(qr_base64, booking_id):
    """Génère le HTML du QR Code à afficher"""
    return f"""
    <div style="
        background: #0A1628; 
        padding: 20px; 
        border-radius: 12px; 
        border: 2px solid #FFD700;
        text-align: center;
        max-width: 300px;
        margin: 0 auto;
    ">
        <img src="data:image/png;base64,{qr_base64}" width="200" height="200" style="border-radius: 8px;">
        <p style="color: #FFD700; font-weight: bold; margin-top: 10px;">✅ Entree autorisee</p>
        <p style="color: #B8C6E0; font-size: 11px;">ID: {booking_id[:8]}... Presentez ce QR a l'entree</p>
    </div>
    """

def get_qr_download_button(qr_base64, booking_id):
    """Crée un bouton de téléchargement pour le QR Code"""
    # Décoder le QR Code
    qr_bytes = base64.b64decode(qr_base64)
    qr_file = BytesIO(qr_bytes)
    
    return qr_file, f"JetSlot_QR_{booking_id}.png"

def generate_qr_code(data, size=8):
    import qrcode
    import io
    import base64
    from PIL import Image
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=size,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#FFD700", back_color="#0A1628")
    
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return img_base64  
    qr_with_prefix = f"data:image/png;base64,{qr_base64}"