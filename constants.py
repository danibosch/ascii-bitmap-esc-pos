# =======================
#  Printer constants
# =======================

BUFFER_SIZE = 40

# =======================
#  ASCII codes
# =======================

HT = b"\x09"
LF = b"\x0A"
CR = b"\x0D"

ESC = b"\x1B"

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