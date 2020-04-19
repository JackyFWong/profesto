import psutil
import platform
import threading as th
import os

OUT_FILE = "sys_out.log"

# https://www.thepythoncode.com/article/get-hardware-system-information-python
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def syst_info():
    out_str = "==========System Information===========\n"
    uname = platform.uname()
    out_str = (out_str +
        f"System: {uname.system}\n" +
        f"Node Name: {uname.node}\n" +
        f"Release: {uname.release}\n" +
        f"Version: {uname.version}\n" +
        f"Machine: {uname.machine}\n" +
        f"Processor: {uname.processor}\n")

    # CPU info
    cpufreq = psutil.cpu_freq()
    out_str = (out_str +
        "==========CPU Information==========\n" +
        f"Physical cores: {psutil.cpu_count(logical=False)}\n" +
        f"Logical cores: {psutil.cpu_count(logical=True)}\n" +
        f"Max freq: {cpufreq.max:.2f}Mhz\n")

    # Mem info
    vmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    out_str = (out_str +
        "==========Memory Information==========\n" +
        f"System memory: {get_size(vmem.total)}\n" +
        f"Swap memory: {get_size(swap.total)}\n")


    return out_str

class System:
    def __init__(self, erase):
        print(syst_info())
        if (erase == 'y'):
            open(OUT_FILE, "w+").close()

        self.out_str = ""
        self.cpu_freq = psutil.cpu_freq()
        self.v_mem = psutil.virtual_memory()
        self.swap = psutil.swap_memory()
        self.disk_io = psutil.disk_io_counters()
        self.net_io = psutil.net_io_counters()

        self.disk_start_read = self.disk_io.read_bytes
        self.disk_start_write = self.disk_io.write_bytes
        self.net_start_sent = self.net_io.bytes_sent
        self.net_start_recv = self.net_io.bytes_recv

    def data_stream(self):
        print(f"Thread {th.current_thread().name} online")
        print(f"---PID {os.getpid()}")
        while True:
            # CPU
            out_str = "======\nCPU per core:\n"
            for i, percent in enumerate(psutil.cpu_percent(percpu=True)):
                out_str = out_str + f"---Core {i}: {percent}%\n"
            out_str = out_str + f"Total CPU: {psutil.cpu_percent()}%\n\n"

            # Memory
            out_str = (out_str +
                f"Mem used: {get_size(self.v_mem.used)} ({self.v_mem.percent}%)\n" +
                f"Swap used: {get_size(self.swap.used)} ({self.swap.percent}%)\n\n")

            # Disk
            read = get_size(self.disk_io.read_bytes - self.disk_start_read)
            write = get_size(self.disk_io.write_bytes - self.disk_start_write)
            out_str = (out_str +
                f"Total disk read: {read}\n" +
                f"Total disk write: {write}\n\n")

            # Net
            sent = get_size(self.net_io.bytes_sent - self.net_start_sent)
            recv = get_size(self.net_io.bytes_recv - self.net_start_recv)
            out_str = (out_str +
                f"Total network sent: {sent}\n" +
                f"Total network received: {recv}\n\n")

            with open(OUT_FILE, "a") as f:
                f.write(out_str)
