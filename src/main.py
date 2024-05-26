import os
import serial
import sys
import cv2
import numpy as np
import time
from PIL import Image
from datetime import datetime

import constants
from commands import Printer


def manual_mode():
    raise NotImplemenetedError("Aún no implementado")


def directory_mode():
    draws = os.listdir("draws")
    while True:
        print("Listado de archivos disponibles:")
        print(f"")
        for i, draw in enumerate(draws): 
            print(f"    [{i}] {draw}")
        print(f"    [{i+1}] Escribir: ")
        print(f"")
        print(f"    [Q] Volver al menú anterior ")
        selection = input(">> ")

        if selection == str(int(i)+1):
            text = input("Texto: ")
            printer.write_print_mode(text)
        elif selection.lower() == "q":
            break
        else:
            filename = draws[int(selection)]

            if filename.endswith(".txt"):
                with open(os.path.join("draws", filename), "rb") as file:
                    printer.write_print_mode(file)
            elif filename.lower().endswith(".png"):
                printer.write_bitmap_mode(os.path.join("draws", filename))
            elif filename.endswith(".py"):
                raise NotImplemenetedError("Aún no implementado")
            else:
                print("Archivo no soportado")


def selfie_mode():
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

        pressedKey = cv2.waitKey(1)
        if pressedKey in [13, 32]: # Enter, space
            cv2.imshow("webcam", np.zeros(frame.shape))
            print("Imprimir?")
            print("    [S] Sí!")
            print("    [N] No, sacar otra")
            print(">> ")
            image = frame
            d = datetime.now().strftime("%Y%m%d%H%M%S")
            cv2.imwrite(os.path.join("photos", f'foto{d}.png'), image)
            mode = 0
        elif pressedKey == ord("s"):
            print("Imprimiendo...")
            if mode == 0:
                printer.write_bitmap_mode(os.path.join("photos", f'foto{d}.png'))
                printer.partial_cut()
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

if __name__ == "__main__":
    printer = Printer()
    printer.reset()
    while True:
        mode = input(
            "Elegir modo:\n"
            "\n"
            "  [1] Cargar archivos para imprimir\n"
            "  [2] Selfie\n"
            "  [3] Comandos manuales\n"
            "\n"
            "  [Q] Salir\n"
            ">> "
        )
        if mode == "1":
            directory_mode()
        elif mode == "2":
            selfie_mode()
        elif mode == "3":
            manual_mode()
        elif mode.lower() == "q":
            break
        else:
            print("Modo desconocido")


    printer.close()