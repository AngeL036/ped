import smtplib
import logging
from email.message import EmailMessage
from app.core.config import settings
logger = logging.getLogger(__name__)

def send_verification_email(to_email:str, token:str):

    verification_link = f"https://agsa.website/api/auth/verificar?token={token}"

    html = f"""
    <h2>Verifica tu cuenta</h2>
    <p>Da click en el siguiente enlace para verificar tu cuenta:</p>
    <a href="{verification_link}"
        style="padding:10px 20px; background:#111; color:white; text-decoration:none; border-radius:5px;"
    >
        Verificar cuenta
    </a>
    <p>Este enlace expirará en 1 hora.</p>
    """

    # Creación del mensaje
    email = EmailMessage()
    email["From"] = settings.email_user
    email["To"] = to_email
    email["Subject"] = "Verifica tu cuenta."

    email.set_content("Visita el enlacen para verificar tu cuenta.")
    email.add_alternative(html,subtype="html")

    #conexion y envio
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(settings.email_user, settings.email_password)
            smtp.send_message(email)
            logger.info(f"Email enviado a {to_email}")
            return True
    except smtplib.SMTPAuthenticationError:
        logger.error("Credenciales incorrectas")
    except smtplib.SMTPException as e:
        logger.error(f"Error SMTP: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")

    return False  
        