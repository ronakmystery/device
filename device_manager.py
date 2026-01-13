import atexit
from components.rgb_led import RGBLed
from components.relay import Relay


class DeviceManager:
    def __init__(self):
        # ---------- OUTPUT DEVICES ----------
        self.status_led = RGBLed(
            red=22,
            green=27,
            blue=17
        )

        self.relay = Relay(
            pin=24,
            active_high=True
        )

        atexit.register(self.cleanup)

    # ---------- STATE ----------
    def get_state(self):
        return {
            "relay": self.relay.get_state(),
        }

    # ---------- LED CONTROL ----------
    def led_set(self, name, brightness=1.0):
        self.status_led.set(name, brightness)

    def led_breathe(self, name, brightness=0.5, speed=0.1):
        self.status_led.breathe(name, brightness, speed)

    def led_rotate(self, brightness=0.4, speed=0.05):
        self.status_led.rotate(brightness, speed)

    def led_off(self):
        self.status_led.off()

    # ---------- RELAY CONTROL ----------
    def relay_on(self):
        self.relay.on()

    def relay_off(self):
        self.relay.off()

    def relay_toggle(self):
        self.relay.toggle()

    # ---------- CLEANUP ----------
    def cleanup(self):
        try:
            self.status_led.shutdown()
        except Exception:
            pass

        try:
            self.relay.cleanup()
        except Exception:
            pass
