import json
import os
import time

# Importaciones de tus módulos locales de servicios y lógica
from servicios.email_service import enviar_email
from servicios.whatsapp_service import enviar_whatsapp
from core.evaluador import evaluar_lectura

def cargar_configuracion():
    """
    Carga los datos del usuario utilizando rutas absolutas automáticas
    para evitar errores de ejecución desde distintas carpetas.
    """
    # Detecta la localización exacta de este archivo main.py
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    
    # Construye la ruta hacia config/usuarios.json
    ruta_usuarios = os.path.join(directorio_actual, "config", "usuarios.json")
    
    with open(ruta_usuarios, "r", encoding="utf-8") as f:
        return json.load(f)

def ejecutar_motor():
    # 1. Inicializar datos de usuario destinatario
    try:
        usuario = cargar_configuracion()
    except FileNotFoundError:
        print("[ERROR] No se encontró el archivo de configuración en 'config/usuarios.json'.")
        return

    print("╔================================================╗")
    print("║  INICIANDO SISTEMA DE MONITOREO AUTOMÁTICO IoT  ║")
    print("╚================================================╝")
    print(f"Monitoreando activamente para: {usuario['nombre']}\n")
    
    # 2. Localizar y cargar el historial de los sensores industriales e IoT
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_sensores = os.path.join(directorio_actual, "data", "sensores_data.json")
    
    try:
        with open(ruta_sensores, "r", encoding="utf-8") as f:
            lecturas = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Archivo de datos no encontrado en: {ruta_sensores}")
        print("Por favor, asegúrate de haber creado el archivo 'sensores_data.json' dentro de la carpeta 'data'.")
        return

    # 3. Ciclo de procesamiento de tramas de sensores paso a paso
    total_lecturas = len(lecturas)
    for indice, registro in enumerate(lecturas, start=1):
        print(f"\n[Procesando Registro {indice}/{total_lecturas}]")
        
        # Evalúa las reglas de negocio y dispara alertas reales si es necesario
        evaluar_lectura(registro, usuario, enviar_email, enviar_whatsapp)
        
        # Si no es el último registro, esperamos 22 segundos para dar tiempo
        # a que las pestañas automatizadas de WhatsApp carguen, envíen y cierren limpiamente.
        if indice < total_lecturas:
            print("[ESPERA] 22 segundos para la siguiente telemetría...")
            time.sleep(22)
            
    print("\n╔================================================╗")
    print("║  PROCESAMIENTO DE TELEMETRÍA FINALIZADO         ║")
    print("╚================================================╝")

if __name__ == "__main__":
    ejecutar_motor()