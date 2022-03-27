###########################################################################
# Imports
###########################################################################
# Standard library imports
import os
from typing import List

# Local imports
# None

###########################################################################
# Code
###########################################################################


def get_all_python_files(directory: str) -> List[str]:
    """
    Get all files in a directory that end in .py.

    Parameters
    ----------
    directory : str
        The directory to search.

    Returns
    -------
    List[str]
        A list of all python files in the directory.
    """
    files = []
    for file in os.listdir(directory):
        if file.endswith(".py"):
            if file == os.path.basename(__file__):
                continue
            files.append(file)
    return files


def generate_autopep8_command(file: str) -> str:
    """
    Generate the autopep8 command for a file.

    Parameters
    ----------
    file : str
        The file to fix.

    Returns
    -------
    str
        The autopep8 command.
    """
    cmd = f"autopep8 {file} -a -a -a -a -a -i -v"
    return cmd


def generate_flake8_command(file: str) -> str:
    """
    Generate the flake8 command for a file.

    Parameters
    ----------
    file : str
        The file to fix.

    Returns
    -------
    str
        The flake8 command.
    """
    cmd = f"flake8 {file}"
    return cmd


def main():
    try:
        import autopep8 as at
    except ImportError:
        print("Please install autopep8.")
        return
    finally:
        del at
    files = get_all_python_files(os.getcwd())

    print("\n\nRunning Autopep8.")
    print("----------------------------------------------------------------")
    for file in files:
        print(F"\nFile: {file}")
        cmd = generate_autopep8_command(file)
        print(f"Running cmd : {cmd}")
        os.system(cmd)
    print("\nAutopep8 complete.")

    print("\n\nRunning Flake8.")
    print("----------------------------------------------------------------")
    for file in files:
        print(F"\nFile: {file}")
        cmd = generate_flake8_command(file)
        print(f"Running cmd : {cmd}")
        os.system(cmd)
    print("\nFlake8 complete.")


###########################################################################
# Main Code
###########################################################################
if __name__ == '__main__':
    main()
