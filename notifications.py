import os
import streamlit as st
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# EMAIL : CONFIRMATION DE RÉSERVATION (CLIENT)
# ============================================
CONFIRMATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Confirmation</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #FFD700;">
                <h1 style="color: #FFD700; font-size: 36px; margin: 0; letter-spacing: 4px; font-family: 'Georgia', serif;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #FFD700; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Confirmation de reservation</h2>
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #FFD700; font-weight: bold;">Bonjour,</span>
                </p>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Nous avons le plaisir de vous confirmer votre reservation <span style="color: #FFD700; font-weight: bold;">#{{ id or booking_id }}</span>.
                </p>
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #FFD700;">
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FFD700;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FFD700;">Date :</strong> {{ date }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FFD700;">Heure :</strong> {{ time }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FFD700;">Duree :</strong> {{ duration }} minutes</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FFD700;">ID de reservation :</strong> #{{ id or booking_id }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FFD700;">Statut :</strong> <span style="color: #4CAF50; font-weight: bold;">Confirme</span></td></tr>
                </table>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">
                    Vous pouvez gerer vos reservations depuis votre espace personnel sur JetSlot.<br>
                    Pour toute question, notre equipe est a votre disposition.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #FFD700; font-size: 15px; margin: 0; font-weight: bold; letter-spacing: 1px;">Aner Youssef</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0; letter-spacing: 1px;">Fondateur, JetSlot</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">contact@myjetslot.com | +447411201949</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    <a href="www.myjetslot.com" style="color: #FFD700; text-decoration: none;">www.myjetslot.com</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Support</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Conditions</a>
                </p>
                <p style="color: #4A4F58; font-size: 11px; margin: 15px 0 0 0; letter-spacing: 0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# ============================================
# EMAIL : ANNULATION DE RÉSERVATION (CLIENT)
# ============================================
CANCELLATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Annulation</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #FF4444;">
                <h1 style="color: #FF4444; font-size: 36px; margin: 0; letter-spacing: 4px; font-family: 'Georgia', serif;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #FF4444; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Annulation de reservation</h2>
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #FF4444; font-weight: bold;">Bonjour,</span>
                </p>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Nous vous confirmons l'annulation de votre reservation <span style="color: #FF4444; font-weight: bold;">#{{ id or booking_id }}</span>.
                </p>
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #FF4444;">
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Date :</strong> {{ date }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Heure :</strong> {{ time }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">ID de reservation :</strong> #{{ id or booking_id }}</td></tr>
                </table>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">
                    Si vous n'etes pas a l'origine de cette annulation, contactez-nous immediatement.<br>
                    Pour toute question, notre equipe est a votre disposition.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #FFD700; font-size: 15px; margin: 0; font-weight: bold; letter-spacing: 1px;">Aner Youssef</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0; letter-spacing: 1px;">Fondateur, JetSlot</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">contact@myjetslot.com | +447411201949</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    <a href="www.myjetslot.com" style="color: #FFD700; text-decoration: none;">www.myjetslot.com</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Support</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Conditions</a>
                </p>
                <p style="color: #4A4F58; font-size: 11px; margin: 15px 0 0 0; letter-spacing: 0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# ============================================
# EMAIL : RAPPEL 24H AVANT (CLIENT)
# ============================================
REMINDER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Rappel</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #F4A460;">
                <h1 style="color: #F4A460; font-size: 36px; margin: 0; letter-spacing: 4px;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #F4A460; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Rappel de reservation</h2>
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #F4A460; font-weight: bold;">Bonjour,</span>
                </p>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Ceci est un rappel : votre reservation <span style="color: #F4A460; font-weight: bold;">#{{ id or booking_id }}</span> a lieu demain.
                </p>
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #F4A460;">
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #F4A460;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #F4A460;">Date :</strong> {{ date }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #F4A460;">Heure :</strong> {{ time }}</td></tr>
                </table>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">Nous vous rappelons que vous devez presenter votre QR Code a l'entree.</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #4A4F58; font-size: 11px; margin: 0; letter-spacing: 0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# ============================================
# EMAIL : NOUVELLE RÉSERVATION (PRESTATAIRE)
# ============================================
PRESTATAIRE_NEW_BOOKING_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Nouvelle reservation</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #4CAF50;">
                <h1 style="color: #4CAF50; font-size: 36px; margin: 0; letter-spacing: 4px;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #4CAF50; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Nouvelle reservation</h2>
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #4CAF50; font-weight: bold;">Bonjour,</span>
                </p>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Un client a reserve l'un de vos creneaux <span style="color: #4CAF50; font-weight: bold;">#{{ booking_id }}</span>.
                </p>
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #4CAF50;">
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #4CAF50;">Client :</strong> {{ client_name }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #4CAF50;">Email :</strong> {{ client_email }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #4CAF50;">Telephone :</strong> {{ client_telephone }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #4CAF50;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #4CAF50;">Date :</strong> {{ date }} a {{ time }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #4CAF50;">Prix :</strong> {{ price }}€</td></tr>
                </table>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">Connectez-vous a votre espace prestataire pour gerer cette reservation.</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #4A4F58; font-size: 11px; margin: 0; letter-spacing: 0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# ============================================
# EMAIL : REFUS DE RÉSERVATION (CLIENT) - NOUVEAU
# ============================================
REFUSED_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Refus</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A1628; font-family: 'Georgia', 'Times New Roman', serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #0A1628; padding: 20px;">
        <tr>
            <td align="center" style="padding: 30px 0 20px 0; border-bottom: 2px solid #FF4444;">
                <h1 style="color: #FF4444; font-size: 36px; margin: 0; letter-spacing: 4px; font-family: 'Georgia', serif;">JetSlot</h1>
                <p style="color: #B8C6E0; font-size: 12px; letter-spacing: 3px; margin: 5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding: 30px 20px; color: #E8EAF0;">
                <h2 style="color: #FF4444; font-size: 22px; margin: 0 0 20px 0; font-weight: 300; letter-spacing: 2px;">Reservation refusee</h2>
                <p style="font-size: 16px; line-height: 1.8; color: #B8C6E0;">
                    <span style="color: #FF4444; font-weight: bold;">Bonjour,</span>
                </p>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0; margin-top: 10px;">
                    Nous regrettons de vous informer que votre reservation <span style="color: #FF4444; font-weight: bold;">#{{ id or booking_id }}</span> a ete refusee.
                </p>
                <table style="width: 100%; margin: 20px 0; background-color: #1A2A4A; border-radius: 8px; padding: 15px; border-left: 3px solid #FF4444;">
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Date :</strong> {{ date }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Heure :</strong> {{ time }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">ID de reservation :</strong> #{{ id or booking_id }}</td></tr>
                    <tr><td style="padding: 8px 0; color: #B8C6E0; font-size: 14px;"><strong style="color: #FF4444;">Statut :</strong> <span style="color: #FF4444; font-weight: bold;">Refuse</span></td></tr>
                </table>
                <p style="font-size: 15px; line-height: 1.8; color: #B8C6E0;">
                    Votre remboursement sera effectue sous 48h.<br>
                    Pour toute question, notre equipe est a votre disposition.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px 0 10px 0; border-top: 1px solid #2A3A5A; text-align: center;">
                <p style="color: #FFD700; font-size: 15px; margin: 0; font-weight: bold; letter-spacing: 1px;">Aner Youssef</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0; letter-spacing: 1px;">Fondateur, JetSlot</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">contact@myjetslot.com | +447411201949</p>
                <p style="color: #6C6F78; font-size: 12px; margin: 5px 0 0 0;">
                    <a href="www.myjetslot.com" style="color: #FFD700; text-decoration: none;">www.myjetslot.com</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Support</a> | 
                    <a href="#" style="color: #FFD700; text-decoration: none;">Conditions</a>
                </p>
                <p style="color: #4A4F58; font-size: 11px; margin: 15px 0 0 0; letter-spacing: 0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# ============================================
# EMAIL : STATIONNEMENT AVEC QR
# ============================================
PARKING_CONFIRMATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Confirmation stationnement</title>
</head>
<body style="margin:0;padding:0;background-color:#0A1628;font-family:'Georgia','Times New Roman',serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;background-color:#0A1628;padding:20px;">
        <tr>
            <td align="center" style="padding:30px 0 20px 0;border-bottom:2px solid #FFD700;">
                <h1 style="color:#FFD700;font-size:36px;margin:0;letter-spacing:4px;">JetSlot</h1>
                <p style="color:#B8C6E0;font-size:12px;letter-spacing:3px;margin:5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding:30px 20px;color:#E8EAF0;">
                <h2 style="color:#FFD700;font-size:22px;margin:0 0 20px 0;font-weight:300;letter-spacing:2px;">Confirmation de stationnement</h2>
                <p style="font-size:16px;line-height:1.8;color:#B8C6E0;">
                    <span style="color:#FFD700;font-weight:bold;">Bonjour,</span>
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;margin-top:10px;">
                    Votre reservation de stationnement <span style="color:#FFD700;font-weight:bold;">#{{ booking_id }}</span> a ete confirmee.
                </p>
                <table style="width:100%;margin:20px 0;background-color:#1A2A4A;border-radius:8px;padding:15px;border-left:3px solid #FFD700;">
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Type :</strong> {{ parking_type }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Arrivee :</strong> {{ arrival_date }} a {{ arrival_time }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Depart :</strong> {{ departure_date }} a {{ departure_time }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Duree :</strong> {{ duration_days }} jour(s)</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Total :</strong> {{ total_price }}€</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#FFD700;">Vehicule :</strong> {{ vehicle_name }}</td></tr>
                </table>
                <div style="text-align:center;background:#0A1628;border-radius:8px;padding:20px;margin:20px 0;border:2px solid #FFD700;">
                    <h3 style="color:#FFD700;font-weight:300;letter-spacing:2px;">QR Code d'entree</h3>
                    <img src="data:image/png;base64,{{ qr_base64 }}" width="200" height="200" style="border-radius:8px;margin:10px 0;border:2px solid #FFD700;">
                    <p style="color:#B8C6E0;font-size:13px;margin:10px 0 0 0;">Presentez ce QR Code a l'entree</p>
                </div>
            </td>
        </tr>
        <tr>
            <td style="padding:20px 0 10px 0;border-top:1px solid #2A3A5A;text-align:center;">
                <p style="color:#4A4F58;font-size:11px;margin:0;letter-spacing:0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

# ============================================
# FONCTION D'ENVOI D'EMAIL
# ============================================
def send_email(to_email, subject, html_content):
    """Envoie un email avec Gmail SMTP"""
    try:
        smtp_user = os.getenv("EMAIL_SENDER")
        smtp_password = os.getenv("EMAIL_PASSWORD")
        
        if not smtp_user or not smtp_password:
            st.error("EMAIL_SENDER ou EMAIL_PASSWORD non configures dans .env")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_content, 'html'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        
        st.success(f"Email envoye a {to_email}")
        return True
        
    except Exception as e:
        st.error(f"Erreur d'envoi email : {e}")
        return False

# ============================================
# FONCTIONS CLIENTS
# ============================================
def send_confirmation_email(email, booking_data):
    """Email de confirmation de reservation (client)"""
    try:
        template = Template(CONFIRMATION_TEMPLATE)
        booking_data['id'] = booking_data.get('id', booking_data.get('booking_id', ''))
        html = template.render(**booking_data)
        subject = f"JetSlot - Confirmation reservation #{booking_data['id']}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur confirmation : {e}")
        return False

def send_cancellation_email(email, booking_data):
    """Email d'annulation de reservation (client)"""
    try:
        template = Template(CANCELLATION_TEMPLATE)
        booking_data['id'] = booking_data.get('id', booking_data.get('booking_id', ''))
        html = template.render(**booking_data)
        subject = f"JetSlot - Annulation reservation #{booking_data['id']}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur annulation : {e}")
        return False

def send_reminder_email(email, booking_data):
    """Email de rappel 24h avant (client)"""
    try:
        template = Template(REMINDER_TEMPLATE)
        booking_data['id'] = booking_data.get('id', booking_data.get('booking_id', ''))
        html = template.render(**booking_data)
        subject = f"JetSlot - Rappel reservation #{booking_data['id']}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur rappel : {e}")
        return False

def send_refused_email(email, booking_data):
    """Email de refus de reservation (client) - NOUVEAU"""
    try:
        template = Template(REFUSED_TEMPLATE)
        booking_data['id'] = booking_data.get('id', booking_data.get('booking_id', ''))
        html = template.render(**booking_data)
        subject = f"JetSlot - Reservation refusee #{booking_data['id']}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur refus : {e}")
        return False

def send_booking_confirmation_email_with_qr(email, booking_data, qr_base64):
    """Email de confirmation avec QR Code (client)"""
    try:
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>JetSlot - Confirmation</title>
        </head>
        <body style="background-color:#0A1628;font-family:Georgia,serif;padding:20px;margin:0;">
            <div style="max-width:600px;margin:0 auto;background:#1A2A4A;border-radius:12px;padding:30px;border:1px solid #FFD700;">
                <h1 style="color:#FFD700;text-align:center;font-weight:300;letter-spacing:4px;">JetSlot</h1>
                <h2 style="color:#FFD700;text-align:center;font-weight:300;letter-spacing:2px;">Confirmation de reservation</h2>
                <div style="background:#0A1628;border-radius:8px;padding:20px;margin:20px 0;border:1px solid rgba(255,215,0,0.1);">
                    <p style="color:#B8C6E0;margin:8px 0;"><strong style="color:#FFD700;">ID :</strong> {{ booking_id }}</p>
                    <p style="color:#B8C6E0;margin:8px 0;"><strong style="color:#FFD700;">Type :</strong> {{ booking_type }}</p>
                    <p style="color:#B8C6E0;margin:8px 0;"><strong style="color:#FFD700;">Lieu :</strong> {{ location }}</p>
                    <p style="color:#B8C6E0;margin:8px 0;"><strong style="color:#FFD700;">Date :</strong> {{ date }} a {{ time }}</p>
                    <p style="color:#B8C6E0;margin:8px 0;"><strong style="color:#FFD700;">Duree :</strong> {{ duration }} min</p>
                    <p style="color:#B8C6E0;margin:8px 0;"><strong style="color:#FFD700;">Prix :</strong> {{ price }}€</p>
                </div>
                <div style="text-align:center;background:#0A1628;border-radius:8px;padding:20px;margin:20px 0;border:2px solid #FFD700;">
                    <h3 style="color:#FFD700;font-weight:300;letter-spacing:2px;">QR Code d'entree</h3>
                    <img src="data:image/png;base64,{{ qr_base64 }}" width="200" height="200" style="border-radius:8px;margin:10px 0;border:2px solid #FFD700;">
                    <p style="color:#B8C6E0;font-size:13px;margin:10px 0 0 0;">Presentez ce QR Code a l'entree</p>
                </div>
                <p style="color:#6C6F78;text-align:center;font-size:11px;margin-top:20px;border-top:1px solid rgba(255,215,0,0.1);padding-top:20px;">
                    JetSlot Technologies - Private Aviation &amp; Yacht<br>
                    © 2026 JetSlot
                </p>
            </div>
        </body>
        </html>
        """)
        booking_data['qr_base64'] = qr_base64
        html = template.render(**booking_data)
        subject = f"JetSlot - Confirmation reservation #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur email QR : {e}")
        return False

# ============================================
# FONCTIONS PRESTATAIRES
# ============================================
def send_prestataire_new_booking(email, booking_data):
    """Email : nouvelle reservation recue (prestataire)"""
    try:
        template = Template(PRESTATAIRE_NEW_BOOKING_TEMPLATE)
        html = template.render(**booking_data)
        subject = f"JetSlot - Nouvelle reservation #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur email prestataire : {e}")
        return False

def send_parking_confirmation_email_with_qr(email, booking_data, qr_base64):
    """Email de confirmation de stationnement avec QR Code"""
    try:
        template = Template(PARKING_CONFIRMATION_TEMPLATE)
        booking_data['qr_base64'] = qr_base64
        html = template.render(**booking_data)
        subject = f"JetSlot - Confirmation stationnement #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur email stationnement : {e}")
        return False

def send_pending_email(email, booking_data):
    """Email : Réservation en attente (SANS QR)"""
    try:
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>JetSlot - En attente</title></head>
        <body style="background-color:#0A1628;font-family:Georgia,serif;padding:20px;">
            <div style="max-width:600px;margin:0 auto;background:#1A2A4A;border-radius:12px;padding:30px;border:1px solid #F4A460;">
                <h1 style="color:#F4A460;text-align:center;">JetSlot</h1>
                <h2 style="color:#F4A460;text-align:center;">Reservation en attente</h2>
                <div style="background:#0A1628;border-radius:8px;padding:20px;">
                    <p><strong style="color:#F4A460;">ID :</strong> {{ booking_id }}</p>
                    <p><strong style="color:#F4A460;">Lieu :</strong> {{ location }}</p>
                    <p><strong style="color:#F4A460;">Date :</strong> {{ date }} a {{ time }}</p>
                    <p><strong style="color:#F4A460;">Prix :</strong> {{ price }}€</p>
                    <p><strong style="color:#F4A460;">Statut :</strong> <span style="color:#F4A460;">En attente de paiement</span></p>
                </div>
                <p style="color:#B8C6E0;text-align:center;">Veuillez proceder au paiement pour confirmer votre reservation.</p>
                <p style="color:#6C6F78;text-align:center;font-size:11px;">© 2026 JetSlot</p>
            </div>
        </body>
        </html>
        """)
        html = template.render(**booking_data)
        subject = f"JetSlot - Reservation en attente #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur pending email : {e}")
        return False

def send_confirmed_email_with_qr(email, booking_data, qr_base64):
    """Email : Réservation CONFIRMEE avec QR Code"""
    if qr_base64 and not qr_base64.startswith("data:image"):
        qr_base64 = f"data:image/png;base64,{qr_base64}"
    
    try:
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>JetSlot - Confirmee</title></head>
        <body style="background-color:#0A1628;font-family:Georgia,serif;padding:20px;">
            <div style="max-width:600px;margin:0 auto;background:#1A2A4A;border-radius:12px;padding:30px;border:1px solid #4CAF50;">
                <h1 style="color:#4CAF50;text-align:center;">JetSlot</h1>
                <h2 style="color:#4CAF50;text-align:center;">Reservation confirmee</h2>
                <div style="background:#0A1628;border-radius:8px;padding:20px;">
                    <p><strong style="color:#4CAF50;">ID :</strong> {{ booking_id }}</p>
                    <p><strong style="color:#4CAF50;">Lieu :</strong> {{ location }}</p>
                    <p><strong style="color:#4CAF50;">Date :</strong> {{ date }} a {{ time }}</p>
                    <p><strong style="color:#4CAF50;">Prix :</strong> {{ price }}€</p>
                    <p><strong style="color:#4CAF50;">Statut :</strong> <span style="color:#4CAF50;">Confirmee</span></p>
                </div>
                <div style="text-align:center;background:#0A1628;border-radius:8px;padding:20px;border:2px solid #4CAF50;">
                    <h3 style="color:#4CAF50;">QR Code d'entree</h3>
                    <img src="{{ qr_base64 }}" width="200" height="200" style="border-radius:8px;">
                    <p style="color:#B8C6E0;font-size:13px;">Presentez ce QR a l'entree</p>
                </div>
                <p style="color:#6C6F78;text-align:center;font-size:11px;">© 2026 JetSlot</p>
            </div>
        </body>
        </html>
        """)
        booking_data['qr_base64'] = qr_base64
        html = template.render(**booking_data)
        subject = f"JetSlot - Reservation confirmee #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur confirmed email : {e}")
        return False

# ============================================
# EMAIL : CODE DE VÉRIFICATION (INSCRIPTION)
# ============================================
VERIFICATION_CODE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Vérification</title>
</head>
<body style="margin:0;padding:0;background-color:#0A1628;font-family:'Georgia','Times New Roman',serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;background-color:#0A1628;padding:20px;">
        <tr>
            <td align="center" style="padding:30px 0 20px 0;border-bottom:2px solid #FFD700;">
                <h1 style="color:#FFD700;font-size:36px;margin:0;letter-spacing:4px;">JetSlot</h1>
                <p style="color:#B8C6E0;font-size:12px;letter-spacing:3px;margin:5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding:30px 20px;color:#E8EAF0;">
                <h2 style="color:#FFD700;font-size:22px;margin:0 0 20px 0;font-weight:300;letter-spacing:2px;">Vérification de votre compte</h2>
                <p style="font-size:16px;line-height:1.8;color:#B8C6E0;">
                    <span style="color:#FFD700;font-weight:bold;">Bonjour,</span>
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;margin-top:10px;">
                    Merci de vous être inscrit sur JetSlot. Pour activer votre compte, veuillez utiliser le code suivant :
                </p>
                <div style="background:#0A1628;border-radius:8px;padding:20px;text-align:center;border:2px solid #FFD700;margin:20px 0;">
                    <p style="color:#FFD700;font-size:36px;letter-spacing:10px;font-weight:bold;">{{ code }}</p>
                </div>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;">
                    Ce code expire dans <span style="color:#FFD700;font-weight:bold;">10 minutes</span>.
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;">
                    Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding:20px 0 10px 0;border-top:1px solid #2A3A5A;text-align:center;">
                <p style="color:#4A4F58;font-size:11px;margin:0;letter-spacing:0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def send_verification_code_email(email, code):
    """Envoie le code de vérification par email"""
    try:
        template = Template(VERIFICATION_CODE_TEMPLATE)
        html = template.render(code=code)
        subject = "JetSlot - Code de vérification"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur envoi code : {e}")
        return False


# ============================================
# AJOUTS : NOTIFICATION AÉROPORT + DEMANDE EN ATTENTE
# ============================================

# ============================================
# EMAIL : DEMANDE DE STATIONNEMENT À L'AÉROPORT
# ============================================
AIRPORT_NOTIFICATION_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Demande de stationnement</title>
</head>
<body style="margin:0;padding:0;background-color:#0A1628;font-family:'Georgia','Times New Roman',serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;background-color:#0A1628;padding:20px;">
        <tr>
            <td align="center" style="padding:30px 0 20px 0;border-bottom:2px solid #F4A460;">
                <h1 style="color:#F4A460;font-size:36px;margin:0;letter-spacing:4px;">JetSlot</h1>
                <p style="color:#B8C6E0;font-size:12px;letter-spacing:3px;margin:5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding:30px 20px;color:#E8EAF0;">
                <h2 style="color:#F4A460;font-size:22px;margin:0 0 20px 0;font-weight:300;letter-spacing:2px;">📋 Nouvelle demande de stationnement</h2>
                <p style="font-size:16px;line-height:1.8;color:#B8C6E0;">
                    <span style="color:#F4A460;font-weight:bold;">Bonjour,</span>
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;margin-top:10px;">
                    Une demande de stationnement a été soumise pour votre infrastructure.
                </p>
                <table style="width:100%;margin:20px 0;background-color:#1A2A4A;border-radius:8px;padding:15px;border-left:3px solid #F4A460;">
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">ID :</strong> {{ booking_id }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Arrivée :</strong> {{ arrival_date }} à {{ arrival_time }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Départ :</strong> {{ departure_date }} à {{ departure_time }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Durée :</strong> {{ duration_days }} jour(s)</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Véhicule :</strong> {{ vehicle_name }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Prestataire :</strong> {{ prestataire_nom }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Téléphone :</strong> {{ prestataire_telephone }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Email :</strong> {{ prestataire_email }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Total :</strong> {{ total_price }}€</td></tr>
                </table>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;">
                    Merci de confirmer ou refuser cette demande via votre espace prestataire.
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;margin-top:10px;border-top:1px solid rgba(255,215,0,0.1);padding-top:15px;">
                    🔗 <a href="#" style="color:#FFD700;text-decoration:none;">Accéder à l'espace prestataire</a>
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding:20px 0 10px 0;border-top:1px solid #2A3A5A;text-align:center;">
                <p style="color:#4A4F58;font-size:11px;margin:0;letter-spacing:0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def send_airport_notification_email(email, booking_data):
    """Email envoyé à l'aéroport/port pour une nouvelle demande"""
    try:
        template = Template(AIRPORT_NOTIFICATION_TEMPLATE)
        html = template.render(**booking_data)
        subject = f"JetSlot - Demande de stationnement #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur envoi notification aéroport : {e}")
        return False

# ============================================
# EMAIL : CONFIRMATION EN ATTENTE (PRESTATAIRE)
# ============================================
PARKING_PENDING_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JetSlot - Demande en attente</title>
</head>
<body style="margin:0;padding:0;background-color:#0A1628;font-family:'Georgia','Times New Roman',serif;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;background-color:#0A1628;padding:20px;">
        <tr>
            <td align="center" style="padding:30px 0 20px 0;border-bottom:2px solid #F4A460;">
                <h1 style="color:#F4A460;font-size:36px;margin:0;letter-spacing:4px;">JetSlot</h1>
                <p style="color:#B8C6E0;font-size:12px;letter-spacing:3px;margin:5px 0 0 0;">PRIVATE AVIATION &amp; YACHT</p>
            </td>
        </tr>
        <tr>
            <td style="padding:30px 20px;color:#E8EAF0;">
                <h2 style="color:#F4A460;font-size:22px;margin:0 0 20px 0;font-weight:300;letter-spacing:2px;">⏳ Demande en attente</h2>
                <p style="font-size:16px;line-height:1.8;color:#B8C6E0;">
                    <span style="color:#F4A460;font-weight:bold;">Bonjour {{ prestataire_nom }},</span>
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;margin-top:10px;">
                    Votre demande de stationnement <span style="color:#F4A460;font-weight:bold;">#{{ booking_id }}</span> a été envoyée à l'aéroport/port.
                </p>
                <table style="width:100%;margin:20px 0;background-color:#1A2A4A;border-radius:8px;padding:15px;border-left:3px solid #F4A460;">
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Lieu :</strong> {{ location }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Arrivée :</strong> {{ arrival_date }} à {{ arrival_time }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Départ :</strong> {{ departure_date }} à {{ departure_time }}</td></tr>
                    <tr><td style="padding:8px 0;color:#B8C6E0;font-size:14px;"><strong style="color:#F4A460;">Total :</strong> {{ total_price }}€</td></tr>
                </table>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;">
                    Vous recevrez une confirmation dès que votre réservation sera validée.
                </p>
                <p style="font-size:15px;line-height:1.8;color:#B8C6E0;margin-top:10px;border-top:1px solid rgba(255,215,0,0.1);padding-top:15px;">
                    🔗 <a href="#" style="color:#FFD700;text-decoration:none;">Suivre ma réservation</a>
                </p>
            </td>
        </tr>
        <tr>
            <td style="padding:20px 0 10px 0;border-top:1px solid #2A3A5A;text-align:center;">
                <p style="color:#4A4F58;font-size:11px;margin:0;letter-spacing:0.5px;">© 2026 JetSlot - Tous droits reserves</p>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def send_parking_pending_email(email, booking_data):
    """Email de confirmation de demande en attente (prestataire)"""
    try:
        template = Template(PARKING_PENDING_TEMPLATE)
        html = template.render(**booking_data)
        subject = f"JetSlot - Demande en attente #{booking_data.get('booking_id', '')}"
        return send_email(email, subject, html)
    except Exception as e:
        st.error(f"Erreur email pending parking : {e}")
        return False