import serial
import six
from PIL import Image, ImageOps

import constants
from settings import SERIAL_PORT, BAUD_RATE, ENCODING


class Printer:
    def __init__(self):
        self.printer = serial.Serial(SERIAL_PORT, BAUD_RATE)

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
        self.printer.write(constants.FULL_CUT)


    def write_print_mode(self, message, wide=True):
        """Escritura en modo texto
        """
        if wide:
            self.printer.write(constants.WIDE_FONT)
        if len(message) % constants.BUFFER_SIZE < constants.BUFFER_SIZE:
            message = message.ljust(constants.BUFFER_SIZE - len(message) % constants.BUFFER_SIZE, " ")
        self.printer.write(message.encode(ENCODING))

    def write_bitmap_mode(self, image, convert=True, width_density=False, cut=False):
        """Escritura en modo bitmap
        """
        image = Image.open(image)
        if convert:
            # Convertimos la imagen a escala de grises, luego a blanco y negro
            # e invertimos, ya que para la impresora 1 es negro y 0 es blanco.
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
        n1n2 = b'';
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

