import os
import serial
import sys

import constants
from commands import Printer


if __name__ == "__main__":
    draws = os.listdir("draws")
    print("Listado de archivos disponibles:")
    for i, draw in enumerate(draws): 
        print(f"[{i}] {draw}")
    selection = int(input("Seleccionar número de archivo: "))
    filename = draws[selection]

    printer = Printer()
    printer.reset()
    if filename.endswith(".txt"):
        printer.write_print_mode(os.path.join("draws", filename))
    elif filename.endswith(".png"):
        printer.write_bitmap_mode(os.path.join("draws", filename))
    elif filename.endswith(".py"):
        raise NotImplemenetedError("Aún no implementado")
    else:
        print("Archivo no soportado")
    printer.close()
