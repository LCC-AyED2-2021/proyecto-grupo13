"""
def_persist module
Serialization readable for humans
Class:
    Array
    String
    LinkedList
    Dictionary
    Tfidf
"""

# Import Class
from algo1 import Array, String
from linkedlist import LinkedList
import linkedlist
import typing

# TextIOWrapper

def save(_object, _file): #_file is a pointer? or open here?
    """ Dump in file """

    typ = object_type(_object)
    if typ == 'Array':
        save_array(_object, _file)
    elif typ == 'String':
        save_string(_object, _file)
    elif typ == 'LinkedList':
        save_linkedlist(_object, _file)

def object_type(_object):
    """ Return object type of _object """

    def extract(_class : str) -> str:
        """ Return class """

        __ = 0
        for _ in range(len(_class)):
            if _class[_] == ".":
                __ = _ + 1
            elif __ > 0 and _class[_] == "'":
                return _class[__:_]

    return extract(str(type(_object)))

def header(_type : str) -> str:
    """ Write header class """
    return '!!python/object<'+_type+'>\n'

def save_array(_object : Array, _file):
    """ Serialization for Array """

    _file.write(header('Array'))
    for _ in range(len(_object)):
        _file.write(' - '+str(_object[_])+'\n')

def save_string(_object : String, _file):
    """ Serialization for String """

    #Only saves one line string
    _file.write(header('String'))
    for _ in range(len(_object)):
        _file.write(str(_object[_]))

def save_linkedlist(_object, _file):
    """ Serialization for LinkedList """

    _file.write(header('LinkedList'))
    #while _object.content != None:
    for _ in range(linkedlist.length(_object)):
        assert not _object.content is None
        head = _object.content[0]
        tail = _object.content[1]
        _file.write(' - '+str(head)+'\n')
        _object = tail

def load(_file):
    """ Load and return object """

    typ = read_object_type(_file.readline())
    if typ == 'Array':
        return load_array(_file)
    elif typ == 'String':
        return load_string(_file)
    elif typ == 'LinkedList':
        return load_linkedlist(_file)

def read_object_type(_header : str) -> str:
    """ Read object type in first line of file """

    __ = 0
    for _ in range(len(_header)):
        if _header[_] == '<':
            __ = _ + 1
        elif __ > 0 and _header[_] == '>':
            return _header[__:_]

def read_values(_file):
    # We consider that a file only contains one datatype

    def clean(_line : str) -> int:
        return int(_line[2:len(_line)]) # Shouldn't it always return an int!

    values : list = []
    line = _file.readline()
    while line: # if not(line) --> End of file?
        values.append(clean(line))
        line = _file.readline()
    return values

def load_array(_file):
    """ Return Array object """

    values = read_values(_file)
    array : Array = Array (len(values), 0)
    for _ in range(len(values)):
        array[_] = values[_]
    return array

def load_string(_file):
    """ Return String object """

    return String(_file.readline())

def load_linkedlist(_file):
    """ Return LinkedList object """

    values = read_values(_file)
    lkdlist : LinkedList = linkedlist.empty()
    for _ in range(len(values)-1, -1, -1):
        lkdlist = linkedlist.cons(values[_], lkdlist)
    return lkdlist
