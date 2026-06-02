import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del servidor SMTP de Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# REEMPLAZA ESTOS DATOS CON LOS TUYOS:
REMITENTE_EMAIL = "mikhailvelasque15@gmail.com"  
REMITENTE_PASSWORD = "cymq tcnv xjyi orjd" # Las 16 letras que te dio Google (sin espacios)

def enviar_email(usuario, asunto, mensaje):
    """
    Se conecta al servidor SMTP de Gmail y envía un correo electrónico real.
    """
    print(f"[SERVICIO EMAIL] Intentando conectar a {SMTP_SERVER}...")
    
    # 1. Crear el contenedor del mensaje
    msg = MIMEMultipart()
    msg['From'] = REMITENTE_EMAIL
    msg['To'] = usuario['email']  # El correo del usuario cargado desde usuarios.json
    msg['Subject'] = asunto

    # 2. Adjuntar el cuerpo del mensaje
    msg.attach(MIMEText(mensaje, 'plain', 'utf-8'))

    try:
        # 3. Establecer conexión segura con el servidor SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Cifrado de seguridad
        
        # 4. Iniciar sesión y enviar
        server.login(REMITENTE_EMAIL, REMITENTE_PASSWORD)
        server.sendmail(REMITENTE_EMAIL, msg['To'], msg.as_string())
        
        print(f"[EMAIL ENVIADO] {msg['To']}")
    
    except Exception as e:
        print(f"[ERROR] Error al enviar el correo: {e}")
        print("[SUGERENCIA] Verifica tu conexión, que tu correo esté bien escrito o tu Contraseña de Aplicación.")
    
    finally:
        # 5. Cerrar la conexión de forma limpia
        try:
            server.quit()
        except:
            pass
    print("-" * 50)