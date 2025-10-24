import serial
import six
import time
from PIL import Image, ImageOps

import src.constants as constants
from src.settings import PRINTER_SERIAL_PORT, PRINTER_BAUD_RATE, ENCODING


class Printer:
    def __init__(self):
        self.printer = serial.Serial(PRINTER_SERIAL_PORT, PRINTER_BAUD_RATE)

    def reset(self):
        self.printer.write(constants.INIT)

    def partial_cut(self):
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.PARTIAL_CUT)

    def full_cut(self):
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.LF)
        self.printer.write(constants.FULL_CUT)

    def write_text(self, text, line_width_mode="normal"):
        if line_width_mode == "normal":
            width = constants.LINE_WIDTH_NORMAL
        elif line_width_mode == "wide":
            self.printer.write(constants.WIDE_FONT)
            width = constants.LINE_WIDTH_WIDE
        else:
            print("Warning: line_width_mode debe ser 'normal' o 'wide'. Usando 'normal' por defecto.")
            width = constants.LINE_WIDTH_NORMAL

        for chunk in [text[i:i+constants.BUFFER_SIZE] for i in range(0, len(text), constants.BUFFER_SIZE)]:
            self.printer.write(chunk.ljust(width, " ").encode(ENCODING))
        self.printer.write(constants.NORMAL_FONT)
        self.printer.write(constants.LF)

    def write_print_mode(self, filename=None, compressed=True, escaped=False):
        """Escritura en modo texto
        """
        if compressed:
            self.printer.write(constants.LINESPACE_HEADER + six.int2byte(18))
        if filename is None:
            print("ERROR: filename is None")
            return
        with open(filename, "r") as lines:
            if len([x for x in lines if len(x) > constants.LINE_WIDTH_WIDE]) > 0:
                width = constants.LINE_WIDTH_NORMAL
            else:
                self.printer.write(constants.WIDE_FONT)
                width = constants.LINE_WIDTH_WIDE

        with open(filename, "r") as lines:
            for i, line in enumerate(lines):
                if (i+1) % 20 == 0:
                    time.sleep(5)
                len_line = len(line)
                if len_line <= width +1:
                    self.printer.write(line.ljust(len(line) % width, " ").encode(ENCODING))
                else:
                    print(f"Warning: cada línea debe ser tener {width} caracteres o menos. Tiene {len_line} caracteres, cortando...")
                    self.printer.write(line[:width].encode(ENCODING))
    

    def write_bitmap_mode(self, image, convert=True, width_density=False, cut=False):
        """Escritura en modo bitmap
        """
        image = Image.open(image)
        if convert:
            # Convertimos la imagen a escala de grises, luego a blanco y negro
            # e invertimos, ya que para la impresora 1 es negro y 0 es blanco.
            base_width = 200
            wpercent = (base_width / float(image.size[0]))
            hsize = int((float(image.size[1]) * float(wpercent)))
            image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)
            image = image.convert("L")
            image = image.convert("1")
            image = ImageOps.invert(image)

        # Rotamos para leer de a columnas
        image = image.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
        if width_density:
            m = b"\x01"
        else:
            m = b"\x00"

        # El protocolo imprime la imagen por columnas de 8 bits, generamos la matriz
        width, height = image.size
        top, left = 0, 0
        chunks = []
        while left < width:
            remaining = width - left
            box = (left, top, left + 8, top + height)
            column = image.transform((8, height), Image.EXTENT, box)
            pixels = column.tobytes()
            chunks.append(pixels)
            left += 8

        # Alto y ancho están rotados, los usamos al revés aquí
        n1n2 = b''
        for _ in range(0, 2):
            n1n2 += six.int2byte(height % 256)
            height = height // 256

        self.printer.write(constants.LINESPACE_HEADER + six.int2byte(16))
        for i, chunk in enumerate(chunks):
            self.printer.write(constants.BMP_HEADER + m + n1n2 + chunk + b"\n")
        
        self.printer.write(constants.LF)
        self.printer.write(constants.LINEFEED_RESET)

    def close(self):
        self.printer.close()

