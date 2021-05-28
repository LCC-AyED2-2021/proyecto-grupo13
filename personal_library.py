"""
A virtual library of documents with querying capabilities.

 ________________________________________
/ This is NOT how you write python. This
| is PSEUDO python                       /
|
  #not-my-python
 ----------------------------------------
   *         __------~~-,
    *      ,'            ,
          /               *
         /                :
        |                  '
        |                  |
        |                  |
         |   _--           |
         _| =-.     .-.   ||
         o|/o/       _.   |
         /  ~          * |
       (____@)  ___~    |
          |_===~~~.`    |
       _______.--~     |
       *________       |
                *      |
              __/-___-- -__
             /            _ *

I denounce and renounce all the code in this repository.
"""
#pylint: disable=too-few-public-methods,no-else-return
#pylint: disable=unused-import

from typing import TypeVar, Generic, Callable, Optional, Tuple

# Capture command line arguments
import sys
# Parse command line arguments
import argparse
# Letter definitions
import string
# Path manipulation
import os.path

# Entries in the directory
import os #os.listdir()

import algo1

import libdic
from libdic import Dic

import linkedlist
from linkedlist import LinkedList

class Document:
    uuid : int = 0
    """ The document representation """
    def __init__(self,
            _title : str,
            _content : LinkedList[str]):
        self.title = _title
        self.content = _content
        self.uuid = Document.uuid
        Document.uuid = Document.uuid + 1

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


def empty_doc_dic() -> Dic[str, int]:
    """ A Standard dictionary for the document's word count"""

    """ hash_str is string_hash_function now
     Is the replacement correct?
    """

    return Dic(200, hash_str)
    #return Dic(200, string_hash_function)

def doc_count_words(_doc : Document) -> Dic[str, int]:
    """ Count the words in a document """

    def folder(__acc : Dic[str, int], __word : str) -> Dic[str, int]:
        """ Folds a new word into __acc """
        return libdic.update_with_default(__acc,
                lambda x : x + 1,
                __word,
                1)

    return linkedlist.foldl(folder, empty_doc_dic(), _doc.content)

class TfidfRow:
    """ An alias for the rows of the matrix.

    Elements are the doc.hash and the tfidf value.

    This could be upgraded to a priority queue.
    """
    def __init__(self,
            _row : LinkedList[Tuple[int, float]]):
        self.row = _row

def doc_tfidf(_docs : LinkedList[Document]) -> Dic[str, TfidfRow]:
    """ Coumpute the tfidf of a set of documents """


    def folder(__dic : Dic[str, TfidfRow], __doc : Document) -> Dic[str, TfidfRow]:
        """ Fold a new document into the matrix """

        counts : Dic[str, int] = doc_count_words(__doc)

        total_words : int = linkedlist.foldl(lambda x, y: x + y,
                0,
                libdic.to_list(counts))

        def folder_(__dic : Dic[str, TfidfRow], __elem : Tuple[str, int]) -> Dic[str, TfidfRow]:
            """ Fold a count entry into the matrix """
            (word, freq) = __elem

            return libdic.update_with_default(__dic,
                    lambda x : TfidfRow(linkedlist.insert(x.row , __doc.uuid, freq)),
                    word,
                    TfidfRow(linkedlist.singleton((__doc.uuid, freq / total_words))))


        return linkedlist.foldl(folder_,
                __dic,
                libdic.assocs(counts))

    """ hash_str is string_hash_function now
    Is the replacement correct?
    """

    tfidf : Dic[str, TfidfRow] = Dic(500, hash_str)
    #tfidf : Dic[str, TfidfRow] = Dic(500, string_hash_function)

    return linkedlist.foldl(folder, tfidf, _docs)

def load_documents(_lib_folder : str) -> LinkedList[Document]:
    """ Load all the documents in the library """

    """
    We assume that _lib_folder ends with "/". Eg: "/home/user/"
    """

    entries = os.listdir(_lib_folder)
    library : LinkedList[Document] = LinkedList()
    is_title : bool = True

    for doc in entries:
        body : LinkedList[str] = LinkedList()
        with open(_lib_folder + doc, 'r') as file_readable:
            for line in file_readable:
                for word in line.split():
                    if is_title:
                        title : str = word
                        is_title = False
                    else: linkedlist.insert(body, None, word)
        new_doc : Document[str, LinkedList] = Document(title, body)
        linkedlist.insert(library, None, new_doc)
    return library

###############################################################################
## General purpose functions
###############################################################################

def heading(level : int, sep : str = ' ') -> None:
    """ Prints a heading """
    print('#' * level + sep, end='')

def hash_str(_s : str) -> int:
    """ Hash a string """
    # TODO: Improve
    if len(_s) > 0:
        return 42 + ord(_s[0])
    else:
        return 69

def string_hash_function(_size : int, _s : str) -> Callable[[str], int]:
    """ Returns a string hash function """

    string=algo1.String(_s)
    hash_value : int = 0

    def hash_func(_key : str) -> int:
        """ Polynomial rolling hash function Horner's method"""

        p : int = 53
        for _ in range(len(string)): hash_value = (hash_value * ord(string[_]) + p) % _size
        return hash_value

    return hash_func

if __name__ == '__main__':
    main()
