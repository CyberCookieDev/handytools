from colorama import Fore as frg
from handytools.internal_code.quick_fetch import main_loop_quickfetch
from handytools.internal_code.quick_format import main_loop_quickformat
from file_sorter import main_loop_filesorter
from script_handling import run_outside_script
import os
import platform

file_list = []
downloaded_scripts = ""
path = "../scripts"


def clear_screen():
    # Check the operating system and clear accordingly
    if platform.system() == "Windows":
        os.system("cls")  # For Windows
    else:
        os.system("clear")  # For MacOS and Linux


for file in os.listdir(path):
    file_list.append(file)

for file in file_list:
    downloaded_scripts += (
        f"        - Enter '{file}' to go to {file}'s dedicated page.\n"
    )


def main_loop():
    to_continue = True
    while to_continue:
        clear_screen()

        menu_text = (
            frg.LIGHTGREEN_EX
            + "HandyTools\n"
            + frg.WHITE
            + """
            Welcome to HandyTools, your script toolbox with many useful utility programs!

            Please enter the program's name to go to its dedicated page, enter 'about' to read about
            HandyTools software, or enter 'exit' to exit.

                - Enter "quickfetch" to go to the Quickfetch dedicated page.
                - Enter "about" to get information about the project and credits.
                - Enter "filesorter" to go to File Sorter's dedicated page.
                - Enter "quickformat" to go to the Quick Format's dedicated page.
        """
            + downloaded_scripts
            + """
                - Enter "exit" to exit.

        """
            + frg.CYAN
            + "--------------------\n"
            + frg.MAGENTA
            + "Author: CyberCookieDev\n"
            + frg.WHITE
        )

        # Print the menu
        print(menu_text)
        answer = input("Enter one of the commands listed above: ")
        while (
            answer
            not in ["quickfetch", "quickformat", "filesorter", "about", "exit"]
            + file_list
        ):
            answer = input("Enter one of the commands listed above: ")
        if answer == "quickfetch":
            clear_screen()
            main_loop_quickfetch()
        elif answer == "about":
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
        elif answer == "quickformat":
            clear_screen()
            main_loop_quickformat()
        elif answer == "filesorter":
            clear_screen()
            main_loop_filesorter()
        elif answer == "exit":
            clear_screen()
            to_continue = False
        elif answer in file_list:
            run_outside_script(answer)


main_loop()
