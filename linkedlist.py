""" The linkedlist module
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
#pylint: disable=too-few-public-methods,no-else-return,invalid-name
from typing import Generic, TypeVar, Callable, Optional, Tuple

A = TypeVar('A')
B = TypeVar('B')

#class Nil(Generic[A]):
#    """ Empty list """
#
#class Cons(Generic[A]):
#    """ A cons """
#    def __init__(self, head: A, tail: LinkedList[A]):
#        self.head = head
#        self.tail = tail

class LinkedList(Generic[A]):
    """ A list """

    content: Optional[Tuple[A, 'LinkedList[A]']] = None

    def __str__(self):
        if self.content is None:
            return ""
        else:
            try:
                return str(self.content[0]) + "," + str(self.content[1])
            except RecursionError:
                return str(self.content[0]) + ", ..."

def empty() -> LinkedList[A]:
    """ Empty """
    return LinkedList()

def is_empty(linked_list: LinkedList[A]) -> bool:
    """is _empty """
    return linked_list.content is None

def cons(element: A, linked_list: LinkedList[A]) -> LinkedList[A]:
    """ Cons """
    ret: LinkedList[A] = LinkedList()
    ret.content = (element, linked_list)
    return ret

def singleton(a: A) -> LinkedList[A]:
    """ A singleton """
    return cons(a, empty())

def foldr(_folder: Callable[[A, B], B], _init: B, _linked_list: LinkedList[A]) -> B:
    """ foldr """
    if _linked_list.content is None:
        return _init
    else:
        head = _linked_list.content[0]
        tail = _linked_list.content[1]
        return _folder(head, foldr(_folder, _init, tail))

def foldl(_folder: Callable[[B, A], B], _init: B, _linked_list: LinkedList[A]) -> B:
    """ foldl """

    # PSEUDO PYTHON

    # if _linked_list.content is None:
    #     return _init

    #head = linked_list.content[0]
    #tail = linked_list.content[1]
    #return foldl(folder, folder(init, head), tail)

    # What follows is no longer pseudo-python
    # We lift circunvent real python maximum rec depth

    cursor = _linked_list
    result = _init
    while not cursor.content is None:
        result = _folder(result, cursor.content[0])
        cursor = cursor.content[1]

    return result




def lmap(mapper: Callable[[A], B], linked_list: LinkedList[A]) -> LinkedList[B]:
    """ maps """
    if linked_list.content is None:
        return empty()
    else:
        head = linked_list.content[0]
        tail = linked_list.content[1]

        try:
            return cons(mapper(head), lmap(mapper, tail))
        except RecursionError:
            rest = tail
            finish : LinkedList[B] = empty()

            while not rest.content is None:
                rhead = rest.content[0]
                rest = rest.content[1]
                finish = cons(mapper(rhead), finish)

            return cons(mapper(head), finish)

def land(linked_list: LinkedList[bool]) -> bool:
    """ all true """
    return foldr(lambda x, y: x and y, True, linked_list)

def reverse(linked_list: LinkedList[A]) -> LinkedList[A]:
    """ reverses """
    return foldr(cons, empty(), linked_list)

def maximum(linked_list: LinkedList[float]) -> Optional[float]:
    """ return the maximum """
    def max_folder(acc: Optional[float], a: float) -> Optional[float]:
        if acc is None:
            return a
        else:
            if a > acc:
                return a
            else:
                return acc

    return foldl(max_folder, None, linked_list)

def concatenate(linked_list_a: LinkedList[A], linked_list_b: LinkedList[A]) -> LinkedList[A]:
    """ concatenate """
    return foldr(cons, linked_list_b, reverse(linked_list_a))

def elem(a: A, linked_list: LinkedList[A]) -> bool:
    """ true if a in linked_list """
    return foldr(lambda x, y: x == a or y, False, linked_list)

def unique(linked_list: LinkedList[A]) -> LinkedList[A]:
    """ all unique elements """
    def uniq_folder(element: A, acc: LinkedList[A]) -> LinkedList[A]:
        if elem(element, acc):
            return acc
        else:
            return cons(element, acc)

    return foldr(uniq_folder, empty(), linked_list)

def length(linked_list: LinkedList[A]) -> int:
    """ the length """

    return foldr(lambda _, y: y + 1, 0, linked_list)

def lzip(linked_list_a: LinkedList[A], linked_list_b: LinkedList[A]) -> LinkedList[Tuple[A, A]]:
    """ True if all equal """
    def zip_rec(list_a: LinkedList[A], list_b: LinkedList[A]) -> LinkedList[Tuple[A, A]]:
        """ the recursive part"""
        if list_a.content is None or list_b.content is None:
            return empty()

        head_a = list_a.content[0]
        tail_a = list_a.content[1]
        head_b = list_b.content[0]
        tail_b = list_b.content[1]

        return cons((head_a, head_b), zip_rec(tail_a, tail_b))

    return zip_rec(linked_list_a, linked_list_b)

def lenumerate(n_elements: int) -> LinkedList[int]:
    """1, 2, 3, ... """
    assert n_elements >= 0
    if n_elements == 0:
        return empty()
    else:
        return cons(1, lmap(lambda x: x + 1, lenumerate(n_elements - 1)))

def eq(linked_list_a: LinkedList[A], linked_list_b: LinkedList[A]) -> bool:
    """ true if all equal """
    return foldr(lambda x, y: x[0] == x[1] and y, True, lzip(linked_list_a, linked_list_b))

def from_array(arr):
    """ Create a list from an array"""
    ret = empty()

    for idx in range(len(arr)):
        ret = cons(arr[len(arr) - 1 - idx], ret)

    return ret

def lall(predicate : Callable[[A], bool], linked_list : LinkedList[A]) -> bool:
    """ all elements of linked_list satisfy predicate """
    if linked_list.content is None:
        return True
    else:
        head = linked_list.content[0]
        tail = linked_list.content[1]
        return predicate(head) and lall(predicate, tail)

def pylist(_linked_list : LinkedList[A] ) -> list[A]:
    """ Convert a linked list to a python list. Used for debuging """
    def pylist_rec(__acc : list[A], __linked_list : LinkedList[A]) -> list[A]:
        if __linked_list.content is None:
            return __acc
        else:
            head = __linked_list.content[0]
            tail = __linked_list.content[1]
            new_acc : list[A] = __acc.copy()
            new_acc.append(head)
            return pylist_rec(new_acc, tail)

    return pylist_rec([], _linked_list)

def lfilter(p : Callable[[A], bool], _linked_list : LinkedList[A] ) -> LinkedList[A]:
    """ Select elements that match p """

    if _linked_list.content is None:
        return empty()
    else:
        head = _linked_list.content[0]
        tail = _linked_list.content[1]

        rest = lfilter(p, tail)

        if p(head):
            return cons(head, rest)
        else:
            return rest


def delete(_linked_list : LinkedList[Tuple[A, B]],
        _key : A) -> LinkedList[Tuple[A, B]]:
    """ Treat a list as a k,v store delete the provided key. O(n) """

    if _linked_list.content is None:
        return empty()

    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    if head[0] == _key:
        return tail
    else:
        return cons(head, delete(tail, _key))

def retrieve(_linked_list : LinkedList[Tuple[A, B]], _key : A) -> Optional[B]:
    """ Treat a list as a k,v store retrive the provided key. O(n) """

    if _linked_list.content is None:
        return None

    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    if head[0] == _key:
        return head[1]
    else:
        return retrieve(tail, _key)

def update_with_default(_linked_list : LinkedList[Tuple[A, B]],
       _update_function : Callable[[B], B],
        _key : A,
       _default : B) -> LinkedList[Tuple[A, B]]:
    """ Update the value at `_key` using `_update_function`. Insert `_default`
    if `_key` is not pressent. """

    if _linked_list.content is None:
        return singleton((_key, _default))

    head = _linked_list.content[0]
    tail = _linked_list.content[1]
    if head[0] == _key:
        return cons((_key, _update_function(head[1])), tail)

    return cons(head, update_with_default(tail
        , _update_function
        , _key
        ,_default))

def insert(_linked_list : LinkedList[Tuple[A, B]]
        , _key : A
        , _value : B) -> LinkedList[Tuple[A, B]]:
    """ Treat a list as a k,v store and update the requested value. O(n) """

    return update_with_default(_linked_list, lambda _ : _value, _key, _value)

    # # Old implementation

    # if _linked_list.content is None:
    #     return singleton((_key, _value))

    # head = _linked_list.content[0]
    # tail = _linked_list.content[1]

    # if head[0] == _key:
    #     # Update the value
    #     return cons((_key, _value), tail)
    # else:
    #     return cons(head, insert(tail, _key, _value))

def rev_concat(_a : LinkedList[A], _b : LinkedList[A]) -> LinkedList[A]:
    """ rev_concat [3,2,1] [4,5,6] = [1,2,3,4,5,6]
    O(length(_a)) """

    if _a.content is None:
        return _b

    head = _a.content[0]
    tail = _a.content[1]

    return cons(head, rev_concat(tail, _b))

def span(predicate : Callable[[A], bool],
        _linked_list : LinkedList[A]) -> Tuple[LinkedList[A], LinkedList[A]]:

    """(a -> Bool) -> [a] -> ([a], [a])

    Breaks the list on the first not satisfaction of the predicate

    span even [2,2,3,4] = ([2,2],[3,4])

    """

    if _linked_list.content is None:
        return (empty(), empty())

    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    (t, f) = span(predicate, tail)

    if predicate(head):
        return (cons(head, t), f)

    return (empty(), cons(head, tail))

def group_count(_linked_list : LinkedList[A]) -> LinkedList[Tuple[A, int]]:
    """ Counts the consecitive ocurrences of elements in the list """

    if _linked_list.content is None:
        return empty()

    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    (t, f) = span(lambda x : x == head, tail)

    return cons((head, length(t) + 1), group_count(f))

def lsum(_linked_list : LinkedList[int]) -> int:
    """ Sums ints """
    return foldl(lambda x, y : x + y, 0, _linked_list)

def partition(_predicate : Callable[[A], bool]
        , _linked_list : LinkedList[A]) -> Tuple[LinkedList[A], LinkedList[A]]:
    """ partitions by the predicate """


    if _linked_list.content is None:
        return (empty(), empty())


    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    (t, f) = partition(_predicate, tail)

    if _predicate(head):
        return (cons(head, t), f)

    return (t, cons(head, f))


def quick_sort_by(_lte : Callable[[A, A], bool],
        _linked_list : LinkedList[A]) -> LinkedList[A]:
    """Sorts a list using quick sort algorithm"""
    # It uses the median pivot technique to have better chances of picking a pivot
    # that is near the median of the list.
    # Eg. The pivot is guaranteed to be the median on a three element list.
    #
    # Having the pivot near the median means the list splist nearly in half.
    # This comes with a slight complexity cost.

    if _linked_list.content is None:
        return empty()

    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    if tail.content is None:
        # A snigleton list
        return singleton(head)

    tail_head = tail.content[0]
    tail_tail = tail.content[1]

    if tail_tail.content is None:
        # Sort a two element list
        if _lte(head, tail_head):
            return cons(head, cons(tail_head, empty()))
        else:
            return cons(tail_head, cons(head, empty()))

    # selects three list positions and search for their values
    # `pivot` has the a value that is in the middle of the three
    # randomly selected. E.g: 1,5,2 -> 2 is the pivot
    # tail_tail has length of at least 1

    # including the two extracted heads
    sample1 = head
    sample2 = tail_head
    sample3 = tail_tail.content[0]

    min_sample : A = sample1 if _lte(sample1, sample2) else sample2
    min_sample = sample3 if _lte(sample3, min_sample) else min_sample

    max_sample : A = sample1 if not _lte(sample1, sample2) else sample2
    max_sample = sample3 if not _lte(sample3, max_sample) else max_sample

    #if (sample1 != min_value) and (sample1 != max_value):
    if sample1 not in (min_sample, max_sample):
        pivot = sample1
    elif sample2 not in (min_sample, max_sample):
        pivot = sample2
    else:
        pivot = sample3

    assert not pivot is None

    (pivots, non_pivots) = partition(lambda x: x == pivot, _linked_list)

    (left, right) = partition(lambda x: _lte(x, pivot), non_pivots)

    return concatenate(
        quick_sort_by(_lte, left),
        concatenate(pivots, quick_sort_by(_lte, right)))

def index(_linked_list : LinkedList[A], idx : int) -> Optional[A]:
    """ The element at index idx """

    assert(idx >= 0)

    if _linked_list.content is None:
        return None

    head = _linked_list.content[0]
    tail = _linked_list.content[1]

    if idx == 0:
        return head

    return index(tail, idx - 1)

def main() -> None:
    """ main """
