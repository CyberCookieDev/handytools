import os
import black


def find_imports_in_file(file_path):
    
    external_modules = []

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

            for line in lines:
                line = line.strip()
                if line.startswith("import") or line.startswith("from"):

                    parts = line.split()
                    if parts[0] == "import":
                        external_modules.append(parts[1].split(".")[0])
                    elif parts[0] == "from":
                        external_modules.append(parts[1].split(".")[0])

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

    return external_modules


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


def generate_requirements(directory, filename):
    """Generate requirements.txt based on imports in Python files."""
    modules = set()  # Use a set to avoid duplicates

    # Traverse the directory and subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                # Find external imports in the Python file
                imports = find_imports_in_file(file_path)
                modules.update(imports)

    # Write the results to requirements.txt
    with open(f"scripts/{filename}/requirements.txt", "w") as req_file:
        for module in sorted(modules):
            req_file.write(f"{module}\n")
