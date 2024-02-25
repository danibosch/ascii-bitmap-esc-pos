import os
import serial
import sys

import constants
from PIL import Image
from commands import Printer


if __name__ == "__main__":
    draws = os.listdir("draws")
    print("Listado de archivos disponibles:")
    for i, draw in enumerate(draws): 
        print(f"[{i}] {draw}")
    print(f"[{i+1}] Escribir: ")
    selection = int(input("Seleccionar número de archivo: "))
    printer = Printer()
    printer.reset()
    if selection == i+1:
        text = input("Texto: ")
        printer.write_print_mode(text)
    else:
        filename = draws[selection]

        if filename.endswith(".txt"):
            with open(os.path.join("draws", filename), "rb") as file:
                printer.write_print_mode(file)
        elif filename.endswith(".png"):
            image = Image.open(os.path.join("draws", filename))
            printer.write_bitmap_mode(image)
        elif filename.endswith(".py"):
            raise NotImplemenetedError("Aún no implementado")
        else:
            print("Archivo no soportado")
        printer.close()
