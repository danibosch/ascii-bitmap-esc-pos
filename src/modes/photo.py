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
        self._print_take_photo()

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
            if pressedKey in [13, "T", "t"]: # Enter, T
                cv2.imshow("webcam", np.zeros(frame.shape))
                self._print_print()
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
                self._print_take_photo()
            elif pressedKey in [ord("n"), "N", "n"]:
                print("Cancelando...")
                self._print_take_photo()
                mode = 1
            elif pressedKey in [ord("q"), "Q", "q"]:
                break

            if mode == 1:
                cv2.imshow("webcam", frame)
            else:
                cv2.imshow("webcam", image)

        stream.release()
        cv2.destroyAllWindows()

    def _print_print(self):
        self._print_title()
        print("                                   |WW|           ")
        print("                                  _|  |_          ")
        print("      ┌──────────────────────────( |__| )─────┐")
        print("      │                         /________\\    │")
        print("      │                        |       o  |   │")
        print("      │    ¿Imprimir?          |__________|   │")
        print("      │                                       │")
        print("      │                  Sacar                │")
        print("      │    ¡Si!          otra                 │")
        print(f"      │   {Colors.YELLOW}.·'''·.{Colors.RESET}      _.-'-._      {Colors.GREEN}.·'''·.{Colors.RESET}   │")
        print(f"      └──{Colors.YELLOW}|·.___.·|{Colors.RESET}────|-._ _.-|────{Colors.GREEN}|·.___.·|{Colors.RESET}──┘")
        print(f"          {Colors.YELLOW}Amarillo{Colors.RESET}        '          {Colors.GREEN}Verde{Colors.RESET}")

    def _print_take_photo(self):
        self._print_title()
        print("                                  _____\\'/_  ")
        print("      ┌──────────────────────────|__/-\\[]|────┐")
        print("      │                          |  (_)  |    │")
        print("      │     Tomar una foto       |_______|    │")
        print("      │                                       │")
        print("      │                              ¡Sí!     │")
        print(f"      │   {Colors.YELLOW}.·'''·.{Colors.RESET}      _.-'-._      {Colors.GREEN}.·'''·.{Colors.RESET}   │")
        print(f"      └──{Colors.YELLOW}|·.___.·|{Colors.RESET}────|-._ _.-|────{Colors.GREEN}|·.___.·|{Colors.RESET}──┘")
        print(f"          {Colors.YELLOW}Amarillo{Colors.RESET}        '          {Colors.GREEN}Verde{Colors.RESET}")

    def _print_title(self):
        print("\033[H\033[2J") # Clear screen
        print("")
        print("   _____ _ _               _             _   _ ")
        print("  |_   _|_| |_ ___ ___ ___| |___ ___ ___|_|_| |")
        print("    | | | | '_| -_| . | . | | .'|  _| . | | . |")
        print("    |_| |_|_,_|___|  _|___|_|__,|_| |___|_|___|")
        print("                  |_|                          ")
        print(f"                                  TG: {Colors.CYAN}@danipupy{Colors.RESET}")
        print("")