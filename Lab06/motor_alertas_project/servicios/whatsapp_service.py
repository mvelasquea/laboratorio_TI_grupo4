import pywhatkit
import time

def enviar_whatsapp(usuario, mensaje):
    """
    Envía la alerta de IoT a través de WhatsApp Web de forma automática.
    """
    numero_destino = usuario.get("telefono")
    nombre_usuario = usuario.get("nombre")
    
    print(f"[SERVICIO WHATSAPP] Abriendo navegador para enviar alerta a {nombre_usuario}...")
    print(f"[DESTINATARIO] {numero_destino}")
    print("[PRECAUCION] No toques el teclado ni el mouse mientras se abre la pestaña.")
    
    try:
        # Abre la pestaña, espera 15 segundos a que cargue WhatsApp Web, escribe el mensaje,
        # lo envía presionando Enter automáticamente y luego cierra la pestaña.
        pywhatkit.sendwhatmsg_instantly(
            phone_no=numero_destino,
            message=mensaje,
            wait_time=15,
            tab_close=True
        )
        print(f"[WHATSAPP ENVIADO] {numero_destino}")
        time.sleep(2)  # Pausa de estabilidad antes de regresar al flujo principal
        
    except Exception as e:
        print(f"[ERROR] Error crítico en el módulo de WhatsApp: {e}")
        print("[SUGERENCIA] Verifica que WhatsApp Web esté logueado en tu navegador por defecto.")
    
    print("-" * 50)