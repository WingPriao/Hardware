import urequests
from machine import Pin, Timer
import network
from umqtt.simple import MQTTClient
import time
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX, COINMARKETCAP_API_KEY
)

motion = False

pir_pin = Pin(14, Pin.IN)
pir_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

coin_selected = ""
index = 0

# Initialize WiFi Connection


def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    mac = ':'.join(f'{b:02X}' for b in wifi.config('mac'))
    print(f'WiFi MAC address is {mac}')
    wifi.active(True)
    print(f'Connecting to WiFi {WIFI_SSID}.')
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        print('.', end='')
        time.sleep(0.5)
    print('\nWiFi connected.')

# Initialize MQTT Connection


def connect_mqtt():
    mqtt = MQTTClient(client_id='', server=MQTT_BROKER,
                      user=MQTT_USER, password=MQTT_PASS)
    mqtt.connect()
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(f"{TOPIC_PREFIX}/coin")
    print('MQTT Connected.')
    return mqtt


def mqtt_callback(topic, payload):
    global coin_value

    if topic.decode() == f'{TOPIC_PREFIX}/coin':
        try:
            coin_select_input = payload.decode("utf-8")
            global coin_selected

            coin_selected = coin_select_input
        except ValueError:
            pass


# Fetch and Publish Cryptocurrency Prices
old_price = 0
is_alert = False


def fetch_and_publish_crypto_prices():
    global old_price
    global is_alert
    try:
        print("HOLA")
        url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest?symbol=BTC,ETH,BNB,SOL,AVAX,MATIC,OP,APT,OKB,TIA,ARB,MNT,SUI,SEI,MANTA,ZETA,DYM,STRK'
        headers = {'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}
        response = urequests.get(url, headers=headers)
        data = response.json()

        for symbol in data['data']:
            # Assuming each symbol has at least one entry and we're interested in the first one
            price_info = data['data'][symbol][0]['quote']['USD']
            price = price_info['price']
            topic = f'{TOPIC_PREFIX}/price'
            mqtt.publish(topic, f'{symbol},{price}')

            print(f'Published {symbol} Price: {price}')

            if coin_selected == symbol:
                if old_price > price:
                    is_alert = True
                old_price = price

    except Exception as e:
        print(f"Error during request: {e}")

# Publish Prices to MQTT (Timer Callback)


def handle_interrupt(pin):
    global motion
    motion = True


def publish_prices(timer):
    # detect time_start to now that has been 1 hour ago
    global index
    global is_alert
    index += 1
    print(index)
    start_time = time.time()
    mot = 0
    while (time.time() - start_time) < 5:
        if motion:
            mot = 1

    if mot == 0:
        index = 0
        # 1 high 2 low 3 press and high 2 hours
    fetch_and_publish_crypto_prices()
    if index == 12 and is_alert != False:
        topic = f'{TOPIC_PREFIX}/ring'
        mqtt.publish(topic, '2')
        index = 0  # Reset Every time bitcoin is down
    if index == 12 and is_alert == False:
        topic = f'{TOPIC_PREFIX}/ring'
        mqtt.publish(topic, '1')
    if index == 24:
        topic = f'{TOPIC_PREFIX}/ring'
        mqtt.publish(topic, '3')
        index = 0  # Reset Every 2 hours


# Setup and Main Loop
connect_wifi()
mqtt = connect_mqtt()

index = 0
publish_prices(0)

# Set a timer to fetch and publish prices every 5 minutes (300 seconds) 300000
timer = Timer(-1)
timer.init(period=15000, mode=Timer.PERIODIC, callback=publish_prices)
