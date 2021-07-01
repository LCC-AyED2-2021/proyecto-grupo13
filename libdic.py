""" The dictionary
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

#pylint: disable=too-few-public-methods, invalid-name

from typing import TypeVar, Generic, Callable, Optional, Tuple
import math
from algo1 import Array
from linkedlist import LinkedList
import linkedlist

K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')

class Dic(Generic[K, V]):
    """ The dictionary class """

    def __init__(self,
            _size : int,
            _hash_function : Callable[[K], int]):
        """Creates an empty dictionary. It has all empty lists.
        Pay the price in size."""

        self.table : Array[LinkedList[Tuple[K, V]]] = Array(_size, None)
        for idx in range(_size):
            self.table[idx] = linkedlist.empty()

        self.hash_function = _hash_function
        self.size = _size


def multiplicative_hash_function(_size: int, _spread: float) -> Callable[[int], int]:
    """ Returns multiplicative hash function """

    def hash_func(__key: int) -> int:
        return math.floor(_size * ((__key * _spread) % 1))

    return hash_func

def golden_ratio() -> float:
    """ that number """
    return (math.sqrt(5) - 1) / 2

def insert(_dic : Dic[K, V], _key : K, _value : V) -> Dic[K, V]:
    """ Insert into a dictionary. """

    this_hash = _dic.hash_function(_key)

    _dic.table[this_hash] = linkedlist.insert(_dic.table[this_hash], _key, _value)

    return _dic


def delete(_dic : Dic[K, V], _key : K) -> Dic[K, V]:
    """ Delete a kay from a dictionary """

    this_hash = _dic.hash_function(_key)

    _dic.table[this_hash] = linkedlist.delete(_dic.table[this_hash], _key)

    return _dic


def search(_dic : Dic[K, V], _key : K) -> Optional[V]:
    """ Search a key in the table """

    this_hash = _dic.hash_function(_key)

    return linkedlist.retrieve(_dic.table[this_hash], _key)

def update_with_default(_dic : Dic[K, V],
        _update_function : Callable[[V], V],
        _key : K ,
       _default : V) -> Dic[K, V]:
    """ Update the value at `_key` using `_update_function`. Insert `_default`
    if `_key` is not pressent. """

    this_hash = _dic.hash_function(_key)

    _dic.table[this_hash] = linkedlist.update_with_default(
            _dic.table[this_hash],
            _update_function,
            _key,
            _default)

    return _dic

def assocs(_dic : Dic[K, V]) -> LinkedList[Tuple[K, V]]:
    """ A list of pairs key, value """

    result : LinkedList[Tuple[K, V]] = linkedlist.empty()

    for l in _dic.table.data:
        result = linkedlist.rev_concat(
                linkedlist.lmap(lambda x : x, l),
                result)

    return result

def to_list(_dic : Dic[K, V]) -> LinkedList[V]:
    """ A list of values """
    return linkedlist.lmap(lambda x : x[1], assocs(_dic))

def keys(_dic : Dic[K, V]) -> LinkedList[K]:
    """ The keys """
    return linkedlist.lmap(lambda x : x[0], assocs(_dic))

def includes(_a : Dic[K, V], _b : Dic[K, V]) -> bool:
    """ Wether all the keys of `_b` are included in `_a`
    O(|_b|)
    """

    keys_b = keys(_b)

    return linkedlist.lall(lambda x : not search(_a, x) is None, keys_b)

def dmap(_mapper : Callable[[V], W], _dic : Dic[K, V]) -> Dic[K, W]:
    """ Maps the values """

    retDic : Dic[K, W] = Dic(_dic.size, _dic.hash_function)

    for idx in range(_dic.size):
        retDic.table[idx] = linkedlist.lmap(lambda p: (p[0], _mapper(p[1])),
            _dic.table[idx])

    return retDic

def dic_health(_dic : Dic[K, V]) -> None:
    """ Helath report for a directory """

    print("Size: ", _dic.size)

    collisions : LinkedList[int] = linkedlist.empty()
    for idx in range(_dic.size):
        collisions = linkedlist.cons(
                linkedlist.length(_dic.table[idx]),
                collisions)

    min_collisions = linkedlist.minimum_by(
            lambda x, y: x <= y,
            collisions)

    if not min_collisions is None:
        print("Min collisions: ", min_collisions)

    max_collisions = linkedlist.maximum(
            linkedlist.lmap(float, collisions))

    if not max_collisions is None:
        print("Max collisions: ", max_collisions)

    elements = linkedlist.lsum(collisions)
    print("Elements: ", elements)

    collisions = linkedlist.quick_sort_by(lambda x, y: x <= y,
            collisions)

    median : Optional[int] = linkedlist.index(collisions, _dic.size // 2)

    print("Median: ", median)

    print("Load factor: ", elements / _dic.size)
