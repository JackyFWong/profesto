import threading as th
import os
import concurrent.futures as cf

import data

kb = "kb_out.log"
mo = "mo_out.log"
sy = "sys_out.log"
wn = "wn_out.log"

class Gui:
    def __init__(self):
        self.input = data.Data((kb, mo, sy, wn))

    def test(self):
        try:
            with cf.ThreadPoolExecutor() as gui_exe:
                gui_th0 = gui_exe.submit(self.input.get_mouse, 10)
                gui_th1 = gui_exe.submit(self.input.get_keyboard, 10)
                gui_th2 = gui_exe.submit(self.input.get_system, 10)
                gui_th3 = gui_exe.submit(self.input.get_window, 10)
        except (KeyboardInterrupt, SystemExit):
            exit()
        print(gui_th0.result())
        print(gui_th1.result())
        print(gui_th2.result())
        print(gui_th3.result())

    def launch_gui(self):
        period = 3
        mouse = th.Thread(target=self.input.get_mouse(period), name='mo_data')
