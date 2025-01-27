import datetime
import json
import os
import platform
import socket

import psutil
import screeninfo
from colorama import Fore as frg, Style as Style


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

print(os.getcwd())
def quickfetch():
    system_name = platform.system()
    system_version = platform.release()
    build_number = platform.python_build()[0]
    machinery = platform.machine()
    processor = platform.processor()
    with open("../../scripts/quickfetch/config.json", "r") as f:
        loaded_data = json.load(f)

    print(frg.GREEN + "User: " + Style.RESET_ALL + socket.gethostname())
    print(frg.YELLOW + "=" * 40, "System Information", "=" * 40 + Style.RESET_ALL)
    if loaded_data["sys_name"] == True:
        print(
            frg.GREEN
            + "System:"
            + Style.RESET_ALL
            + f" {system_name} {system_version} {machinery}"
        )

    if loaded_data["uptime"] == True:
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
        print(
            frg.GREEN
            + "Boot Time: "
            + Style.RESET_ALL
            + f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
        )
    if loaded_data["basic_network"] == True:
        uname = platform.uname()
        print(
            frg.GREEN
            + "Ip-Address:"
            + Style.RESET_ALL
            + f"{socket.gethostbyname(socket.gethostname())}"
        )
        print(frg.GREEN + "Node Name:" + Style.RESET_ALL + f"{uname.node}")

    if loaded_data["python_data"] == True:

        print(
            frg.YELLOW
            + "\n--- Useful Python debugging/problem solving data ---\n"
            + Style.RESET_ALL
        )
        print(
            frg.GREEN
            + "Python version:"
            + Style.RESET_ALL
            + f" {platform.python_version()}"
        )
        print(frg.GREEN + "Python build number:" + Style.RESET_ALL + f" {build_number}")
        print(
            frg.GREEN
            + "Python build date:"
            + Style.RESET_ALL
            + f" {platform.python_build()[1]}"
        )
        print(
            frg.GREEN
            + "Python compiler:"
            + Style.RESET_ALL
            + f" {platform.python_compiler()}"
        )
        print(
            frg.GREEN
            + "Python implementation:"
            + Style.RESET_ALL
            + f" {platform.python_implementation()}"
        )
        print(frg.GREEN + "Python build number:" + Style.RESET_ALL + f" {build_number}")

    print(frg.YELLOW + "\n" + "=" * 40, "Hardware", "=" * 40 + "\n" + Style.RESET_ALL)
    if loaded_data["processor"] == True:

        print(frg.GREEN + "Processor:" + Style.RESET_ALL + f" {processor}")

    if loaded_data["res"] == True:
        m = screeninfo.get_monitors()
        for i in m:
            print(frg.BLUE + f"\n--- Monitor {i.name}  ---" + Style.RESET_ALL)
            if i.is_primary == True:
                print(
                    frg.GREEN
                    + "Is it primary?:"
                    + Style.RESET_ALL
                    + frg.LIGHTGREEN_EX
                    + " Yes"
                    + Style.RESET_ALL
                )
            else:
                print(
                    frg.GREEN
                    + "Is it primary?: "
                    + Style.RESET_ALL
                    + frg.RED
                    + "No"
                    + Style.RESET_ALL
                )
            print(
                frg.GREEN
                + "Screen resolution: "
                + Style.RESET_ALL
                + f"{i.width}X{i.height}"
            )

    if loaded_data["memory_data"] == True:

        # get the memory details
        print(frg.YELLOW + "\n--- Memory Information ---\n" + Style.RESET_ALL)
        svmem = psutil.virtual_memory()
        print(frg.GREEN + "Total:" + Style.RESET_ALL + f" {get_size(svmem.total)}")
        print(
            frg.GREEN + "Available:" + Style.RESET_ALL + f" {get_size(svmem.available)}"
        )
        print(frg.GREEN + "Used:" + Style.RESET_ALL + f" {get_size(svmem.used)}")
        print(frg.GREEN + "Percentage:" + Style.RESET_ALL + f" {svmem.percent}%")

    if loaded_data["disk_data"] == True:

        print(frg.YELLOW + "\n--- Disk Data ---\n" + Style.RESET_ALL)
        partitions = psutil.disk_partitions()

        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            print(
                frg.GREEN
                + "Total Size:"
                + Style.RESET_ALL
                + f" {get_size(partition_usage.total)}"
            )
            print(
                frg.GREEN
                + "Used:"
                + Style.RESET_ALL
                + f" {get_size(partition_usage.used)}"
            )
            print(
                frg.GREEN
                + "Free:"
                + Style.RESET_ALL
                + f" {get_size(partition_usage.free)}"
            )
            print(
                frg.GREEN
                + "Percentage:"
                + Style.RESET_ALL
                + f" {partition_usage.percent}%"
            )


def main():
    continuity = True
    while continuity:
        print(
            frg.LIGHTGREEN_EX
            + """
                Quickfetch
            """
            + frg.WHITE
            + """
                Welcome to Quickfetch, tool displaying some info about your OS and hardware. You can freely customize
                what it displays to match your needs.
                
                - Enter 'fetch' to display the data.
                - Enter 'custom' to customize #TODO: Currently not available.
                - Enter 'back' to go to the main page.
            """
        )
        answer = input("")
        while answer not in ["fetch", "custom", "back"]:
            answer = input("")
        if answer == "fetch":
            quickfetch()
        if answer == "back":
            continuity = False