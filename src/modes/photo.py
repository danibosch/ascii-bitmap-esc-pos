import cv2
import os
import numpy as np

from datetime import datetime

from src.modes.base import BaseMode
from src.constants import Colors


class PhotoMode(BaseMode):
    def run(self):
        stream = cv2.VideoCapture(0)
        stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        stream.set(cv2.CAP_PROP_EXPOSURE, 250) 
        stream.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
        stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
        ret, frame = stream.read()
        mode = 1
        print("[Enter o Space o T] Tomar una foto")

        while True:
            ret, frame = stream.read()
            frame = cv2.resize(frame, (200, 130))
            if not ret:
                print("no more stream")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #pressedKey = cv2.waitKey(1)
            pressedKey = self._q.get()
            print(f"Pressed key: {pressedKey}")
            if pressedKey in [13, 32, "T", "t"]: # Enter, space, T
                cv2.imshow("webcam", np.zeros(frame.shape))
                print("Imprimir?")
                print(f"    [{Colors.GREEN}S{Colors.RESET}] Sí!")
                print(f"    [{Colors.RED}N{Colors.RESET}] No, sacar otra")
                print(">> ")
                image = frame
                d = datetime.now().strftime("%Y%m%d%H%M%S")
                cv2.imwrite(os.path.join("src", "photos", f'foto{d}.png'), image)
                mode = 0
            elif pressedKey in [ord("s"), "S", "s"]:
                print("Imprimiendo...")
                if mode == 0:
                    if self.wrapper is not None:
                        print("Agregando wrapper...")
                        self.wrapper.print_pre(self.printer)
                    self.printer.write_bitmap_mode(os.path.join("src", "photos", f'foto{d}.png'))
                    if self.wrapper is not None:
                        self.wrapper.print_post(self.printer)
                    self.printer.partial_cut()
                    mode = 1
                print("[Enter o Space] Tomar una foto")
            elif pressedKey in [ord("n"), "N", "n"]:
                print("[Enter o Space] Tomar una foto")
                mode = 1
            elif pressedKey in [ord("q"), "Q", "q"]:
                break

            if mode == 1:
                cv2.imshow("webcam", frame)
            else:
                cv2.imshow("webcam", image)

        stream.release()
        cv2.destroyAllWindows()