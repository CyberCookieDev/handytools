import os
import json
import sys
import importlib
from importlib import util
import colorama
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from pathlib import Path
from internal_vital_scripts import generate_requirements
from internal_vital_scripts import format_file
import datetime
import psutil
import time
import send2trash

""" On a side note, this file is the one I, documenting the code long after writing it (which is a mistake by the way),
have the most problem documenting, so there might be mistakes, or not so clear moments."""

license = f"""
    Copyright {datetime.date.year} <COPYRIGHT HOLDER>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

path = "../../scripts"
downloaded_scripts = ""
file_list = []
home_path = Path.home()

# Loads a module given a path.


def load_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot find module '{module_name}' at '{path}'")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


with open("settings.json", "r") as f:
    settings = json.load(f)

# Checks for developer mode and if it is enabled, displays additional options
if settings["dev_mode"] == "true":
    dev_options = (
        ""
        + "\n"
        + "- Enter 'view' to view code of the script"
        + "\n"
        + "- Enter 'dependencies' to view dependencies."
        + "\n"
        + "- Enter 'scan' to scan and make scripts better."
    )
else:
    dev_options = ""


# opens files requirements.txt
def view_dependencies(filename):
    try:
        with open(f"../../scripts/{filename}/requirements.txt") as f:
            print("")
            print("Dependencies:")
            lines = f.read().splitlines()
            for x in lines:
                print(f"    - {x}")
            print("")

    except:
        print("Requirements are unavailible for this script.")
        x = input("Do you want to generate requirements? [y/n]:  ")
        while x not in ["y", "n"]:
            x = input("Do you want to generate requirements? [y/n]:  ")
        if x == "y":
            generate_requirements(f"scripts/{filename}", filename)
        else:
            pass


# Uses a bunch of functions to make the code better, like appending a license., generating requirements and formatting.
def improve_code(filename):
    try:
        with open(f"../../scripts/{filename}/requirements.txt") as f:
            pass
    except:
        print("Requirements are unavailible for this script.")
        x = input("Do you want to generate requirements? [y/n]:  ")
        while x not in ["y", "n"]:
            x = input("Do you want to generate requirements? [y/n]:  ")
        if x == "y":
            generate_requirements(f"scripts/{filename}", filename)
        else:
            pass
    for file in f"scripts/{filename}/":
        if file.endswith(".py"):
            format_file(file)
    if "LICENSE.txt" not in os.listdir(f"../../scripts/{filename}/"):
        with open(f"../../scripts/{filename}/LICENSE.txt", "w") as f:
            f.write(license)


# The big script running menu
def run_outside_script(filename):

    # Tries to load data about a project, if not available, displays placeholders.

    try:

        file = open(f"../../scripts/{filename}/{filename}.json", "r")
        loaded_data = json.load(file)
        print(
            colorama.Fore.LIGHTGREEN_EX
            + f"{loaded_data['title']}\n"
            + colorama.Style.RESET_ALL
            + colorama.Fore.WHITE
            + "\n"
            + f"{loaded_data['desc']} \n"
            + f'Filesize: {os.path.getsize(f"../../scripts/{filename}/{filename}.py")}\n'
            + "\n"
            + "- Enter 'run' to run the script"
            + "\n"
            + "- Enter 'exit' to exit."
            + "\n"
            + "- Enter 'delete' to delete."
            + dev_options
        )

    except Exception as e:

        print(e)

        print(
            f"{filename}"
            + "\n"
            + "Description not found"
            + f'Filesize: {os.path.getsize(f"../../scripts/{filename}/{filename}.py")}\n'
            + """
            - Enter 'run' to run the script.
            - Enter 'exit' to exit.
            - Enter 'delete' to delete.
            """
            + "\n"
            + dev_options
        )
    u_input = input("Enter one of the commands above: ")

    # Validity checks

    while u_input not in ["run", "exit", "view", "dependencies", "scan", "delete"]:
        u_input = input("Enter one of the commands above: ")

    if u_input == "exit":
        sys.exit()

    elif u_input == "run":

        module_path = os.path.join("../../scripts", filename, filename + ".py")

        if os.path.exists(module_path):

            # Tries to run using importlib.

            try:

                # Load the module dynamically
                spec = importlib.util.spec_from_file_location(filename, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Get the 'main' function and execute
                if hasattr(module, "main") and callable(module.main):

                    print(f"Running script: {filename}")

                    start_time = time.time()
                    cpu_start = psutil.cpu_percent(interval=None)

                    module.main()  # Run the script's main function

                    cpu_end = psutil.cpu_percent(interval=None)
                    end_time = time.time()

                    print(f"Execution completed in {end_time - start_time:.2f} seconds")
                    print(f"Average CPU usage: {(cpu_start + cpu_end) / 2:.2f}%")

                else:

                    print(
                        f"The script '{filename}' does not have a callable 'main()' function."
                    )

            except Exception as e:
                print(f"Error running script '{filename}': {e}")

        else:
            print(f"Module '{filename}' not found at {module_path}.")

    elif u_input == "view":
        # View the code.
        with open(f"../../scripts/{filename}/{filename}.py", "r") as file:
            code = file.read()
            highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())
            print(highlighted_code)
        run_outside_script(filename)

    elif u_input == "dependencies":
        # Just shows dependencies.
        view_dependencies(filename)
        run_outside_script(filename)

    elif u_input == "scan":
        improve_code(filename)
        run_outside_script(filename)

    elif u_input == "delete":
        # Deletes (sends to trash) the script folder.
        send2trash.send2trash(f"../../scripts/{filename}")
