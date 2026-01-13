from fastapi import FastAPI
from pydantic import BaseModel
from collections import deque
import threading
import time
import atexit

from device_manager import DeviceManager

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse






# ---------- CONFIG ----------
SAMPLE_HZ = 10
HISTORY_SECONDS = 60 * 10   # 10 minutes
MAX_POINTS = SAMPLE_HZ * HISTORY_SECONDS

# ---------- APP ----------
app = FastAPI()
manager = DeviceManager()

state_history = deque(maxlen=MAX_POINTS)
lock = threading.Lock()


# ---------- BACKGROUND SAMPLER ----------
def sampler_loop():
    interval = 1.0 / SAMPLE_HZ
    while True:
        start = time.time()

        state = manager.get_state()

        with lock:
            state_history.append(state)

        elapsed = time.time() - start
        if elapsed < interval:
            time.sleep(interval - elapsed)


threading.Thread(target=sampler_loop, daemon=True).start()


# ---------- MODELS ----------
class LedSetReq(BaseModel):
    name: str = "OFF"
    brightness: float = 1.0


class LedBreatheReq(BaseModel):
    name: str = "BLUE"
    brightness: float = 0.5
    speed: float = 0.1



app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

# ---------- API ----------

@app.get("/state")
def state():
    return manager.get_state()


@app.get("/history")
def history():
    with lock:
        return list(state_history)


# ---------- RELAY ----------
@app.post("/relay/on")
def relay_on():
    manager.relay_on()
    return {"relay": True}


@app.post("/relay/off")
def relay_off():
    manager.relay_off()
    return {"relay": False}


@app.post("/relay/toggle")
def relay_toggle():
    manager.relay_toggle()
    manager.led_set("GREEN" if manager.relay.get_state() else "RED")
    return {"relay": manager.relay.get_state()}


# ---------- LED ----------
@app.post("/led/set")
def led_set(req: LedSetReq):
    manager.led_set(req.name, req.brightness)
    return {"ok": True}


@app.post("/led/breathe")
def led_breathe(req: LedBreatheReq):
    manager.led_breathe(req.name, req.brightness, req.speed)
    return {"ok": True}


@app.post("/led/off")
def led_off():
    manager.led_off()
    return {"ok": True}


# ---------- CLEANUP ----------
@atexit.register
def shutdown():
    manager.cleanup()


# ---------- RUN ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        reload=False
    )
