"""
A virtual library of documents with querying capabilities.
"""
#pylint: disable=too-few-public-methods,no-else-return

# Capture command line arguments
import sys
# Parse command line arguments
import getopt
# Letter definitions
import string
# Path manipulation
import os.path

class Document:
    """ The document representation """
    def __init__(self,
            _title : str):
        self.title = _title

def main() -> None:
    """ The entry point """

    # Declare commands
    commands = ['create', 'search']

    # Parse commands
    opt_list, args = getopt.getopt(sys.argv[1:], '', commands)

    # Act on commands
    for opt, _ in opt_list:
        if opt == "--create":
            return create(args)
        elif opt == "--search":
            return search(args)
        else:
            print("Unknown command:", opt)

    # TODO: Write a more detailed usage message.
    print("Valid commands are:\n", '\n'.join(commands))

    return None

###############################################################################
## Create specific code
###############################################################################

def create(arg : list[str]) -> None:
    """ Handles the creation of a document """

    if len(arg) < 1:
        print('Please use: --create <library_path>')
        return

    root_folder = arg[0]

    heading(1)

    print("Creating a document\n")

    doc_title = input("What's the docment's title?\n")
    file_name = title_normalize(doc_title) + ".txt"
    file_path = os.path.join(root_folder, file_name)


    while os.path.exists(file_path):
        print("Error: file already exists: ", file_path)
        print("Please change the title")

        print("Creating a document\n")

        doc_title = input("What's the docment's title?\n")
        file_name = title_normalize(doc_title) + ".txt"
        file_path = os.path.join(root_folder, file_name)

    # At this point we know the document is not present

    print("Please, Enter the docment's content. Ctrl-D when Done.")
    with open(file_path, 'x') as file_handle:
        for line in sys.stdin.readlines():
            file_handle.write(line)

def title_normalize(title : str) -> str:
    """ Normalizes the file name:

    eg. "this is a test?_  " -> "this_is_a_test"

    """
    parts = title.strip().lower().split()
    words = [ ''.join( c for c in p if c in string.ascii_lowercase) for p in parts ]
    return '_'.join(words)


###############################################################################
## Search specific code
###############################################################################

def search(arg : list[str]) -> None:
    """ Handles the search of documents """
    print("Searching")
    print(arg)

###############################################################################
## General purpose functions
###############################################################################

def heading(level : int, sep : str = ' ') -> None:
    """ Prints a heading """
    print('#' * level + sep, end='')

if __name__ == '__main__':
    main()
