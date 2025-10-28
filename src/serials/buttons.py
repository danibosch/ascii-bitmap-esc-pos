import serial
import time
import threading

from src.settings import BUTTONS_SERIAL_PORT, BUTTONS_BAUD_RATE


class Buttons(threading.Thread):
    def __init__(self, input_queue):
        super().__init__(daemon=True)
        self._q = input_queue
        self.buttons = serial.Serial(BUTTONS_SERIAL_PORT, BUTTONS_BAUD_RATE, timeout=0.1)
        self.buttons.setDTR(False)
        self.buttons.setRTS(False)
        time.sleep(0.5)
        self.buttons.reset_input_buffer()

    def run(self):
        while True:
            if self.buttons.in_waiting > 0:
                data = self.buttons.read()
                print(f"Received: {data}")
                self._q.put(data.decode("utf-8"))
            time.sleep(0.1)
