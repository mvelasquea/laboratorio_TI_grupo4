# Límites reglamentarios
TEMP_MAX = 8.0
TEMP_MIN = 2.0
TIEMPO_PUERTA_MAX = 15  # Segundos

def evaluar_lectura(registro, usuario, callback_email, callback_whatsapp):
    """
    Analiza las tramas de los sensores industriales y GPS contra las reglas de negocio.
    """
    timestamp = registro.get("timestamp")
    id_dispositivo = registro.get("dispositivo_id")
    
    # Extraer datos de los sub-objetos del JSON
    sensores = registro.get("sensores", {})
    gps = registro.get("gps", {})
    
    # Lecturas específicas de tu hardware
    temp_principal = sensores.get("DS18B20_temp")
    temp_precision = sensores.get("PT100_temp")
    humedad = sensores.get("SHT31_humedad")
    puerta_tiempo = sensores.get("puerta_abierta_segundos")
    
    # Datos de Ubicación (NEO-M8N / NEO-6M)
    lat = gps.get("latitud")
    lon = gps.get("longitud")
    velocidad = gps.get("velocidad_kmh")
    
    alertas = []

    # 1. Validación de Reglas Inteligentes usando hardware específico
    if temp_principal > TEMP_MAX:
        alertas.append(f"Alta Temperatura (DS18B20): {temp_principal}°C [PT100: {temp_precision}°C] (Límite: >{TEMP_MAX}°C)")
        
    if temp_principal < TEMP_MIN:
        alertas.append(f"Baja Temperatura (DS18B20): {temp_principal}°C [PT100: {temp_precision}°C] (Límite: <{TEMP_MIN}°C)")
        
    if puerta_tiempo > TIEMPO_PUERTA_MAX:
        alertas.append(f"Puerta Abierta por {puerta_tiempo}s (Límite: >{TIEMPO_PUERTA_MAX}s)")

    # 2. Procesamiento de Resultados
    if alertas:
        print(f"\n[ALERTA CRITICA EN RUTA] Unidad: {id_dispositivo} | {timestamp}")
        print(f"[UBICACION] Lat: {lat}, Lon: {lon} | Velocidad: {velocidad} km/h")
        for error in alertas:
            print(f"   [DETALLE] {error}")
            
        # Construcción del mensaje con telemetría integrada para el usuario
        mensaje_notificacion = (
            f"[ALERTA IOT] [{id_dispositivo}]\n"
            f"Hora: {timestamp}\n"
            f"Ubicación: https://maps.google.com/?q={lat},{lon}\n"
            f"Incidentes: " + " | ".join(alertas)
        )
        
        # Disparar alertas de inmediato
        callback_whatsapp(usuario, mensaje_notificacion)
        callback_email(usuario, f"CRÍTICO: Alerta IoT en Unidad {id_dispositivo}", mensaje_notificacion)
    else:
        print(f"[OK] {timestamp} | Unidad: {id_dispositivo} | Temp: {temp_principal}°C | Humedad: {humedad}% | Puerta: {puerta_tiempo}s | Ubicación normal.")