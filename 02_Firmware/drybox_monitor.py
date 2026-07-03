import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_dht

# Setup I2C communications for the OLED screen (Pins: SDA/SCL)
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Setup the DHT22 Temperature/Humidity Sensor
dhtDevice = adafruit_dht.DHT22(board.D4)

#clear OLED memory
oled.fill(0)
oled.show()

# blank canvas dispaly for drawing elements
mage = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
print("Drybox monitor script running in VS Code. Press Ctrl+C in the terminal to exit.")

while True:
    try:
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        temperature_f = (temperature_c * 9/5) + 32
        if humidity < 20:
            status = "STATUS: DRY/PERFECT"
        elif humidity < 35:
            status = "STATUS: SAFE/OK"
        else:
            status = "STATUS: WET/ATTN!"
    
        draw.rectangle((0, 0, oled.width, oled.height), fill=0)
        draw.text((0, 0),  "INLAND STORAGE", font=font, fill=255)
        draw.text((0, 18), f"Humidity: {humidity:.1f}%", font=font, fill=255)
        draw.text((0, 32), f"Temp: {temperature_f:.1f} F", font=font, fill=255)
        draw.text((0, 50), status, font=font, fill=255)
    oled.image(image)
    oled.show()
    except RuntimeError as error:
        print(f"Sensor communication lag: {error.args[0]}")
        time.sleep(2.0)
        continue
        
    except Exception as e:
        dht_sensor.exit()
        raise e
    time.sleep(2.0)