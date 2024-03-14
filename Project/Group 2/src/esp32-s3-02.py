from machine import Pin, ADC, I2C, PWM
from ssd1306 import SSD1306_I2C
import time
import mmlparser
import uasyncio as asyncio
import network
from umqtt.simple import MQTTClient
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)


def lens(ls_input):
    try:
        return len(ls_input)
    except:
        return 0


note_ctime = 0
status = 0
position = 0
# ไม่แก้(add)
RED_GPIO = 42
YELLOW_GPIO = 41
GREEN_GPIO = 40
LDR_GPIO = 4
BUTTON_GPIO = 2
OLED_WIDTH = 128
OLED_HEIGHT = 64
I2C_SCL_PIN = 47
I2C_SDA_PIN = 48
GREEN_LED_STATE = 0
YELLOW_LED_STATE = 0
coin_list = ["BTC", "ETH", "BNB", "SOL", "AVAX", "MATIC", "OP", "APT",
             "OKB", "TIA", "ARB", "MNT", "SUI", "SEI", "MANTA", "ZETA", "DYM", "STRK"]  # 17
coin_list_input = {}
coin_receive_count = {}
dfi = 0  # จับเวลาเริ่มกด เเละหลังกด;
mml_str_up = "o5t77V127l16r>c+f+g+a4g+8.f+4.c+f+g+a4b8ab8>c+4<c+f+g+a4g+8.f+4.f+>c+<b8f+>c+l8<beef+16f+1&f+.l16c+f+g+ac+ag+8f+e16f+8<ab>c+8c+c+c+def+e8eeef+g+ag+8c+f+g+ac+ag+8f+ef+8<ab>c+8c+c+c+l8dag+16f+ee16f+.l16c+f+g+a4.a8g+&g+64a.g+8&g+64c+g+ab4.b8a&a64g+.f+8&f+64f+ab>c+8<f+a8b8>c+4c+e8dc+2.&c+>c+<<c+f+g+a4g+8.f+4.c+f+g+a4b8ab8>c+4<c+f+g+a4g+8.f+4.f+>c+<b8f+>c+<b8e8e8f+f+8.c+f+g+a4g+8.f+4.c+f+g+a4b8ab8>c+4<c+f+g+a4g+8.f+4.f+>c+<b8f+>c+l8<beef+16f+.l16f+>c+<b8f+>c+l8<beef+16f+.f+16>c+16<bf+16>c+16<beef+16f+4.,o5l16r4<f+a>c+f+<eg+b>e<f+a>c+f+a4<f+a>c+f+<eg+b>e<c+fg+>c+f4<f+a>c+f+<eg+b>e<f+b>d+f+b4<<b>df+bc+eg+>c+<<f+a>c+f+af+a>c+f+1<f+a>c+f+<eg+b>e<<a>c+ea>c+ea8<df+a>df+a>d8<<c+fg+>c+fg+>c+8<<f+a>c+f+<eg+b>e<<a>c+ea>c+ea8<df+a>d<eg+b>e<f+a>c+f+a4<df+a>df+a>c+8<<eg+b>eg+>de8<<c+eg+>c+eg+>c+8<<f+a>c+f+a>c+f+8o3b>df+b>df+b8<df+a>df+a>d8<c+8.c+8c+8c+c+2<f+a>c+f+<eg+b>e<f+a>c+f+a4<f+a>c+f+<eg+b>e<c+fg+>c+f4<f+a>c+f+<eg+b>e<f+b>d+f+b4<<b>df+bc+eg+>c+<<f+a>c+f+af+a>c+<f+a>c+f+<eg+b>e<f+a>c+f+a4<f+a>c+f+<eg+b>e<c+fg+>c+f4<f+a>c+f+<eg+b>e<f+b>d+f+b4<<b>df+bc+eg+>c+<<f+a>c+f+af+a>c+<<b>df+bc+eg+>c+<<f+a>c+f+af+a>c+<df+a>d<eg+b>e8f+f+4."
mml_str_down = "v127t110<e8>d8e8e8<e8>d8e8e8<e8>d8e8e8d8e8f+8f+8e8d8<b8a8b4b8>d8e8d8<b8a8>d8<b16b16a8g8e4a8g8a8b8a8g8e4e4"
mml_str_press = "t155>f+8f+8d8<b4b4>e4e4e8g+8g+8a8b8a8a8a8e4d4f+4f+4f+8e8e8f+8e8f+8f+8d8<b4b4>e4e4e8g+8g+8a8b8a8a8a8e4d4f+4f+4f+8e8e8f+8e4,t155>d2.&d8d1&d8e2.&e8c+2&c+8<a2>d2.&d8d1&d8e2.&e8c+2&c+8<a2"
len_coin_list = len(coin_list)
coin_value = 0
coin_value_input = 0
TOPIC_LIGHT = f'{TOPIC_PREFIX}/light'
TOPIC_DISPLAY_TEXT = f'{TOPIC_PREFIX}/display/text'
TOPIC_SWITCH = f'{TOPIC_PREFIX}/switch'
TOPIC_CRYPTO = f'{TOPIC_PREFIX}/price'
TOPIC_TIME2PRESS = f'{TOPIC_PREFIX}/Time2press'
TOPIC_RING = f'{TOPIC_PREFIX}/ring'
TOPIC_COIN = f'{TOPIC_PREFIX}/coin'
coinindex = 0
start_time_run = 0


async def play_music(mml_str, max_duration=15000):
    print("PLAY")
    time_start = time.ticks_ms()
    music_task = asyncio.create_task(
        parser.aplay(mml_str))  # Play music asynchronously
    print("PLAYED")
    while time.ticks_ms() < time_start + max_duration:
        await asyncio.sleep(0)  # Allow other tasks to run
        if music_task.done():
            # Music playback completed before the timeout, exit the loop
            break
    print("Timeout reached, stopping music")
    if not music_task.done():
        # Music playback hasn't completed yet, cancel the task
        music_task.cancel()
    for pwm in pwm_pins:
        pwm.duty_u16(0)


def pwm_callback(channel, action, note, velocity):
    pwm = pwm_pins[channel]
    if action == "on":
        # Calculate frequency from note number
        frequency = 2 ** ((note - 69) / 12) * 440
        pwm.freq(int(frequency))
        pwm.duty_u16(32768)  # 50% duty cycle
    elif action == "off":
        pwm.duty_u16(0)  # Turn off


# Initialize the MMLParser
pwm_pins = [PWM(Pin(18), duty=0)]
parser = mmlparser.MMLParser(len(pwm_pins), pwm_callback)

# Initialize the OLED display
i2c = I2C(-1, Pin(I2C_SCL_PIN), Pin(I2C_SDA_PIN))
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

oled.fill(0)  # Clear the display
oled.text(f'CRYPTO: {coin_list[coinindex]}', 0, 0)
oled.text(f'PRICE: 0.00', 0, 20)
oled.text(f'DIFF: 0.00 $', 0, 40)
oled.text(f'      0.00 %', 0, 50)
oled.show()
stat = 0

stop_sound_press = False


def soundAndPress(status):
    global stat
    global stop_sound_press

    stat = status

    if stat == 1:
        sound_up_con()
    if stat == 2:
        sound_down_con()
    if stat == 0:
        if stop_sound_press == False:
            stop_sound_press = True

        send_Data(time.ticks_ms() - start_time_run)

# ไม่แก้


def connect_wifi():
    mac = ':'.join(f'{b:02X}' for b in wifi.config('mac'))
    print(f'WiFi MAC address is {mac}')
    wifi.active(True)
    print(f'Connecting to WiFi {WIFI_SSID}.')
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        print('.', end='')
        time.sleep(0.5)
    print('\nWiFi connected.')


# ไม่แก้
def connect_mqtt():
    print(f'Connecting to MQTT broker at {MQTT_BROKER}.')
    mqtt.connect()
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(TOPIC_SWITCH)
    mqtt.subscribe(TOPIC_DISPLAY_TEXT)
    mqtt.subscribe(TOPIC_CRYPTO)
    mqtt.subscribe(TOPIC_TIME2PRESS)
    mqtt.subscribe(TOPIC_RING)
    print('MQTT broker connected.')


sound_up = 0
sound_down = 0
al_time = 0


def sound():
    sound_up = 1
    al_time = time.ticks_ms()


def price_cal():

    price_cal_list = coin_list_input.get(coin_list[coinindex])

    if price_cal_list == None:
        price_cal_list = [0, 0]

    price_diff = price_cal_list[1] - price_cal_list[0]

    if price_cal_list[0] == 0:
        price_diff_change = 0
    else:
        price_diff_change = (price_diff/price_cal_list[0])*100

    price_symbol = ""
    text_price_diff = ""

    if price_diff == 0:
        yellow.value(1)
        red.value(0)
        green.value(0)
        text_price_diff = "0.00 $"
        price_symbol = ""

    elif price_diff < 0:
        yellow.value(0)
        red.value(1)
        green.value(0)
        price_symbol = "-"
        text_price_diff = f'{abs(price_diff):.2f} $'
    elif price_diff > 0:
        yellow.value(0)
        red.value(0)
        green.value(1)
        price_symbol = "+"
        text_price_diff = f'{price_diff:.2f} $'

    oled.fill(0)  # Clear the display
    oled.text(f'CRYPTO: {coin_list[coinindex]}', 0, 0)
    oled.text(f'PRICE: {price_cal_list[1]:.2f}', 0, 20)
    oled.text(f'DIFF: {price_symbol}{text_price_diff}', 0, 40)
    oled.text(f'      {price_symbol}{abs(price_diff_change):.2f} %', 0, 50)
    oled.show()


def mqtt_callback(topic, payload):
    global coin_value

    if topic.decode() == f'{TOPIC_PREFIX}/price':
        try:
            coin_value_input = payload.decode("utf-8")
            coin2list = coin_value_input.split(",")

            if coin_list_input.get(coin2list[0]) == None:
                coin_list_input[coin2list[0]] = [
                    float(coin2list[1]), float(coin2list[1])]

                coin_receive_count[coin2list[0]] = 1

            elif coin_receive_count[coin2list[0]] == 13:
                coin_list_input[coin2list[0]] = [
                    float(coin2list[1]), float(coin2list[1])]

                coin_receive_count[coin2list[0]] = 1

                sound()
            else:
                coin_list_input[coin2list[0]] = [
                    coin_list_input[coin2list[0]][0], float(coin2list[1])]
                coin_receive_count[coin2list[0]] += 1

            if coin_list[coinindex] == coin2list[0]:
                price_cal()

        except ValueError:
            pass

    if topic.decode() == f'{TOPIC_PREFIX}/ring':
        try:
            ring_input = int(payload.decode("utf-8"))
            soundAndPress(ring_input)

        except ValueError:
            pass


def press():
    global position
    position += 1
    position = position % len_coin_list


def hold():
    global sound_up, souund_down
    sound_up = 0
    sound_down = 0


freqIndex = 0


def sound_up_con():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(play_music(mml_str_up))


def sound_down_con():
    # Adjust as needed
    loop = asyncio.get_event_loop()
    loop.run_until_complete(play_music(mml_str_down))

# Set initial frequency (in Hz)


# Function to change the frequency
def change_frequency(new_frequency):
    speaker_pwm.freq(new_frequency)


############
# setup
############
red = Pin(RED_GPIO, Pin.OUT)
green = Pin(GREEN_GPIO, Pin.OUT)
yellow = Pin(YELLOW_GPIO, Pin.OUT)
ldr = ADC(Pin(LDR_GPIO), atten=ADC.ATTN_11DB)
button_pin = Pin(BUTTON_GPIO, Pin.IN, Pin.PULL_UP)
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
connect_wifi()
connect_mqtt()
start_time = 0
is_hold = False
is_press = False
data_ls_ja = []

# ส่งค่าไปยัง website Dashboard


def send_Data(number_ja):
    data_ls_ja.append(number_ja)
    mqtt.publish(f'{TOPIC_PREFIX}/Time2press', f'{data_ls_ja}')
    print("send :" + f"{data_ls_ja}")


n2music = None


async def n_2press(stopped=False):
    global n2music

    if n2music != None:
        if stopped == True:

            n2music.cancel()
            n2music = None
        elif stopped == False and n2music.done():

            n2music.cancel()
            n2music = None
            n2music = asyncio.create_task(parser.aplay(mml_str_press))
    elif n2music == None:

        n2music = asyncio.create_task(parser.aplay(mml_str_press))

############
# loop
############
initial_frequency = 69

while True:
    mqtt.check_msg()
    button_state = button_pin.value()

    if button_state == 0:  #
        if start_time == 0:
            start_time = time.ticks_ms()
            is_hold = False
            is_press = False
    else:
        if start_time != 0:

            if time.ticks_diff(time.ticks_ms(), start_time) >= 1200:

                is_hold = True
                soundAndPress(0)
            else:

                is_press = True
                if coinindex < 17:
                    coinindex += 1
                else:
                    coinindex = 0
                price_cal()
                mqtt.publish(f'{TOPIC_PREFIX}/coin', coin_list[coinindex])
                if al_time != 0:
                    time2p = time.ticks_ms() - al_time
                    time2press_list.append(time2p)
            start_time = 0

    if stat == 3:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(n_2press(stop_sound_press))

        if stop_sound_press == True:
            stop_sound_press = False

    if is_press:
        press()
    if is_hold:
        start_time_run = time.ticks_ms()

        hold()
