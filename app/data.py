import threading as th
import json
import os
import time

KEYBOARD_DATA = MOUSE_DATA = SYSTEM_DATA = WINDOW_DATA = None

# return generator with period of time's worth of data
def get_data(period, opt):
    if opt == "kb":
        fname = KEYBOARD_DATA
    elif opt == "mo":
        fname = MOUSE_DATA
    elif opt == "sy":
        fname = SYSTEM_DATA
    else:
        fname = WINDOW_DATA

    while not os.path.exists(fname):
        pass

    with open(fname, "r") as f:
        f.seek(0, 2)
        start_time = time.time()
        end_time = start_time + period
        while time.time() < end_time:
            # ensure contents present
            while not os.path.getsize(fname) > 0:
                pass
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

# https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file

class Data:
    def __init__(self, filenames):
        global KEYBOARD_DATA, MOUSE_DATA, SYSTEM_DATA, WINDOW_DATA
        KEYBOARD_DATA = filenames[0]
        MOUSE_DATA = filenames[1]
        SYSTEM_DATA = filenames[2]
        WINDOW_DATA = filenames[3]

    #
    # processes data to proper json;
    # called by gui.py
    #

    def get_keyboard(self, period):
        for lines in get_data(period, "kb"):
            print("hello world")

    def get_mouse(self, period):
        output = ""
        for lines in get_data(period, "mo"):
            output = (output + lines + "\n")

    def get_system(self, period):
        for lines in get_data(period, "sy"):
            print("hello world")

    def get_window(self, period):
        for lines in get_data(period, "wn"):
            print("hello world")
