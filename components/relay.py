from gpiozero import DigitalOutputDevice
import atexit


class Relay:
    def __init__(self, pin=24, active_high=True):
        self._relay = DigitalOutputDevice(
            pin,
            active_high=active_high,
            initial_value=False
        )
        self.state = False
        atexit.register(self.off)

    # ---------- CORE ----------
    def on(self):
        self._relay.on()
        self.state = True

    def off(self):
        self._relay.off()
        self.state = False

    def toggle(self):
        if self.state:
            self.off()
        else:
            self.on()

    def get_state(self):
        return self.state

    # ---------- CLEANUP ----------
    def cleanup(self):
        self.off()
