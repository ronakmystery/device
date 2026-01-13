from gpiozero import RGBLED
import time
import math
import threading
import atexit


class RGBLed:
    COLORS = {
        "RED":     (1, 0, 0),
        "GREEN":   (0, 1, 0),
        "BLUE":    (0, 0, 1),
        "YELLOW":  (1, 1, 0),
        "MAGENTA": (1, 0, 1),
        "CYAN":    (0, 1, 1),
        "WHITE":   (1, 1, 1),
        "OFF":     (0, 0, 0),
    }

    def __init__(self, red=22, green=27, blue=17, active_high=True):
        self.led = RGBLED(
            red=red,
            green=green,
            blue=blue,
            active_high=active_high
        )

        self._stop_event = threading.Event()
        self._thread = None

        atexit.register(self.shutdown)

    # ---------- INTERNAL ----------
    def _apply(self, name, brightness):
        r, g, b = self.COLORS.get(name.upper(), (0, 0, 0))
        brightness = max(0.0, min(brightness, 1.0))
        self.led.color = (
            r * brightness,
            g * brightness,
            b * brightness
        )

    # ---------- PUBLIC API ----------
    def set(self, name, brightness=1.0):
        self.stop_breathing()
        self._apply(name, brightness)

    def off(self):
        self.set("OFF")

    # ---------- BREATHING ----------
    def breathe(self, name, max_brightness=1.0, speed=0.1):
        self.stop_breathing()
        self._stop_event.clear()

        r, g, b = self.COLORS.get(name.upper(), (0, 0, 0))

        def loop():
            t = 0.0
            while not self._stop_event.is_set():
                br = max_brightness * (0.5 + 0.5 * math.sin(t))
                self.led.color = (
                    r * br,
                    g * br,
                    b * br
                )
                t += speed
                time.sleep(0.02)

        self._thread = threading.Thread(target=loop)
        self._thread.start()

    def stop_breathing(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            self._thread = None

            

    # ---------- CLEAN SHUTDOWN ----------
    def shutdown(self):
        self.stop_breathing()
        try:
            self.led.off()
        except Exception:
            pass
