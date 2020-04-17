import keyboard
import mouse
import window as wn
import system as sy
import gui

import json
import threading as th
import os

def test(x):
    print("Thread {} online",format(th.current_thread().name))
    print("---PID {}",format(os.getpid()))
    print(x)

if __name__ == "__main__":
    x = input("Write over old data? (y/n)")

    kb = keyboard.Keyboard(erase = x)
    mo = mouse.Mouse(erase = x)
    msg = "hello world"

    thread1 = th.Thread(target=kb.data_stream, name='kb_in')
    thread2 = th.Thread(target=test, name='test', args=(msg,))
    thread3 = th.Thread(target=mo.data_stream, name='mo_in')

    try:
        thread1.start()
        thread2.start()
        thread3.start()
    except (KeyboardInterrupt, SystemExit):
        print("Recieved keyboard interrupt, exiting...")
        sys.exit()
