import json
import threading as th
import concurrent.futures as cf
import os

import keyboard
import mouse
import system
import window
import gui

if __name__ == "__main__":
    #x = input("Write over old data? (y/n) ")
    x = 'y'

    msg = "testing thread from main.py"
    kb = keyboard.Keyboard(erase=x)
    mo = mouse.Mouse(erase=x)
    sy = system.System(erase=x)
    wn = window.Window(erase=x)
    dash = gui.Gui()
    th0 = th.Thread(target=kb.data_stream, daemon=True)
    th1 = th.Thread(target=mo.data_stream, daemon=True)
    th2 = th.Thread(target=sy.data_stream, daemon=True)
    th3 = th.Thread(target=wn.data_stream, daemon=True)

    try:
        """
        with cf.ThreadPoolExecutor() as exe:
            th1 = exe.submit(kb.data_stream)
            th2 = exe.submit(mo.data_stream)
            th3 = exe.submit(sy.data_stream)
            th4 = exe.submit(wn.data_stream)
        """
        th0.start()
        th1.start()
        th2.start()
        th3.start()

        # cannot run PySimpleGUI from thread
        dash.launch_gui()
    except (KeyboardInterrupt, SystemExit):
        exit()

