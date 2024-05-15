import queue
import threading

from evreka.db import add_location_to_device

db_queue = queue.Queue()


def worker():
    while True:
        device_id, location = db_queue.get()
        add_location_to_device(device_id, location.lat, location.long, location.timestamp)


threading.Thread(target=worker, daemon=True).start()
