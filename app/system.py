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
        f"Max freq: {cpufreq.max/1000:.2f}Ghz\n")

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
        #print(syst_info())
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
        """ Format:
            {
                core_per : [core0%, ..., coreN%], total_cpu_per : X%,
                mem_usg : XGB, mem_per : X%, swap_usg : XGB, swap_per : X%,
                disk_read : XGB, disk_write : XGB,
                net_sent : XGB, net_recv : XGB,
            }
        """
        while True:
            out_str = "{"
            
            # CPU
            out_str += "'core_per':["
            for i, percent in enumerate(psutil.cpu_percent(percpu=True)):
                out_str += f"{percent},"
            out_str += f"],'total_cpu_per':{psutil.cpu_percent()},"

            # Mem
            out_str += ( f"'mem_usg':{self.v_mem.used}," +
                f"'mem_per':{self.v_mem.percent}," +
                f"'swap_usg':{self.swap.used}," +
                f"'swap_per':{self.swap.percent}," )

            # Disk
            out_str += ( f"'disk_read':{self.disk_io.read_bytes - self.disk_start_read}," +
                f"'disk_write':{self.disk_io.write_bytes - self.disk_start_write}," )

            # Net
            out_str += ( f"'net_sent':{self.net_io.bytes_sent - self.net_start_sent}," +
                f"'net_recv':{self.net_io.bytes_recv - self.net_start_recv}" )

            out_str += "}\n"
            with open(OUT_FILE, "a") as f:
                f.write(out_str)
