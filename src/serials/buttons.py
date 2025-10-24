import serial
import time

from src.settings import BUTTONS_SERIAL_PORT, BUTTONS_BAUD_RATE


class Buttons:
    def __init__(self):
        self.buttons = serial.Serial(BUTTONS_SERIAL_PORT, BUTTONS_BAUD_RATE, timeout=0.1)
        self.buttons.setDTR(False)
        self.buttons.setRTS(False)
        time.sleep(0.5)
        self.buttons.reset_input_buffer()

    def read(self):
        if self.buttons.in_waiting > 0:
            data = self.buttons.read()
            print(f"Received: {data}")

    def close(self):
        self.buttons.close()