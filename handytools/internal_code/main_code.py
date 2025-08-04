from colorama import Fore as frg
from script_handling import run_outside_script
import os
import platform
import json
import shutil
import internal_vital_scripts
import datetime


file_list = []
downloaded_scripts = ""
path = "../../scripts"
license = f"""
Copyright {str(datetime.date.year)} <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


def add_script(add_file_path):

    # Adds temporary json file with description, temporary name, and the default license (MIT License).

    if os.path.isfile(add_file_path) and add_file_path.endswith(".py"):
        file_name = os.path.splitext(os.path.basename(add_file_path))[0]

        target_dir = os.path.join(path, file_name)
        os.makedirs(target_dir, exist_ok=True)

        shutil.move(
            add_file_path, os.path.join(target_dir, os.path.basename(add_file_path))
        )

        json_file_path = os.path.join(target_dir, f"{file_name}.json")
        data = {
            "desc": "Temporary description, replace with actual description.",
            "title": f"Temporary name, {file_name}",
        }

        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        internal_vital_scripts.generate_requirements(add_file_path)

        with open(os.path.join(target_dir, f"LICENSE.txt")) as f:
            f.write(license)
        print("Added the default MIT License.")
        internal_vital_scripts.format_file(f"../../scripts/{file_name}/{file_name}.py")

        print("Remember to change the main command and data in the JSON file!")

    else:
        print("Something went wrong. Please provide a valid Python script path.")


def add_dir(add_file_path, file_name):

    # Repeatedly transfers files.
    if os.path.isdir(add_file_path):

        target_dir = os.path.join(path, file_name)
        os.makedirs(target_dir, exist_ok=True)

        for file in os.listdir(add_file_path):
            shutil.move(f"{add_file_path}/{file}", f"{target_dir}")

        json_file_path = os.path.join(target_dir, f"{file_name}.json")
        data = {
            "desc": "Temporary description, replace with actual description.",
            "title": f"Temporary name, {file_name}",
        }
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        internal_vital_scripts.generate_requirements(add_file_path)

        with open(os.path.join(target_dir, f"LICENSE.txt"), "w+") as f:
            f.write(license)
        print("Added the default MIT License.")
        internal_vital_scripts.format_file(f"../../scripts/{file_name}/{file_name}.py")

        print("Remember to change the main command and data in the JSON file!")

    else:
        print("Something went wrong. Please provide a valid Python script path.")


# Temporarily not working function to import things from GitHub
def add_from_github(git_url):
    print(
        "Please, ensure that the project you import is compatible with our standards."
    )
    u_input = input("Enter the github repositories link: ")
    x = input("Please enter the repositories name: ")
    print(
        "Note that if something isn't working, it probably might be the structure, please read the instructions.txt!"
    )


# Really basic function, kind of self explanatory.
def run_settings():
    u_input = input("Enable developer mode? [y/n]: ")
    while u_input not in ["y", "n"]:
        u_input = input("Enable developer mode? [y/n]: ")
    if u_input == "y":
        print("Please start the script again to apply changes.")
        return "true"
    if u_input == "n":
        print("Please start the script again to apply changes.")
        return "false"


def clear_screen():
    # Check the operating system and clear accordingly
    if platform.system() == "Windows":
        os.system("cls")  # For Windows
    else:
        os.system("clear")  # For MacOS and Linux


# Enables the visibility of dev commands based on the JSON file, that is changed by the run_settings()
with open("settings.json", "r") as jsonFile:
    data = json.load(jsonFile)
    if data["dev_mode"] == "true":
        dev_commands = """
        Dev Commands:
                    
        - Enter "add" to add a python script.
        """
    else:
        dev_commands = ""
# Adds files to file list
for file in os.listdir(path):
    validity = True
    if file.endswith(".txt") == False:
        file_list.append(file)
        downloaded_scripts += f"- {file}" + "\n" + "        "


# Main loop of the whole program
def main_loop():
    dev_mode = False
    to_continue = True
    while to_continue:
        clear_screen()
        menu_text = (
            frg.BLUE
            + """

  _    _                 _    _______          _     
 | |  | |               | |  |__   __|        | |    
 | |__| | __ _ _ __   __| |_   _| | ___   ___ | |___ 
 |  __  |/ _` | '_ \ / _` | | | | |/ _ \ / _ \| / __|
 | |  | | (_| | | | | (_| | |_| | | (_) | (_) | \__ |
 |_|  |_|\__,_|_| |_|\__,_|\__, |_|\___/ \___/|_|___/
                            __/ |                    
                           |___/                     

"""
            + frg.WHITE
            + """
            Welcome to HandyTools, your script toolbox with many useful utility programs!

        Please enter the program's name to go to its dedicated page, enter 'about' to read about
        HandyTools software, enter 'settings' to go to settings, or enter 'exit' to exit.
        """
            + """
        Commands:
        
        - Enter "exit" to exit.
        - Enter "about" to read about the project
        - Enter "settings" to open settings.
        """
            + dev_commands
            + """
        Currently installed scripts:
        """
            + downloaded_scripts
            + frg.CYAN
            + "--------------------\n"
            + frg.MAGENTA
            + "Author: CyberCookieDev\n"
            + frg.WHITE
        )

        # Print the menu
        print(menu_text)
        # Answer validity check, if valid, looks at the input and runs corresponding code.
        answer = input("Enter one of the commands listed above: ")

        while answer not in file_list and answer not in [
            "about",
            "exit",
            "settings",
            "add",
        ]:
            answer = input("Enter one of the commands listed above: ")

        if answer == "about":
            clear_screen()
            print(
                frg.LIGHTCYAN_EX
                + """
                                        ==================== About =====================
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
                                        ==================================================
                """
            )
        # Breaks the while loop terminating the script.
        elif answer == "exit":
            clear_screen()
            to_continue = False

        elif answer in file_list:
            clear_screen()
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
            clear_screen()
            u_input = input("Add directory or file? [dir/file]: ")

            while u_input not in ["dir", "file"]:
                u_input = input("Add directory or file? [dir/file]: ")

            if u_input == "dir":
                u_input = input("Paste filepath to the directory you want to add: ")
                x = input("What is the name of the main file?: ")
                add_dir(u_input, x)

            else:
                u_input = input("Paste filepath to the python file you want to add: ")
                add_script(u_input)


main_loop()
