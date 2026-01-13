from rgb_led import RGBLed
import time

led = RGBLed()

led.set("GREEN", brightness=0.2)
time.sleep(2)
led.breathe("RED", max_brightness=0.5)
time.sleep(3)

led.shutdown()