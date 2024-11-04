import network
import time
import random
from umqtt.simple import MQTTClient
import ujson

# Configuración del Wi-Fi
ssid = 'mosquito'
password = 'abcd1234'

# Configuración de MQTT
MQTT_BROKER = '192.168.76.166'  # Cambia esto por la IP de tu servidor
MQTT_TOPIC = 'sensor/datos'
MQTT_USER = 'nehir'        # Cambia esto por tu usuario de MQTT
MQTT_PASSWORD = 'nehir1234'  # Cambia esto por tu contraseña de MQTT

# Conectar a Wi-Fi
nic = network.WLAN(network.STA_IF)
nic.active(True)
print(nic.scan())  # Mostrar las redes disponibles
nic.connect(ssid, password)
while not nic.isconnected():
    print("[INFO] Connecting to wifi....")
    time.sleep(1)
print("[INFO] Wi-Fi connected!")

# Función para enviar datos
def publish_data():
    # Conectar a MQTT con usuario y contraseña
    client = MQTTClient("esp32_client", MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
    
    try:
        client.connect()
        print('Conectado al broker MQTT')
    except Exception as e:
        print('Error al conectar al broker MQTT:', e)
        return

    while True:
        # Generar datos aleatorios
        humedad = random.uniform(10, 30)
        inclinacion = random.uniform(10, 30)
        vibracion = random.uniform(10, 30)
        timestamp = int(time.time())
        
        data = {
            "id_equipo":"esp32",
            "humedad": humedad,
            "inclinacion": inclinacion,
            "vibracion": vibracion,
            "timestamo" : timestamp
        }
        
        # Publicar datos
        payload = ujson.dumps(data)
        try:
            client.publish(MQTT_TOPIC, payload)
            print(f"Datos enviados: {payload}")
        except Exception as e:
            print("Error al enviar datos:", e)
        
        time.sleep(5)  # Publicar cada 5 segundos

# Iniciar la publicación
publish_data()

