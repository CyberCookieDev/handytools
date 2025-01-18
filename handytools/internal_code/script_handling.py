import os
import json
import sys
import importlib
from importlib import util
import colorama

path = "scripts"
downloaded_scripts = ""
file_list = []


def load_module_from_path(path, module_name):
    """Dynamically loads a module from a given file path."""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot find module '{module_name}' at '{path}'")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

f = open("settings.json", "r")
settings = json.load(f)

if settings["dev_mode"] == "true":
    dev_options = (""
            +"\n"
            + "- Enter 'view' to view code of the script"
            + "\n"
            + "- Enter 'dependencies' to view dependencies."
    )
else:
    dev_options = ""

def run_outside_script(filename):
    try:
        file = open(f"scripts/{filename}/{filename}.json", "r")
        loaded_data = json.load(file)
        print(
            colorama.Fore.LIGHTGREEN_EX
            + f"{loaded_data['title']}\n"
            + colorama.Style.RESET_ALL
            + colorama.Fore.WHITE
            + "\n"
            + f"{loaded_data['desc']} \n"
            + "\n"
            + "- Enter 'run' to run the script"
            + "\n"
            + "- Enter 'exit' to go back to main page."
            + dev_options
        )
    except Exception as e:
        print(e)
        print(
            f"{filename}"
            + "\n"
            + "Description not found"
            + """
            - Enter 'run' to run the script.
            - Enter 'exit' to go back to main page.
            """
        )
    u_input = input("Enter 'run' or 'exit: ")
    while u_input not in ["run", "exit"]:
        u_input = input("Enter 'run' or 'exit': ")
    if u_input == "exit":
        sys.exit()
    else:
        # Assume 'filename' is the name of the module or directory
        # Example: "module_name" for "scripts/module_name/module_name.py"
        module_path = os.path.join("scripts", filename, filename + ".py")

        if os.path.exists(module_path):

            module = load_module_from_path(module_path, filename)

            # Assuming `loaded_data["main_command"]` holds the function name to execute
            function_name = loaded_data.get("main_command")

            if hasattr(module, function_name):
                function_to_run = getattr(module, function_name)
                function_to_run()
            else:
                print(f"Function '{function_name}' not found in {filename}.")
        else:
            print(f"Module '{filename}' not found at {module_path}.")
