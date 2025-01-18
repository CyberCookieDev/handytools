from colorama import Fore as frg
from script_handling import run_outside_script
import os
import platform
import json
from pathlib import Path
import shutil

file_list = []
downloaded_scripts = ""
path = "scripts"

import os
import shutil
import json


def add_script(add_file_path):
    if os.path.isfile(add_file_path) and add_file_path.endswith(".py"):
        file_name = os.path.splitext(os.path.basename(add_file_path))[0]

        target_dir = os.path.join(path, file_name)
        os.makedirs(target_dir, exist_ok=True)

        shutil.move(add_file_path, os.path.join(target_dir, os.path.basename(add_file_path)))

        json_file_path = os.path.join(target_dir, f"{file_name}.json")
        data = {
            "desc": "Temporary description, replace with actual description.",
            "title": f"Temporary name, {file_name}",
            "main_command": f"main_loop_{file_name}",
        }
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print("Remember to change the main command and data in the JSON file!")
    else:
        print("Something went wrong. Please provide a valid Python script path.")


def run_settings():
    u_input = input("Enable developer mode? [y/n]: ")
    while u_input not in ["y", "n"]:
        u_input = input("Enable developer mode? [y/n]: ")
    if u_input == "y":
        return "true"
    if u_input == "n":
        return "false"
    print("Please restart the script again to apply changes.")
def clear_screen():
    # Check the operating system and clear accordingly
    if platform.system() == "Windows":
        os.system("cls")  # For Windows
    else:
        os.system("clear")  # For MacOS and Linux

with open("settings.json", "r") as jsonFile:
    data = json.load(jsonFile)
    if data["dev_mode"] == "true":
            dev_commands = (
        """
        Dev Commands:
                    
        - Enter "add" to add a python script.
        """
                    )
    else:
        dev_commands = ""

for file in os.listdir(path):
    validity = True
    if file.endswith(".txt") == False:
        file_list.append(file)

for file in file_list:
    if file.endswith(".txt") == False:
        downloaded_scripts += (
            f"- {file}" + "\n" + "        "
        )

def main_loop():
    dev_mode = False
    to_continue = True
    while to_continue:
        clear_screen()

        menu_text = (
                frg.LIGHTGREEN_EX
                + "HandyTools\n"
                + frg.WHITE
                + """Welcome to HandyTools, your script toolbox with many useful utility programs!

        Please enter the program's name to go to its dedicated page, enter 'about' to read about
        HandyTools software, enter 'settings' to go to settings, or enter 'exit' to exit.

        Currently installed scripts:
        """
                + downloaded_scripts
                + """
        Commands:
        
        - Enter "exit" to exit.
        - Enter "about" to read about the project
        - Enter "settings" to open settings.
        """
                + dev_commands
                + frg.CYAN
                + "--------------------\n"
                + frg.MAGENTA
                + "Author: CyberCookieDev\n"
                + frg.WHITE
        )

        # Print the menu
        print(menu_text)
        answer = input("Enter one of the commands listed above: ")
        while answer not in file_list and answer not in ["about", "exit", "settings", "add"]:
            answer = input("Enter one of the commands listed above: ")
        if answer == "about":
            clear_screen()
            print(
                frg.LIGHTCYAN_EX
                + """
                                        ==================== About ====================
                """
                + frg.WHITE
                + """

                                        HandyTools is a small Python project that serves as a
                                        script hub, featuring a variety of useful utilities 
                                        for everyday Python development. From file management 
                                        tools to code formatting, HandyTools aims to save time 
                                        and streamline your workflow.

                                        Whether you're working on personal projects or professional
                                        tasks, HandyTools offers handy scripts to simplify common 
                                        tasks and boost your productivity.

                                        If you want to contribute to this project, visit the 
                                        GitHub page.

                """
                + frg.LIGHTCYAN_EX
                + """
                                        --------------------------------------------
                """
            )
        elif answer == "exit":
            clear_screen()
            to_continue = False
        elif answer in file_list:
            run_outside_script(answer)
        elif answer == "settings":
            dev_mode = run_settings()
            # Read the JSON file
            with open("settings.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["dev_mode"] = dev_mode
            with open("settings.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)
        elif answer == "add":
            u_input = input("Paste filepath to the python file you want to add: ")
            add_script(u_input)

main_loop()
