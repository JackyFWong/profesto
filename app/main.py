import json
import threading as th
import os

import keyboard
import mouse
import window
import system
import gui

def test(x):
    print("Thread {} online",format(th.current_thread().name))
    print("---PID {}",format(os.getpid()))
    print(x)

if __name__ == "__main__":
    x = input("Write over old data? (y/n) ")

    kb = keyboard.Keyboard(erase=x)
    mo = mouse.Mouse(erase=x)
    sy = system.System(erase=x)
    wn = window.Window(erase=x)

    msg = "testing thread from main.py"

    thread0 = th.Thread(target=test, name='main', args=(msg,))
    thread1 = th.Thread(target=kb.data_stream, name='kb_in')
    thread2 = th.Thread(target=mo.data_stream, name='mo_in')
    thread3 = th.Thread(target=sy.data_stream, name='sy_in')
    thread4 = th.Thread(target=wn.data_stream, name='wn_in')

    try:
        thread0.start()
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
    except (KeyboardInterrupt, SystemExit):
        print("Recieved keyboard interrupt, exiting...")
        sys.exit()
