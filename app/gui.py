import data
import threading as th
import os

kb = "kb_out.log"
mo = "mo_out.log"
sy = "sys_out.log"
wn = "wn_out.log"

class Gui:
    def __init__(self):
        self.input = data.Data((kb, mo, sy, wn))

    def test(self):
        print(f"Thread {th.current_thread().name} online")
        print(f"---PID {os.getpid()}")
        print(self.input.get_mouse(10))
