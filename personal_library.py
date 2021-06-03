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
# Letter definitions
import string
# Path manipulation
import os.path

# Entries in the directory
import os #os.listdir()

from args import ArgumentParser

from algo1 import String
import algo1

import libdic
from libdic import Dic

import linkedlist
from linkedlist import LinkedList

class Document:
    """ The document representation """
    uuid : int = 0
    def __init__(self,
            _title : String,
            _content : LinkedList[String]):
        self.title = _title
        self.content = _content
        self.uuid = Document.uuid
        Document.uuid = Document.uuid + 1

def main():
    """ The entry point """

    args = ArgumentParser(sys.argv)

    if args.lib:
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


def title_normalize(_title : String) -> String:
    """ Normalizes the file name:

    eg. "this is a test?_  " -> "this_is_a_test"

    """
    # O(|_title|)
    """
        Not tested with modified characters (á,ì,ŷ) and ñ
    """

    return algo1.lower(algo1.join(algo1.split(algo1.delete_symbols(_title), ' '), '_'))

###############################################################################
## Search specific code
###############################################################################

def search(_lib_folder : str, _args : list[str]) -> None:
    """ Handles the search of documents """

    print("Searching")
    print(_lib_folder)
    print(_args)


#def query(_word : String, _tfidf : Dic[String, TfidfRow]) -> Optional[TfidfRow]:
    """Return the relevant row """

#    return libdic.search(_tfidf, _word)

def empty_doc_dic() -> Dic[String, int]:
    """ A Standard dictionary for the document's word count"""

    return Dic(200, string_hash_function(200))

def doc_count_words(_doc : Document) -> Dic[String, int]:
    """ Count the words in a document """

    def folder(__acc : Dic[String, int], __word : String) -> Dic[String, int]:
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

def doc_tfidf(_docs : LinkedList[Document]) -> Dic[String, TfidfRow]:
    """ Coumpute the tfidf of a set of documents """


    def folder(__dic : Dic[String, TfidfRow], __doc : Document) -> Dic[String, TfidfRow]:
        """ Fold a new document into the matrix """

        counts : Dic[String, int] = doc_count_words(__doc)

        total_words : int = linkedlist.foldl(lambda x, y: x + y,
                0,
                libdic.to_list(counts))

        def folder_(__dic : Dic[String,
            TfidfRow], __elem : Tuple[String, int]) -> Dic[String, TfidfRow]:
            """ Fold a count entry into the matrix """
            (word, freq) = __elem

            return libdic.update_with_default(__dic,
                    lambda x : TfidfRow(linkedlist.insert(x.row , __doc.uuid, freq)),
                    word,
                    TfidfRow(linkedlist.singleton((__doc.uuid, freq / total_words))))


        return linkedlist.foldl(folder_,
                __dic,
                libdic.assocs(counts))


    tfidf : Dic[String, TfidfRow] = Dic(500, string_hash_function(500))

    return linkedlist.foldl(folder, tfidf, _docs)

def load_documents(_lib_folder : str) -> LinkedList[Document]:
    """ Load all the documents in the library """

    def read_doc(_doc : list) -> Document:
        """ Capture words in a document """

        def read_line(_line : String, _list : LinkedList[String]) -> LinkedList[String]:
            """ Capture words by line. Adds to _list """

            word : String = String('')

            # Explore characters in String
            for _ in range(algo1.strlen(_line)):

                if _line[_] != ' ' and _line[_] != '\n':
                    # Save character
                    word = algo1.concat(word, _line[_])

                elif algo1.strlen(word) != 0:
                    # Save word
                    _list = linkedlist.cons(word, _list)
                    word = algo1.String('')

            return _list


        def linkedlist_to_string(_list : LinkedList[String]) -> String:
            # Concatenate linkedlist elements

            return linkedlist.foldl(algo1.concat_string, String(''), _list)

        # LinkedLists for Document
        title : LinkedList[String] = linkedlist.empty()
        body : LinkedList[String] = linkedlist.empty()
        is_title : bool = True

        # Explore lists in _doc
        for _ in range(len(_doc)):
            if is_title:
                title = read_line(String(_doc[_]), title)
                is_title = False
            else:
                body = read_line(String(_doc[_]), body)

        new_doc : Document = Document(linkedlist_to_string(title), body)

        return new_doc

    # Add tailing / if missing
    if _lib_folder[-1] != '/':
        _lib_folder = _lib_folder + '/'

    # Add directory
    if _lib_folder[0] != '/':
        _lib_folder = os.getcwd() + '/' + _lib_folder
    else:
        _lib_folder = os.getcwd() + _lib_folder

    print(_lib_folder)
    # Existing path check
    if os.path.exists(_lib_folder):

        entries = os.listdir(_lib_folder)
        library : LinkedList[Document] = linkedlist.empty()

        # Access to documents
        for doc in entries:

            with open(_lib_folder + doc, 'r') as file_readable:
                text : list = file_readable.readlines()
            new_doc : Document = read_doc(text)
            library = linkedlist.cons(new_doc, library)

        return library

    else: print("Invalid path")

    return linkedlist.empty()

###############################################################################
## General purpose functions
###############################################################################

def heading(level : int, sep : str = ' ') -> None:
    """ Prints a heading """
    print('#' * level + sep, end='')

def string_hash_function(_size : int) -> Callable[[String], int]:
    """ Returns a string hash function """

    def hash_func(_key : String) -> int:
        """ Polynomial rolling hash function Horner's method O(|_key|)"""

        hash_value : int = 0
        seed_value : int = 53
        for _ in range(algo1.strlen(_key)):
            hash_value = (hash_value * seed_value + ord(_key[_])) % _size
        return hash_value

    return hash_func

if __name__ == '__main__':
    main()
