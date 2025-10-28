import cv2
import os
import numpy as np

from datetime import datetime

from src.modes.base import BaseMode


class PhotoMode(BaseMode):
    def run(self):
        stream = cv2.VideoCapture(0)
        stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        stream.set(cv2.CAP_PROP_EXPOSURE, 250) 
        stream.set(cv2.CAP_PROP_FRAME_WIDTH, 250)
        stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
        ret, frame = stream.read()
        mode = 1
        print("[Enter o Space] Tomar una foto")

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
            if pressedKey in [13, 32, "2"]: # Enter, space
                cv2.imshow("webcam", np.zeros(frame.shape))
                print("Imprimir?")
                print("    [S] Sí!")
                print("    [N] No, sacar otra")
                print(">> ")
                image = frame
                d = datetime.now().strftime("%Y%m%d%H%M%S")
                cv2.imwrite(os.path.join("src", "photos", f'foto{d}.png'), image)
                mode = 0
            elif pressedKey in ["s", "4"]:
                print("Imprimiendo...")
                if mode == 0:
                    self.printer.write_bitmap_mode(os.path.join("src", "photos", f'foto{d}.png'))
                    self.printer.partial_cut()
                    mode = 1
                print("[Enter o Space] Tomar una foto")
            elif pressedKey == ord("n"):
                print("[Enter o Space] Tomar una foto")
                mode = 1
            elif pressedKey == ord("q"):
                break

            if mode == 1:
                cv2.imshow("webcam", frame)
            else:
                cv2.imshow("webcam", image)

        stream.release()
        cv2.destroyAllWindows()