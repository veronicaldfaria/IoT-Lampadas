import network
import time
from machine import Pin, ADC
from umqtt.simple import MQTTClient

# --- Configurações de Rede e MQTT ---
SSID = "Wokwi-GUEST"
PASSWORD = ""
# Usando o broker do exemplo que você achou
MQTT_BROKER = "broker.mqttdashboard.com" 
MQTT_TOPIC = b"esp32/potenciometro" # 'b' na frente cria bytes
CLIENT_ID = "esp32_publisher_pot_py" # ID Único

# --- Pinos ---
pot_pin = ADC(Pin(34))
pot_pin.atten(ADC.ATTN_11DB) # Configura para ler a escala completa (0-3.3V)

def connect_wifi():
    """Conecta ao Wi-Fi do Wokwi."""
    print(f"Conectando ao Wi-Fi: {SSID}")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="") # Adicionado 'end' para ficar na mesma linha
        time.sleep(0.5)
    print(f"\nWi-Fi Conectado! IP: {sta_if.ifconfig()[0]}")

def connect_mqtt():
    """Conecta ao broker MQTT."""
    print(f"Conectando ao MQTT Broker: {MQTT_BROKER}")
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.connect()
        print("MQTT Conectado!")
        return client
    except OSError as e:
        print(f"Falha ao conectar ao MQTT: {e}")
        time.sleep(5)
        return connect_mqtt() # Tenta novamente

# --- Execução Principal ---
connect_wifi()
client = connect_mqtt()

last_value = -1

while True:
    try:
        # Lê o valor do potenciômetro (0-4095)
        current_value = pot_pin.read()

        # Envia apenas se o valor mudar (para evitar spam)
        # Vamos adicionar uma pequena margem (histerese) para evitar ruído
        if abs(current_value - last_value) > 10:
            last_value = current_value
            
            # Converte o número para string e publica
            msg = str(current_value)
            client.publish(MQTT_TOPIC, msg)
            print(f"Publicado no tópico '{MQTT_TOPIC.decode()}': {msg}")

        time.sleep_ms(100) # Espera 100ms

    except OSError as e:
        print(f"Erro na publicação: {e}. Reconectando...")
        time.sleep(5)
        client = connect_mqtt() # Tenta reconectar se a publicação falhar
