import machine
import time
import dht
import ssd1306

# Setup I2C communications for the OLED screen (Pins: SDA/SCL)
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# Setup the DHT22 Temperature/Humidity Sensor
sensor = dht.DHT11(machine.Pin(15))
print("Pico Drybox Monitor Active. Press Ctrl+C in your IDE to stop.")

while True:
    try:
        # Trigger sensor reading
        sensor.measure()
        humidity = sensor.humidity()
        temp_c = sensor.temperature()
        
        # Convert Celsius to Fahrenheit
        temp_f = (temp_c * 9/5) + 32
        
        # Determine environmental safety status
        if humidity < 20:
            status = "DRY / PERFECT"
        elif humidity < 35:
            status = "SAFE / OK"
        else:
            status = "WET / ATTN!"
            
        # Clear the OLED screen buffer
        oled.fill(0)
        
        # Write text to the display buffer (X, Y coordinates)
        oled.text("INLAND STORAGE", 0, 0)
        oled.text(f"Humidity: {humidity}%", 0, 18)
        oled.text(f"Temp: {temp_f:.1f} F", 0, 34)
        oled.text(status, 0, 52)
        
        # Push buffer changes live to the physical screen
        oled.show()
        
    except OSError as e:
        print("Sensor read error, trying again...", e)
        
    # Polling interval pause
    time.sleep(2.0)