import sys


if sys.platform.startswith('win32'):
    CLEAR = "cls"
elif sys.platform.startswith('win64'):
    CLEAR = "cls"
elif sys.platform.startswith('cygwin'):
    CLEAR = "clear"
elif sys.platform.startswith('linux'):
    CLEAR = "clear"
elif sys.platform.startswith('darwin'):
    CLEAR = "clear"
else:
    CLEAR = ""