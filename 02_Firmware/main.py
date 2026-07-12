import machine
import time
import dht
import ssd1306

# I2C configuration for OLED Screen
i2c = machine.I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# DHT11 Sensor configuration
sensor = dht.DHT11(machine.Pin(15))

# Case Fan configuration on GPIO 14
fan = machine.Pin(14, machine.Pin.OUT)
fan.value(0) # Initialize fan to off

# LED configurations (Red on GPIO 18, Yellow on GPIO 20)
led_red = machine.Pin(18, machine.Pin.OUT)
led_yellow = machine.Pin(20, machine.Pin.OUT)
led_red.value(0)
led_yellow.value(1) # Fan is initially off, so yellow is ON

while True:
    try:
        sensor.measure()
        humidity = sensor.humidity()
        temp_c = sensor.temperature()
        temp_f = (temp_c * 9/5) + 32
        
        # Turn fan ON if temp gets too high (>30C), OFF once it drops to the lower end (<=10C)
            
        if humidity <= 46:
            status = "DRY / PERFECT"
            fan.value(0)
            led_red.value(0)
            led_yellow.value(1)  # Yellow LED ON when fan is off
        elif humidity < 40:
            status = "SAFE / OK"
            fan.value(0)
            led_red.value(0)
            led_yellow.value(1)  # Yellow LED ON when fan is off
        elif humidity > 46:
            status = "WET / ATTN!"
            fan.value(1)
            led_red.value(1)     # Red LED ON when fan is running
            led_yellow.value(0)
            
        oled.fill(0)
        oled.text("INLAND STORAGE", 0, 0)
        oled.text(f"Humidity: {humidity}%", 0, 18)
        oled.text(f"Temp: {temp_f:.1f} F", 0, 34)
        oled.text(status, 0, 52)
        oled.show()
        
    except OSError as e:
        print("Sensor read error, trying again...", e)
        
    time.sleep(2.0)
