import argparse

from src.serials.escpos_printer import Printer
from src.modes.directory import DirectoryMode
from src.modes.photo import PhotoMode


if __name__ == "__main__":
    print("Iniciando conexión con la impresora...")
    printer = Printer()
    printer.reset()

    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", type=str, default="archivos")
    parser.add_argument("--evento", type=str, default=None)
    args = parser.parse_args()
    if args.modo == "archivos":
        dm = DirectoryMode(printer, args.evento)
        dm.run()
    elif args.modo == "foto":
        pm = PhotoMode(printer, args.evento)
        pm.run()
    else:
        print("Modo desconocido, elija entre las opciones: archivos, foto, manual ")

    printer.close()
