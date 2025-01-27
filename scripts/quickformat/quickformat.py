import os
import black
from colorama import Fore as frg

input_dir = ""
file = ""

validity = False


def is_valid(usr_input):
    if os.path.exists(usr_input):
        global validity
        validity = True
    else:
        print("Invalid path")


def format_file(file_path):
    mode = black.FileMode()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

            # Format the code
        formatted_code = black.format_file_contents(code, fast=True, mode=mode)

        # Write the formatted code back to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(formatted_code)

    except Exception as e:
        print(f"An error occurred. More details: {e} ")


# TODO: Make exception when file is already formated not show as an exception.
# Also gotta do some comments


def format_code(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                format_file(file_path)


def main():
    continuity = True
    while continuity:
        print(
            frg.LIGHTGREEN_EX
            + """
                Quickformat
            """
            + frg.WHITE
            + """
                Welcome to Quickformat, a tool that cleans up and formats your messy Python code with ease.

                Quickformat uses the powerful Python Black code formatter under the hood to ensure that your 
                scripts are clean, consistent, and adhere to best practices of PEP 8, the official Python style guide.

                - Enter 'format' to begin the formatting process.
                - Enter 'back' to go to the main page.
            """
        )
        usr_input = input("Enter 'format' or 'back':")
        while usr_input not in ["format", "back"]:
            usr_input = input("Enter 'format' or 'back':")
        if usr_input == "format":
            usr_input = input("Certain file or directory? Enter 'directory'/'file': ")
            while usr_input not in ["file", "directory"]:
                usr_input = input(
                    "Certain file or directory? Enter 'directory'/'file': "
                )
            if usr_input == "file":
                while not validity:
                    x = input("Please enter a file you wish will be formated: ")
                    is_valid(x)
                format_file(x)
            elif usr_input == "directory":
                while not validity:
                    x = input("Please enter a directory you wish will be formated: ")
                    is_valid(x)
                format_code(x)

        else:
            continuity = False
