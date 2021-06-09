import def_persist
from algo import Array #para matriz
import algo1
import random
from linkedlist import LinkedList
import linkedlist

def main():

    ################################## Print Array
    arr = algo1.Array(3, 0)
    for _ in range(3):
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

    ################################## Print Matrix
    matrix = Array(2, Array(3,0))
    for _ in range(2):
        for __ in range (3):
            matrix[_][__] = random.randint(10,60)
    print("Array type")
    print(matrix)
    print(type(matrix))
    # Saving
    with open('data_matrix.def', 'w') as file:
        def_persist.save(matrix, file)

    # Opening
    with open('data_matrix.def', 'r') as file:
        matrix = def_persist.load(file)
    print("Reading")
    print(matrix)
    print(type(matrix))

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

    ################################# Print LinkedList[Array]
    print("\nLinkedList type")
    linked : LinkedList = linkedlist.empty()
    for _ in range(5):
        linked = linkedlist.cons(arr, linked)

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
