import machine
import time
import dht
import ssd1306

# I2C configuration for OLED Screen
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# DHT11 Sensor configuration
sensor = dht.DHT11(machine.Pin(15))

# Case Fan configuration on GPIO 11
fan = machine.Pin(11, machine.Pin.OUT)
fan.value(0) # Initialize fan to off

while True:
    try:
        sensor.measure()
        humidity = sensor.humidity()
        temp_c = sensor.temperature()
        temp_f = (temp_c * 9/5) + 32
        
        # Turn fan ON if humidity gets too high (>20%), OFF once it drops (<=15%)
        if humidity > 20:
            fan.value(1)
        elif humidity <= 15:
            fan.value(0)
            
        if humidity < 20:
            status = "DRY / PERFECT"
        elif humidity < 35:
            status = "SAFE / OK"
        else:
            status = "WET / ATTN!"
            
        oled.fill(0)
        oled.text("INLAND STORAGE", 0, 0)
        oled.text(f"Humidity: {humidity}%", 0, 18)
        oled.text(f"Temp: {temp_f:.1f} F", 0, 34)
        oled.text(status, 0, 52)
        oled.show()
        
    except OSError as e:
        print("Sensor read error, trying again...", e)
        
    time.sleep(2.0)
