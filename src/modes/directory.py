import os
import re
import json

from src.modes.base import BaseMode


class DirectoryMode(BaseMode):
    def run(self):
        while True:
            draws = sorted(os.listdir("draws"))
            print("Listado de archivos disponibles:")
            print("")
            for i, draw in enumerate(draws): 
                print(f"    [{i}] {draw}")
            print("")
            print("    [Q] Salir ")
            selection = input(">> ")

            if selection.lower() == "q":
                break
            if not re.search("^[0-9]+$", selection):
                print("Opción no válida")
                continue
            if int(selection) >= len(draws):
                print("Opción no valida")
                continue

            filename = draws[int(selection)]
            filename_extension = filename.split(".")[-1].lower()

            if filename_extension not in ["json", "txt", "png", "jpg", "jpeg"]:
                print(f"Archivo {filename_extension} no soportado por el momento")
                continue
            print("Imprimiendo...")
            if self.wrapper is not None:
                print("Agregando wrapper...")
                self.wrapper.print_pre(self.printer)
            self._print(filename)
            if self.wrapper is not None:
                self.wrapper.print_post(self.printer)
            
            #printer.full_cut()

    def _print(self, filename):
        if filename.endswith(".txt"):
            self.printer.write_print_mode(os.path.join("draws", filename))
        elif filename.lower().endswith(".png") or filename.lower().endswith(".jpg"):
            self.printer.write_bitmap_mode(os.path.join("draws", filename))
        elif filename.lower().endswith(".json"):
            pipeline = json.loads(os.path.join("draws", filename))