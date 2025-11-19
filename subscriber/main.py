import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
import neopixel # Nova biblioteca para NeoPixel

# --- Configurações de Rede e MQTT ---
SSID = "Wokwi-GUEST"
PASSWORD = ""
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = b"esp32/potenciometro"
CLIENT_ID = "esp32_subscriber_neopixel_py" # ID Único (diferente do publisher)

# --- Configurações do NeoPixel ---
NEOPIXEL_PIN = 2     # Pino GPIO onde o DIN do NeoPixel está conectado
NUM_PIXELS = 12      # Número de LEDs no seu NeoPixel Ring (ajuste se for diferente)
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

def connect_wifi():
    """Conecta ao Wi-Fi do Wokwi."""
    print(f"Conectando ao Wi-Fi: {SSID}")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(f"\nWi-Fi Conectado! IP: {sta_if.ifconfig()[0]}")

# --- Callback: O que fazer quando uma mensagem chega ---
def mqtt_callback(topic, msg):
    """Função chamada quando uma mensagem é recebida."""
    try:
        print(f"Mensagem recebida no tópico '{topic.decode()}': {msg.decode()}")
        
        # Converte a mensagem (string) para um número inteiro
        pot_value = int(msg.decode()) # Valor de 0 a 4095

        # --- Controle de Brilho (0-255) ---
        # Mapeia o valor do potenciômetro (0-4095) para um brilho geral (0-255)
        # Vamos usar um brilho máximo ligeiramente menor para não cegar no Wokwi
        global_brightness = int(pot_value * 200 / 4095) # 0 a 200
        if global_brightness < 10: global_brightness = 0 # Desliga se muito baixo

        # --- Controle de Cor (Branco Frio para Quente) ---
        # 0 (potenciômetro min) = branco frio
        # 4095 (potenciômetro max) = branco quente (âmbar)

        # Para simular branco frio para quente, podemos variar o componente azul.
        # Mais azul = mais frio; Menos azul + mais vermelho/verde = mais quente.

        # Interpolamos a quantidade de azul (0 = quente, 255 = frio)
        blue_component = int(pot_value * 255 / 4095) # Invertemos o mapeamento para ir de 255 (frio) para 0 (quente)
        blue_component = 255 - blue_component # Agora 0 é frio, 255 é quente.
        blue_component = max(0, min(255, blue_component)) # Garante que está entre 0-255

        # Para a cor quente, aumentamos vermelho e verde para dar o tom âmbar
        # Quando o potenciômetro está no máximo (quente), azul é 0, vermelho e verde são maiores.
        # Quando está no mínimo (frio), azul é 255, vermelho e verde são menores.
        
        # Um "branco" básico para o NeoPixel é (R, G, B)
        # Vamos definir R e G fixos ou com uma leve variação para o tom quente
        red_base = 255
        green_base = 255
        
        # Ajuste fino: diminui um pouco o azul para deixar mais "quente"
        # Quando pot_value é baixo, blue_component é ~255 (branco puro)
        # Quando pot_value é alto, blue_component é ~0 (mais amarelo/vermelho)
        
        # Aqui, vamos fazer uma interpolação mais direta para o tom
        # Branco Frio (Exemplo): (200, 200, 255) - mais azul
        # Branco Quente (Exemplo): (255, 180, 50) - mais vermelho/amarelo

        # Interpola entre dois pontos:
        # Ponto A (pot_value = 0): (200, 200, 255)
        # Ponto B (pot_value = 4095): (255, 180, 50)
        
        # Normaliza o pot_value para uma escala de 0.0 a 1.0
        t = pot_value / 4095.0

        # Interpola cada componente de cor
        r = int(200 * (1 - t) + 255 * t)
        g = int(200 * (1 - t) + 180 * t)
        b = int(255 * (1 - t) + 50 * t)

        # Aplica o brilho geral
        r = int(r * global_brightness / 255)
        g = int(g * global_brightness / 255)
        b = int(b * global_brightness / 255)

        # Garante que os valores fiquem entre 0 e 255
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        color = (r, g, b)
        print(f"Brilho: {global_brightness}, Cor (R,G,B): {color}")

        # Define a cor para todos os LEDs do anel
        for i in range(NUM_PIXELS):
            np[i] = color
        np.write() # Envia os dados para o NeoPixel

    except Exception as e:
        print(f"Erro no callback: {e}")

def connect_mqtt():
    """Conecta ao broker MQTT e se inscreve no tópico."""
    print(f"Conectando ao MQTT Broker: {MQTT_BROKER}")
    try:
        client = MQTTClient(CLIENT_ID, MQTT_BROKER)
        client.set_callback(mqtt_callback) # Configura a função de callback
        client.connect()
        client.subscribe(MQTT_TOPIC) # Se inscreve no tópico
        print(f"MQTT Conectado e inscrito no tópico '{MQTT_TOPIC.decode()}'")
        return client
    except OSError as e:
        print(f"Falha ao conectar ao MQTT: {e}")
        time.sleep(5)
        return connect_mqtt() # Tenta novamente

# --- Execução Principal ---
connect_wifi()
client = connect_mqtt()

# Desliga todos os LEDs ao iniciar
for i in range(NUM_PIXELS):
    np[i] = (0, 0, 0)
np.write()

while True:
    try:
        client.check_msg()
        time.sleep_ms(50) 
        
    except OSError as e:
        print(f"Erro na conexão MQTT: {e}. Reconectando...")
        time.sleep(5)
        client = connect_mqtt()
