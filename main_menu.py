from colorama import Fore as frg
from quick_fetch import main_loop_quickfetch
from quick_format import main_loop_quickformat
from file_sorter import main_loop_filesorter
import os
import platform

def clear_screen():
    # Check the operating system and clear accordingly
    if platform.system() == "Windows":
        os.system("cls")  # For Windows
    else:
        os.system("clear")  # For MacOS and Linux
def main_loop():
    to_continue = True
    while to_continue:
        clear_screen()
        print(frg.LIGHTGREEN_EX + """
                                HandyTools
            """ + frg.WHITE + """

                                Welcome to HandyTools, your script toolbox with many useful utility programs!

                                Please enter the program's name to go to its dedicated page, enter 'about' to read about
                                HandyTools software or enter 'exit' to exit.

                                - Enter "quickfetch" to go to the Quickfetch dedicated page.
                                - Enter "about" to get information about the project and credits.
                                - Enter "filesorter" to go to File Sorter's dedicated page.
                                - Enter "quickformat" to go to the Quick Format's dedicated page.
                                - Enter "exit" to exit.

                                """ + frg.CYAN + """
                                ---
            """ + frg.MAGENTA + """
                                Author: CyberCookieDev
            """ + frg.WHITE + """
            """)

        answer = input("Enter 'quickfetch','quickformat', 'filesorter', 'about' or 'exit': ")
        while answer not in ['quickfetch','quickformat', 'filesorter', 'about','exit']:
            answer = input("")
        if answer == "quickfetch":
            clear_screen()
            main_loop_quickfetch()
        elif answer == "about":
            clear_screen()
            print(
                frg.LIGHTCYAN_EX + """
                                        ==================== About ====================
                """
                + frg.WHITE + """

                                        HandyTools is a small Python project that serves as a
                                        script hub, featuring a variety of useful utilities 
                                        for everyday Python development. From file management 
                                        tools to code formatting, HandyTools aims to save time 
                                        and streamline your workflow.

                                        Whether you're working on personal projects or professional
                                        tasks, HandyTools offers handy scripts to simplify common 
                                        tasks and boost your productivity.

                                        If you want to contribute to this project, visit the 
                                        GitHub page: [GitHub Link Here]

                """
                + frg.LIGHTCYAN_EX + """
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

main_loop()