import argparse

from queue import Queue

from src.serials.escpos_printer import Printer
from src.serials.buttons import Buttons
from src.serials.keyboard import Keyboard
from src.modes.directory import DirectoryMode
from src.modes.photo import PhotoMode
from src.wrappers.base import __all__ as wrappers


if __name__ == "__main__":
    print("***************************************")
    print("*       |WW|                          *")
    print("*      _|  |_       Tickepolaroid     *")
    print("*     ( |__| )                        *")
    print("*    /________\   Imágenes impresas   *")
    print("*   |       o  |      en 1-bit        *")
    print("*   |__________|    por @danipupy     *")
    print("*                                     *")
    print("***************************************")

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

    input_queue = Queue()

    printer = Printer()
    printer.reset()
    buttons = Buttons(input_queue)
    keyboard = Keyboard(input_queue)
    buttons.start()
    keyboard.start()

    try:
        if args.modo == "archivos":
            dm = DirectoryMode(printer, args.evento, input_queue)
            dm.run()
        elif args.modo == "foto":
            pm = PhotoMode(printer, args.evento, input_queue)
            pm.run()
        else:
            print("Modo desconocido, elija entre las opciones: archivos, foto")
    except KeyboardInterrupt:
        print("Interrupción del usuario")
    finally:
        print("Finalizando conexión con la impresora...")
        printer.close()
        print("Finalizando conexión con la botonera...")
        buttons.join(timeout=1)
        print("Finalizando conexión con el teclado...")
        keyboard.join(timeout=1)
