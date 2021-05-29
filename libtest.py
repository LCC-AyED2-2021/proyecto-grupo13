""" Test some functions
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
from typing import TypeVar, Generic, Callable, Optional, Tuple

import unittest

import personal_library
from personal_library import Document

import linkedlist
from linkedlist import LinkedList

import libdic
from libdic import Dic

class TestFunctions(unittest.TestCase):
    """ Tests for the personal library functions """

    def test_doc_count_words(self):
        """ Test doc_count_words """
        test_contents : LinkedList[str] = linkedlist.empty()

        for word in ["this", "test", "is", "this"]:
            test_contents = linkedlist.cons(word, test_contents)

        test_doc = Document("A title", test_contents)

        test_count : Dic[str, int] = personal_library.doc_count_words(test_doc)

        self.assertEqual(libdic.search(test_count, "this"), 2)
        self.assertEqual(libdic.search(test_count, "is"), 1)
        self.assertEqual(libdic.search(test_count, "test"), 1)

    def test_doc_tfidf(self):
        """ Thest doc_tfidf """

        Document.uuid = 0

        test_docs : LinkedList[Document] = linkedlist.empty()

        # Create first doc
        test_contents : LinkedList[str] = linkedlist.empty()

        for word in ["shark", "test", "is", "this"]:
            test_contents = linkedlist.cons(word, test_contents)

        test_doc = Document("On Sharks", test_contents)

        test_docs = linkedlist.cons(test_doc, test_docs)

        # Create second doc
        test_contents = linkedlist.empty()

        for word in ["cow", "test", "is", "this"]:
            test_contents = linkedlist.cons(word, test_contents)

        test_doc = Document("On cows", test_contents)

        test_docs = linkedlist.cons(test_doc, test_docs)

        # Create the tfidf
        tfidf = personal_library.doc_tfidf(test_docs)

        # Assert that the word shark has the right row
        shark_result : LinkedList[Tuple[int, float]]= libdic.search(tfidf, "shark")

        self.assertTrue(not shark_result is None)
        assert not shark_result is None
        assert not shark_result.row.content is None

        (uuid, freq) = shark_result.row.content[0]
        tail = shark_result.row.content[1]

        self.assertEqual(uuid, 0)
        self.assertEqual(freq, 1 / 4)
        self.assertTrue(tail.content is None)

        # TODO: test the word "this"


if __name__ == '__main__':
    unittest.main()
