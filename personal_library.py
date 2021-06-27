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

import math
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
# Persistence
import persist

from algo1 import String
import algo1

import libdic
from libdic import Dic

import linkedlist
from linkedlist import LinkedList



class Document:
    """ The document representation """
    uuid : int = 0

    directory : Dic[int, String] = Dic(1000,
            libdic.multiplicative_hash_function(1000, libdic.golden_ratio()))

    def __init__(self,
            _title : String,
            _content : LinkedList[String],
            _uuid : Optional[int] = None):
        self.title = _title
        self.content = _content

        if not _uuid is None:
            assert libdic.search(Document.directory, _uuid) is None
            self.uuid = _uuid
            Document.directory = libdic.insert(Document.directory, self.uuid,
                    self.title)
            if Document.uuid < _uuid:
                Document.uuid = _uuid
        else:
            self.uuid = Document.uuid
            Document.uuid = Document.uuid + 1

            Document.directory = libdic.insert(Document.directory, self.uuid,
                    self.title)

    def __str__(self):
        return str(self.uuid) + str(self.title) + "\n" + str(self.content)

class TfidfRow:
    """ An alias for the rows of the matrix.

    Elements are the doc.hash and the tfidf value.

    This could be upgraded to a priority queue.
    """
    def __init__(self,
            _row : LinkedList[Tuple[int, Tuple[int, float]]]):
        self.row = _row

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

    print("Creating index...")

    documetnts = load_documents(_lib_folder)

    print("Computing index...")
    tfidf = doc_tfidf(documetnts)

    print("Save index...")
    with open("tfidf.def", 'x') as file_writable:
        persist.save(tfidf, file_writable)

    print("Save directory...")
    with open("directory.def", 'x') as file_writable:
        persist.save(Document.directory, file_writable)

    libdic.dic_health(tfidf)
    print("Done")

def title_normalize(_title : String) -> String:
    """ Normalizes the file name:

    eg. "this is a test?_  " -> "this_is_a_test"

    # O(|_title|)

        Not tested with modified characters (á,ì,ŷ) and ñ
    """

    return algo1.lower(
            linkedlist.ljoin(
                linkedlist.str_split(algo1.delete_symbols(_title), ' '), '_'))

###############################################################################
## Search specific code
###############################################################################

def search(_lib_folder : str, _args : str) -> None:
    """ Handles the search of documents """

    print("Searching: " + _args)

    print("Load index...")
    tfidf = None
    with open("tfidf.def", 'r') as file_readable:
        tfidf = persist.load(file_readable)

    assert not tfidf is None

    print("Load directory...")
    directory = None
    with open("directory.def", 'r') as file_readable:
        directory = persist.load(file_readable)

    assert not directory is None

    results = query(String(_args), tfidf)

    if results is None:
        print("No results")
    else:

        result_row = results.row

        print("Freq", "title", "relevance", sep="\t")
        while not result_row.content is None:

            (doc_id, (freq, relevance)) =  result_row.content[0]
            result_row = result_row.content[1]

            title = libdic.search(directory, doc_id)

            print(freq, title, relevance, sep="\t")



def query(_word : String, _tfidf : Dic[String, TfidfRow]) -> Optional[TfidfRow]:
    """Return the relevant row """

    return libdic.search(_tfidf, _word)

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


def doc_tfidf(_docs : LinkedList[Document]) -> Dic[String, TfidfRow]:
    """ Coumpute the tfidf of a set of documents """

    n_docs : int = linkedlist.length(_docs)

    assert n_docs > 0

    def idf_folder(__idf : Dic[String, float],
            __doc : Document) -> Dic[String, float]:
        """ Fold a new document into the matrix """

        word_set : Dic[String, int] = doc_count_words(__doc)

        def folder_(___idf : Dic[String, float],
                ___word : String) -> Dic[String, float]:
            """ Fold a new word into the matrix """

            return libdic.update_with_default(___idf,
                    lambda x: x + 1,
                    ___word, 1)

        return linkedlist.foldl(folder_, __idf, libdic.keys(word_set))

    # idf["word"] = log (n_docs / <number of docs that contain "word" )

    idf : Dic[String, float] = Dic(500, string_hash_function(500))

    idf = linkedlist.foldl(idf_folder, idf, _docs)

    idf = libdic.dmap(lambda x : math.log(n_docs / x), idf)

    def tfidf_folder(__tf : Dic[String, TfidfRow],
            __doc : Document) -> Dic[String, TfidfRow]:
        """ Fold a new document into the matrix """

        nonlocal idf

        counts : Dic[String, int] = doc_count_words(__doc)

        total_words : int = linkedlist.foldl(lambda x, y: x + y,
                0,
                libdic.to_list(counts))

        def folder_(__tf : Dic[String, TfidfRow],
                __elem : Tuple[String, int]) -> Dic[String, TfidfRow]:
            """ Fold a count entry into the matrix """
            nonlocal idf

            (word, freq) = __elem

            word_idf_result = libdic.search(idf, word)

            assert not word_idf_result is None

            word_idf : float = word_idf_result


            return libdic.update_with_default(__tf,
                    lambda x : TfidfRow(linkedlist.insert(x.row , __doc.uuid,
                        (freq, freq / total_words * word_idf))),
                    word,
                    TfidfRow(linkedlist.singleton((__doc.uuid,
                        (freq, freq / total_words * word_idf)))))


        return linkedlist.foldl(folder_,
                __tf,
                libdic.assocs(counts))

    #                      <number of times "word" appears in doc>
    # tfidf["word", doc] = --------------------------------------- * idf["word"]
    #                      <total words in doc>

    tfidf : Dic[String, TfidfRow] = Dic(500, string_hash_function(500))

    tfidf = linkedlist.foldl(tfidf_folder, tfidf, _docs)

    # Sort in decreasing order
    def lte(__a : Tuple[int, Tuple[int, float]],
            __b : Tuple[int, Tuple[int, float]]) -> bool:
        return __a[1][0] > __b[1][0]


    tfidf = libdic.dmap(lambda r:
            TfidfRow(linkedlist.quick_sort_by(lte, r.row)), tfidf)

    return tfidf


def load_documents(_lib_folder : str) -> LinkedList[Document]:
    """ Load all the documents in the library """

    print("Laoding documents...")

    # Add tailing / if missing
    if _lib_folder[-1] != '/':
        _lib_folder = _lib_folder + '/'

    # Add directory
    if _lib_folder[0] != '/':
        _lib_folder = os.getcwd() + '/' + _lib_folder
    else:
        _lib_folder = os.getcwd() + _lib_folder

    # Existing path check
    if os.path.exists(_lib_folder):

        entries = os.listdir(_lib_folder)
        library : LinkedList[Document] = linkedlist.empty()

        # Access to documents
        for doc in entries:

            with open(_lib_folder + doc, 'r') as file_readable:
                content : LinkedList[String] = linkedlist.empty()
                for line in file_readable.readlines():
                    content = linkedlist.foldr(linkedlist.cons,
                            content,
                            linkedlist.lmap(algo1.lower,
                            linkedlist.lmap(select_letters,
                            linkedlist.concatmap(lambda s:
                                linkedlist.str_split(s, "-"),
                            linkedlist.str_split(String(line), " ")))))


                title = title_normalize(String(doc))
                new_doc : Document = Document(title, content)

            print("Loading: ", doc)
            library = linkedlist.cons(new_doc, library)

        print("Loading Complete")

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

def select_letters(_string : String) -> String:
    """ remove non-letters """

    chars : LinkedList[str] = linkedlist.lfilter(
            lambda c: c in string.ascii_letters,
            linkedlist.from_string(_string))

    ret : String = String("F" * linkedlist.length(chars))

    idx = 0
    while not chars.content is None:
        # ret = algo1.concat_string(ret, String(chars.content[0]))
        ret[idx] = chars.content[0][0]

        chars = chars.content[1]
        idx = idx + 1

    return ret





if __name__ == '__main__':
    main()
