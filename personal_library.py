"""
A virtual library of documents with querying capabilities.
"""
#pylint: disable=too-few-public-methods,no-else-return

from typing import TypeVar, Generic, Callable, Optional, Tuple

# Capture command line arguments
import sys
# Parse command line arguments
import argparse
# Letter definitions
import string
# Path manipulation
import os.path

import hashlib

class Document:
    """ The document representation """
    def __init__(self,
            _title : str):
        self.title = _title

def main() -> None:
    """ The entry point """

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("lib", help = "Where to store/search for files")
    arg_parser.add_argument("--create", help = "Create a document", action="store_true")
    arg_parser.add_argument("--search", help = "Search a term")

    args = arg_parser.parse_args()

    if args.create:
        return create(args.lib)
    elif args.search:
        return search(args.lib, args.search)

    return None

###############################################################################
## Create specific code
###############################################################################

def create(_lib_folder : str) -> None:
    """ Handles the creation of a document """

    heading(1)

    print("Creating a document\n")

    doc_title = input("What's the docment's title?\n")
    file_name = title_normalize(doc_title) + ".txt"
    file_path = os.path.join(_lib_folder, file_name)


    # Keep asking until there are no colisions
    while os.path.exists(file_path):
        print("Error: file already exists: ", file_path)
        print("Please change the title")

        print("Creating a document\n")

        doc_title = input("What's the docment's title?\n")
        file_name = title_normalize(doc_title) + ".txt"
        file_path = os.path.join(_lib_folder, file_name)

    # At this point we know the document is not present

    print("Please, Enter the docment's content. Ctrl-D when Done.")
    with open(file_path, 'x') as file_handle:
        file_handle.write(doc_title + '\n')
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

def search(_lib_folder : str, _args : list[str]) -> None:
    """ Handles the search of documents """

    print("Searching")
    print(_lib_folder)
    print(_args)

###############################################################################
## General purpose functions
###############################################################################

def heading(level : int, sep : str = ' ') -> None:
    """ Prints a heading """
    print('#' * level + sep, end='')

if __name__ == '__main__':
    main()
