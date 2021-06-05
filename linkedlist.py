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

def foldr(folder: Callable[[A, B], B], init: B, linked_list: LinkedList[A]) -> B:
    """ foldr """
    if linked_list.content is None:
        return init
    else:
        head = linked_list.content[0]
        tail = linked_list.content[1]
        return folder(head, foldr(folder, init, tail))

def foldl(folder: Callable[[B, A], B], init: B, linked_list: LinkedList[A]) -> B:
    """ foldl """
    if linked_list.content is None:
        return init
    else:
        head = linked_list.content[0]
        tail = linked_list.content[1]
        return foldl(folder, folder(init, head), tail)

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
            finish = empty()

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
    def max_folder(a: float, acc: Optional[float]) -> Optional[float]:
        if acc is None:
            return a
        else:
            if a > acc:
                return a
            else:
                return acc

    return foldr(max_folder, None, linked_list)

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

def main() -> None:
    """ main """
