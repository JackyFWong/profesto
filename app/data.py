import threading as th
import json
import os
import time
import math

KEYBOARD_DATA = MOUSE_DATA = SYSTEM_DATA = WINDOW_DATA = None

remove_keyboard = [
    "[BACKSPACE]",
    "[TAB]",
    "[ENTER]",
    "[LCTRL]",
    "[LSHIFT]",
    "[RSHIFT]",
    "[LALT]",
    "[SPACE]",
    "[CAPSLOCK]",
    "[RCTRL]",
    "[RALT]"
]

def calc_dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

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
        start_time = time.time()
        end_time = start_time + period
        f.seek(0, 2)
        while time.time() < end_time:
            """
            # ensure contents present
            while not os.path.getsize(fname) > 0:
                pass
            """
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

    """Returns dict with { num_keys, wpm }
    """
    def get_keyboard(self, period):
        output = ""
        spaces = 0
        for line in get_data(period, "kb"):
            output += line
        wpm = (output.count("[SPACE]") * 60) / period
        for word in remove_keyboard:
            output = output.replace(word, "")
        return { "num_keys" : len(output), "wpm" : wpm }

    """Returns dict with { dist }
    """
    def get_mouse(self, period):
        output = []
        dist = 0
        last = None
        for line in get_data(period, "mo"):
            line = json.loads(line)
            output.append(line)
            if last == None:
                last = line
                continue
            dist += calc_dist(last, line)
        return { "dist" : dist }

    """Returns dict with system information
    """
    def get_system(self, period):
        core_tot = [0] * 4      # hard coded, bad practice
        cpu_tot = 0
        mem_tot_usg = 0
        mem_tot_per = 0
        swap_tot_usg = 0
        swap_tot_per = 0
        length = 0
        data = None
        for line in get_data(period, "sy"):
            data = eval(line)
            length += 1

            for idx, val in enumerate(data["core_per"]):
                core_tot[idx] += val
            cpu_tot += data["total_cpu_per"]
            mem_tot_usg += data["mem_usg"]
            mem_tot_per += data["mem_per"]
            swap_tot_usg += data["swap_usg"]
            swap_tot_per += data["swap_per"]
            
        core_avg = [0] * 4
        for idx, val in enumerate(core_tot):
            core_avg[idx] = round(val / length, 2)

        return {
            "core_per" : core_avg,
            "total_cpu_per" : round(cpu_tot / length, 2),
            "mem_usg" : get_size(mem_tot_usg / length),
            "mem_per" : round(mem_tot_per / length, 2),
            "swap_usg" : get_size(swap_tot_usg / length),
            "swap_per" : round(swap_tot_per / length, 2),
            "disk_read" : get_size(data["disk_read"]),
            "disk_write" : get_size(data["disk_write"]),
            "net_sent" : get_size(data["net_sent"]),
            "net_recv" : get_size(data["net_recv"])
        }

    """Returns dict with
        { process0 : duration, ..., processX : duration }
    """
    def get_window(self, period):
        processes = {}
        tot = 0
        for line in get_data(period, "wn"):
            data = eval(line)

            if data["pname1"] == None:
                continue
            if data["pname1"] not in processes:
                processes[data["pname1"]] = 1
            else:
                processes[data["pname1"]] += 1
            tot += 1

        for p in processes.keys():
            processes[p] = round((processes[p]/tot)*period, 3)

        return processes
