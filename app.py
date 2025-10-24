import argparse

from src.serials.escpos_printer import Printer
from src.modes.directory import DirectoryMode
from src.modes.photo import PhotoMode
from src.wrappers.base import __all__ as wrappers


if __name__ == "__main__":
    print("Iniciando conexión con la impresora...")

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        "--modo", type=str, default="archivos",
        choices=["archivos", "foto"],
        help="""
            Modo de impresión:
            - archivos: Imprime los archivos desde un directorio
            - foto: Toma una foto con la webcam y la imprime
        """,
    )
    parser.add_argument(
        "--evento", type=str, default=None,
        choices=wrappers,
        help="""
            Para eventos, imprime al inicio y al final de la 
            impresión imágenes o textos personalizados
        """,
    )
    args = parser.parse_args()
    
    if args.help:
        parser.print_help()
        raise SystemExit(0)
    
    printer = Printer()
    printer.reset()

    if args.modo == "archivos":
        dm = DirectoryMode(printer, args.evento)
        dm.run()
    elif args.modo == "foto":
        pm = PhotoMode(printer, args.evento)
        pm.run()
    else:
        print("Modo desconocido, elija entre las opciones: archivos, foto")

    printer.close()
