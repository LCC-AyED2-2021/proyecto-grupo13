import def_persist
import algo1
import random
from linkedlist import LinkedList
import linkedlist

def main():

    ################################## Print Array
    arr = algo1.Array(10, 0)
    for _ in range(10):
        arr[_] = random.randint(10,60)
    print("Array type")
    print(arr)
    print(type(arr))
    # Saving
    with open('data_array.def', 'w') as file:
        def_persist.save(arr, file)

    # Opening
    with open('data_array.def', 'r') as file:
        arr = def_persist.load(file)
    print("Reading")
    print(arr)
    print(type(arr))

    ################################## Print String
    st = algo1.String("This a test of DEFs module")
    print("\nString type")
    print(st)
    print(type(st))

    # Saving
    with open('data_string.def', 'w') as file:
        def_persist.save(st, file)

    # Opening
    with open('data_string.def', 'r') as file:
        st = def_persist.load(file)
    print("Reading")
    print(st)
    print(type(st))

    ################################# Print LinkedList
    print("\nLinkedList type")
    linked : LinkedList = linkedlist.empty()
    for _ in range(10):
        linked = linkedlist.cons(random.randint(10,60), linked)

    print_linkedlist(linked)
    print(type(linked))

    # Saving
    with open('data_linkedlist.def', 'w') as file:
        def_persist.save(linked, file)

    # Opening
    with open('data_linkedlist.def', 'r') as file:
        linked = def_persist.load(file)
    print("Reading")
    print_linkedlist(linked)
    print(type(linked))

def print_linkedlist(_linkedlist):
    print("[",end='')
    for _ in range(linkedlist.length(_linkedlist)):
        assert not _linkedlist.content is None
        head = _linkedlist.content[0]
        tail = _linkedlist.content[1]
        print(head,end=',')
        _linkedlist = tail
    print(']')

if __name__ == '__main__':
    main()
