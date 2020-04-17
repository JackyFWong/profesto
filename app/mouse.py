from Xlib import display
import threading as th
import os

OUT_FILE = "mo_out.txt"

class Mouse:
    def __init__(self, erase):
        if (erase == 'y'):
            open(OUT_FILE, "w").close()
        self.mouse_loc = 0

    def data_stream(self):
        print("Thread {} online",format(th.current_thread().name))
        print("---PID {}",format(os.getpid()))
        while True:
            self.mouse_loc = display.Display().screen().root.query_pointer()._data
            x = self.mouse_loc["root_x"]
            y = self.mouse_loc["root_y"]
            out_str = f"{x} {y}\n"
            with open(OUT_FILE, "a") as f:
                f.write(out_str)
