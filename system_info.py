import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_system_info():
    info = ''
    info += "[INFO]  System Information\n"
    uname = platform.uname()
    info += f"System: {uname.system}\n"
    info += f"Node Name: {uname.node}\n"
    info += f"Release: {uname.release}\n"
    info += f"Version: {uname.version}\n"
    info += f"Machine: {uname.machine}\n"
    info += f"Processor: {uname.processor}\n"
    info += f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n"
    info += f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n"
    info += f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n"

    # Boot Time
    info += "[INFO] Boot Time:\n"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    info += f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n"

    # print CPU information
    info += "[INFO] CPU Info\n"
    # number of cores
    info += f"Physical cores: {psutil.cpu_count(logical=False)}\n"
    info += f"Total cores: {psutil.cpu_count(logical=True)}\n"
    # CPU frequencies
    # CPU usage
    info += "CPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        info += f"Core {i}: {percentage}%\n"
    info += f"Total CPU Usage: {psutil.cpu_percent()}%\n"

    # Memory Information
    info += "[INFO] Memory Information\n"
    # get the memory details
    svmem = psutil.virtual_memory()
    info += f"Total: {get_size(svmem.total)}\n"
    info += f"Available: {get_size(svmem.available)}\n"
    info += f"Used: {get_size(svmem.used)}\n"
    info += f"Percentage: {svmem.percent}%\n"
    # Disk Information
    info += "[INFO] Disk Information\n"
    info += "Partitions and Usage:\n"
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        info += f"=== Device: {partition.device} ===\n"
        info += f"  Mountpoint: {partition.mountpoint}\n"
        info += f"  File system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        info += f"  Total Size: {get_size(partition_usage.total)}\n"
        info += f"  Used: {get_size(partition_usage.used)}\n"
        info += f"  Free: {get_size(partition_usage.free)}\n"
        info += f"  Percentage: {partition_usage.percent}%\n"
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    info += f"Total read: {get_size(disk_io.read_bytes)}\n"
    info += f"Total write: {get_size(disk_io.write_bytes)}\n"

    net_io = psutil.net_io_counters()
    info += f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n"
    info += f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n"
    return info

if __name__ == "__main__":
    print(get_system_info())
