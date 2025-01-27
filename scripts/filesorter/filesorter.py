import os
import re
import shutil
from pathlib import Path

import send2trash
from colorama import Fore as frg
from colorama import init as init
from rich.progress import Progress
from colorama import Style

# All folder names/types

folders = [
    "Images",
    "Documents",
    "Ebooks",
    "Videos",
    "Audio",
    "Programs",
    "Fonts",
    "Code",
    "Archive",
    "Other",
]

# All extensions to sort them to corresponding folders

code_extensions = [
    "c",
    "class",
    "cpp",
    "cs",
    "css",
    "go",
    "h",
    "htaccess",
    "html",
    "java",
    "js",
    "json",
    "kml",
    "php",
    "pl",
    "py",
    "rb",
    "sql",
    "swift",
    "vb",
    "yaml",
    "ipynb",
]

ebook_extensions = [
    "epub",
    "pdb",
    "fb2",
    "ibook",
    "inf",
    "azw",
    "azw3",
    "mobi",
]

audio_extensions = ["mp3", "m4a", "aac", "oga", "flac", "wav", "pcm", "aiff"]

image_extensions = [
    "jpg",
    "jpeg",
    "jif",
    "jfif",
    "jfi",
    "png",
    "gif",
    "webp",
    "tiff",
    "tif",
    "psd",
    "raw",
    "arw",
    "cr2",
    "nrw",
    "k25",
    "bmp",
    "dib",
    "heif",
    "heic",
    "ind",
    "indd",
    "indt",
    "jp2",
    "j2k",
    "jpf",
    "jpx",
    "jpm",
    "mj2",
    "svg",
    "svgz",
    "ai",
    "eps",
    "pdf",
]

document_extensions = [
    "md",
    "txt",
    "rtf",
    "ppt",
    "ott",
    "odt",
    "ods",
    "odp",
    "docx",
    "doc",
    "csv",
]

program_extensions = [
    "bin",
    "jar",
    "apk",
    "exe",
    "msi",
    "run",
    "appimage",
    "sh",
    "fish",
]

video_extensions = [
    "webm",
    "mpg",
    "mp2",
    "mpeg",
    "mpe",
    "mpv",
    "ogg",
    "mp4",
    "m4p",
    "m4v",
    "avi",
    "wmv",
    "mov",
    "qt",
    "flv",
    "swf",
]

archive_extensions = ["zip", "7z", "pkg", "rpm", "z", "xz"]

font_extensions = ["vfb", "pfa", "fnt", "vlw", "jfproj", "woff", "sfd", "pfb"]

# Use progress for progress bars

with Progress(auto_refresh=True, refresh_per_second=10) as progress:

    # Added markdown to make text look nicer

    # Globally declaring downloads path and download list
    downloads_path = str(Path.home() / "Downloads")
    downloads_list = os.listdir(f"{downloads_path}")

    # Ask if user wants to sort downloads or custom path using some simple logic.

    def default_custom():

        while True:
            ask_for_path = input("Enter your path to sort: ")
            if os.path.isdir(ask_for_path) is False:
                pass
            else:
                global downloads_path
                global downloads_list
                downloads_path = str(ask_for_path)
                downloads_list = os.listdir(f"{ask_for_path}")
                break

    # Create folders if they don't exist to avoid duplicates

    def create_folders(folders, download_path):
        print("Creating folders...")
        for folder_type in folders:
            mypath = os.path.join(download_path, folder_type)
            if not os.path.isdir(mypath):
                os.makedirs(
                    mypath
                )  # Creates folder and necessary parent directories if needed
                print(f"Created folder: {mypath}")
            else:
                print(f"Folder already exists: {mypath}")

    # Whole logic behind removing file duplicates if they exist in path or renaming the file you are moving.

    def replace_or_keep(folder_name, file):
        global files_sent2trash

        # Checks if file already exists
        if not os.path.exists(downloads_path + "\\" + folder_name + "\\" + file):
            shutil.move(
                str(downloads_path + "\\" + file),
                str(downloads_path + "\\" + folder_name),
            )
        else:
            # If it exists, it asks for input if you want to keep both, or delete the older one
            replace_keep = input(
                f"{file} already exist. Do you want to replace it or keep both? replace/keep: "
            )
            while replace_keep not in ["replace", "keep"]:
                replace_keep = input(
                    f"{file} already exist. Do you want to replace it or keep both? replace/keep: "
                )

            # Logic for sending to trash
            if replace_keep == "replace":
                send2trash.send2trash(downloads_path + "\\" + folder_name + "\\" + file)
                shutil.move(
                    str(downloads_path + "\\" + file),
                    str(downloads_path + "\\" + folder_name),
                )
                files_sent2trash += 1

            # Regex to detect if file has the number, for example main_script(1).py
            else:
                file_path = downloads_path + "\\" + folder_name + "\\" + file
                file_path_reversed = file_path[::-1]
                digit_search = re.search("(\d+)", file_path_reversed)
                digit_search_span = digit_search.span
                if digit_search is not None and digit_search_span == "0":
                    digit_to_edit = digit_search.group()[::-1]
                    digit = digit_to_edit[1:-2]
                    file_name = os.rename(
                        downloads_path + "\\" + file,
                        downloads_path + "\\" + split_tup[0] + f"({digit})" + extension,
                    )
                    shutil.move(
                        file_name,
                        downloads_path
                        + "\\"
                        + folder_name
                        + "\\"
                        + split_tup[0]
                        + f"({digit})"
                        + extension,
                    )
                else:
                    os.rename(
                        downloads_path + "\\" + file,
                        downloads_path + "\\" + split_tup[0] + "(1)" + extension,
                    )
                    shutil.move(
                        downloads_path + "\\" + split_tup[0] + "(1)" + extension,
                        downloads_path
                        + "\\"
                        + folder_name
                        + "\\"
                        + split_tup[0]
                        + "(1)"
                        + extension,
                    )

    # Sort files to destination and use the replace_or_keep to not have.

    def run():
        task_id = progress.add_task(
            "[green]Sorting files...",
            total=len(downloads_list),
            completed_style="green",
        )
        global files_sorted
        global files_unsorted
        global files_sent2trash
        files_sent2trash = 0
        files_sorted = 0
        files_unsorted = 0
        for file in downloads_list:
            global split_tup
            global extension
            split_tup = os.path.splitext(file)
            extension = split_tup[1]
            extension = extension.replace(".", "")
            category = None
            progress.update(task_id, advance=1, refresh=True)
            if extension.lower() in code_extensions:
                replace_or_keep("Code", file)
                category = "Code"

            elif extension.lower() in ebook_extensions:
                replace_or_keep("Ebooks", file)
                category = "Ebook"

            elif extension.lower() in audio_extensions:
                replace_or_keep("Audio", file)
                category = "Audio"

            elif extension.lower() in image_extensions:
                replace_or_keep("Images", file)
                category = "Image"

            elif extension.lower() in document_extensions:
                replace_or_keep("Documents", file)
                category = "Document"

            elif extension.lower() in program_extensions:
                replace_or_keep("Programs", file)
                category = "Program"

            elif extension.lower() in video_extensions:
                replace_or_keep("Videos", file)
                category = "Video"

            elif extension.lower() in font_extensions:
                replace_or_keep("Fonts", file)
                category = "Font"

            elif extension.lower() in archive_extensions:
                replace_or_keep("Archive", file)
                category = "Archive"

            if category is not None:
                files_sorted += 1
            else:
                files_unsorted += 1
        init(autoreset=True)

        # About section

    def clean():
        file_list = []
        for file in downloads_list:
            if file not in file_list:
                file_list.append(file)
            else:
                send2trash.send2trash(file)

    def about():
        print(
            """
            ==================== About ====================

            File Sorter is a small python project made to help you with
            organising your files. If you have an idea for a feature or found a bug, just submit
            an issue on this projects Github page.
            """
        )

    # Checking if user input is valid
    def isvalid():
        global user_input
        # Keep asking for input until a valid input is provided
        while user_input not in ["sort", "custom", "about", "back"]:
            user_input = input(
                'Invalid input. Please enter "sort", "custom", "back" or "about": '
            )

    # Loop to get users input to navigate the command menu
    def main():
        global user_input
        continuity = True

        while continuity:
            print(
                frg.LIGHTGREEN_EX
                + """
                                File Sorter
                                  """
                + frg.WHITE
                + """
                  Please enter one of the commands below or type 'run' to execute the program:

                  - Enter 'sort' to sort the directory.
                  - Enter 'custom' to change the directory that will be the subject.
                  - Enter 'about' to get information about the project and credits.
                  - Enter 'back' to go back to main

                  ---  
                  Author: CyberCookieDev
                  """
            )
            user_input = input(
                frg.GREEN
                + 'Enter "sort", "custom", "back" or "about": '
                + Style.RESET_ALL
            )
            isvalid()  # Call the isvalid() function to ensure valid input

            if user_input == "sort":
                create_folders(folders, downloads_path)
                run()  # Call the run() function
                print(
                    frg.GREEN + f"Files sorted: {files_sorted}"
                )  # Print the statistics
                print(frg.RED + f"Files not sorted: {files_unsorted}")
                print(f"Files sent to trash: {files_sent2trash}")
                print(frg.GREEN + "Process ended succesfully")
                print(frg.WHITE + "(Note that folders count as unsorted files)")
                continuity = False  # Stop the loop
            elif user_input == "custom":
                default_custom()  # Call the default_custom() function
            elif user_input == "about":
                about()  # Call the about() function
            elif user_input == "back":
                continuity = False
