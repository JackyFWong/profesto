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
    x = input("Write over old data? (y/n) ")

    msg = "testing thread from main.py"
    kb = keyboard.Keyboard(erase=x)
    mo = mouse.Mouse(erase=x)
    sy = system.System(erase=x)
    wn = window.Window(erase=x)
    dash = gui.Gui()

    try:
        with cf.ThreadPoolExecutor() as exe:
            th1 = exe.submit(kb.data_stream)
            th2 = exe.submit(mo.data_stream)
            th3 = exe.submit(sy.data_stream)
            th4 = exe.submit(wn.data_stream)
            th5 = exe.submit(dash.test)
    except (KeyboardInterrupt, SystemExit):
        exit()
