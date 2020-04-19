from Xlib import display
import threading as th
import os
import math

OUT_FILE = "mo_out.log"

def calc_dist(x, y):
    return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

# https://stackoverflow.com/questions/21850145/monitor-mouse-coordinates-in-real-time-in-linux
class Mouse:
    def __init__(self, erase):
        if (erase == 'y'):
            open(OUT_FILE, "w+").close()
        self.mouse_loc = 0

    def data_stream(self):
        print(f"Thread {th.current_thread().name} online")
        print(f"---PID {os.getpid()}")
        while True:
            self.mouse_loc = display.Display().screen().root.query_pointer()._data
            x = self.mouse_loc["root_x"]
            y = self.mouse_loc["root_y"]
            out_str = f"{x} {y}\n"
            with open(OUT_FILE, "a") as f:
                f.write(out_str)
