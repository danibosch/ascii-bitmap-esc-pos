# =======================
#  Printer constants
# =======================

BUFFER_SIZE = 40
LINE_WIDTH_NORMAL = 40
LINE_WIDTH_WIDE = 34

# =======================
#  ASCII codes
# =======================

HT = b"\x09" # Horizontal tab
LF = b"\x0A" # Line feed
CR = b"\x0D" # Carriage return

ESC = b"\x1B" # Escape

# =======================
#  Special commands
# =======================

INIT =        ESC + b'@'
PARTIAL_CUT = ESC + b"m"
FULL_CUT =    ESC + b"i"

BLACK = ESC + b"r" + b"1"
RED =   ESC + b"r" + b"1"

LINEFEED_RESET = ESC + b"2"

# =======================
#  Print mode
# =======================

# Ref n:       u|x|w|h|x|x|x|f
#  underline:  1 0 0 0 0 0 0 0 --> \x80
#  normal:     0 0 0 0 0 0 0 1 --> \x01 default
#  wide font:  0 0 0 0 0 0 0 1 --> \x00
WIDE_FONT =      ESC + b"!" + b"\x00"
NORMAL_FONT =    ESC + b"!" + b"\x01"
UNDERLINE_FONT = ESC + b"!" + b"\x80"
DOUBLEWH_FONT =  ESC + b"!" + b"\x30"

LINESPACE_HEADER = ESC + b"3"

# =======================
#  Bitmap mode
# =======================

BMP_HEADER = ESC + b"*"

# =======================
#  Terminal
# =======================

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'