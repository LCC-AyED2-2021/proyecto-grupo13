"""
persist module
Serialization readable for humans
Class:
    Array
    String
    LinkedList
    Document
    Dic
    TfidfRow
"""

# Import Class
import algo1
from algo1 import Array, String

import linkedlist
from linkedlist import LinkedList

from personal_library import Document, TfidfRow
from libdic import Dic

import typing

# TextIOWrapper
class Extractor:
    def __init__(self,
            _class : str = '',
            _subclass : str = None,
            _length : int = None,
            _value : str = None):

        self.mclass = _class
        self.subclass = _subclass
        self.length = _length
        self.value = _value

###############################################################################
## Dump objects
###############################################################################

def save(_object, _file, _hierarchy : str = '') -> None:
    """ Dump in file """

    typ = object_type(_object)
    if typ == 'Array':
        save_array(_object, _file, _hierarchy)
    elif typ == 'String':
        save_string(_object, _file, _hierarchy)
    elif typ == 'LinkedList':
        save_linkedlist(_object, _file, _hierarchy)
    elif typ == 'Document':
        save_document(_object, _file, _hierarchy)
    elif typ == 'Dic':
        save_dic(_object, _file, _hierarchy)
    elif typ == 'TfidfRow':
        save_tfidfrow(_object, _file, _hierarchy)
    elif typ == 'function':
        save_function(_object, _file, _hierarchy)

    # Only used when an _object contains multiple types
    elif typ == 'int':
        save_int(_object, _file, _hierarchy)
    elif typ == 'str':
        save_str(_object, _file, _hierarchy)
    elif typ == 'float':
        save_str(_object, _file, _hierarchy)

def object_type(_object) -> str:
    """ Return object type of _object """

    def extract_type(_class : str) -> str:
        """ Return class """

        length : int = (len(_class))
        for _ in range(length-3, -1, -1):
            if _class[_] == "." or _class[_] == "'":
                return _class[_+1:length-2]

    return extract_type(str(type(_object)))

def header(_type : str, _subtype : str = '', _hierarchy : str = '', _length : int = None) -> str:
    """ Construct class head """

    temp_title : str = '!pyObj<'+_type+'>{'+_subtype+'}'
    if len(_hierarchy) == 0:
        if _length != None:
            return temp_title+'{'+str(_length)+'}\n'
        return temp_title+'\n'

    spaces : str = ''
    for _ in range(len(_hierarchy)-2):
        spaces += ' '
    if _length != None:
        return spaces+'- '+temp_title+'{'+str(_length)+'}\n'
    return spaces+'- '+temp_title+'\n'


def footer(_type : str, _hierarchy : str = '') -> str:
    """ Construct class foot """

    spaces : str = ''
    if len(_hierarchy) == 0:
        return '!pyEnd<'+_type+'>\n'
    for _ in range(len(_hierarchy)-2):
        spaces += ' '
    return spaces+'- '+'!pyEnd<'+_type+'>\n'

def is_recursive_type(_type : str) -> bool:
    """ Return False if type is int, str, float """

    if _type == 'int' or _type == 'float' or _type == 'str':
        return False
    return True

def save_int(_object : int, _file, _hierarchy : str) -> None:
    """ Serialization for int """

    _file.write(header('int', _hierarchy = _hierarchy))
    _file.write(_hierarchy+'- '+str(_object)+'\n')
    _file.write(footer('int', _hierarchy))

def save_float(_object : float, _file, _hierarchy : str) -> None:
    """ Serialization for float """

    _file.write(header('float', _hierarchy = _hierarchy))
    _file.write(_hierarchy+'- '+str(_object)+'\n')
    _file.write(footer('float', _hierarchy))

def save_str(_object : str, _file, _hierarchy : str) -> None:
    """ Serialization for str """

    _file.write(header('str', _hierarchy = _hierarchy))
    _file.write(_hierarchy+'- '+_object+'\n')
    _file.write(footer('str', _hierarchy))

def save_function(_object, _value : int, _file, _hierarchy : str) -> None:
    """ Serialization for method """

    _file.write(header('function', _hierarchy = _hierarchy))
    # _file.write(_hierarchy+'- '+_object+'\n')
    _file.write(_hierarchy+'- '+str(_value)+'\n')
    # Could can add name of module and function but, how detect it?
    _file.write(footer('function', _hierarchy))

def save_array(_object : Array, _file, _hierarchy : str) -> None:
    """ Serialization for Array """

    subtype = object_type(_object[0])
    _file.write(header('Array', subtype, _hierarchy, len(_object)))

    if is_recursive_type(subtype):
        for _ in range(len(_object)):
            save(_object[_], _file, _hierarchy+'  ')
    else:
        for _ in range(len(_object)):
            _file.write(_hierarchy+'- '+str(_object[_])+'\n')
    _file.write(footer('Array', _hierarchy))

def save_string(_object : String, _file, _hierarchy : str) -> None:
    """ Serialization for String """

    #Only saves one line string
    _file.write(header('String', 'str', _hierarchy))
    _file.write(_hierarchy+'- ')
    for _ in range(len(_object)):
        _file.write(str(_object[_]))
    _file.write('\n')
    _file.write(footer('String', _hierarchy))

def save_linkedlist(_object : LinkedList, _file, _hierarchy : str) -> None:
    """ Serialization for LinkedList """

    length = linkedlist.length(_object)
    subtype = object_type(_object.content[0])
    _file.write(header('LinkedList', subtype, _hierarchy, length))

    if is_recursive_type(subtype):
        for _ in range(length):
            assert not _object.content is None
            head = _object.content[0]
            tail = _object.content[1]
            save(_object.content[0], _file, _hierarchy+'  ')
            _object = tail
    else:
        for _ in range(length):
            assert not _object.content is None
            head = _object.content[0]
            tail = _object.content[1]
            _file.write(_hierarchy+'  '+'- '+str(head)+'\n')
            _object = tail

    _file.write(footer('LinkedList', _hierarchy))

def save_dic(_object : Dic, _file, _hierarchy : str) -> None:
    """ Serialization for Dic """

    # Multiple subtypes
    _file.write(header('Dic', _hierarchy = _hierarchy))
    save(_object.size, _file, _hierarchy+'  ')
    #save(_object.hash_function, _file, _hierarchy+'  ')
    save_function(_object.hash_function, _object.size, _file, _hierarchy+'  ')
    save(_object.table, _file, _hierarchy+'  ')
    _file.write(footer('Dic'))


def save_document(_object : Document, _file, _hierarchy : str) -> None:
    """ Serialization for Document """

    # Multiple subtypes
    _file.write(header('Dictionary', _hierarchy = _hierarchy))
    save(_object.title, _file, _hierarchy+'  ')
    save(_object.content, _file, _hierarchy+'  ')
    save(_object.uuid, _file, _hierarchy+'  ')
    save(_object.directory, _file, _hierarchy+'  ')
    _file.write(footer('Dictionary'))


def save_tfidfrow(_object : TfidfRow, _file, _hierarchy : str) -> None:
    """ Serialization for TfidfRow """

    _file.write(header('TfidfRow', object_type(_object.row), _hierarchy))
    save(_object.row, _file, _hierarchy+'  ')
    _file.write(footer('TfidRow'))

###############################################################################
## Load objects
###############################################################################

def load(_file):
    """ Wrapper for rec_load """
    return rec_load(_file, data_extractor(_file.readline()))

def rec_load(_file, _data : Extractor):
    """ Load and return object """

    if _data.mclass == 'Array':
        return load_array(_file, _data)
    elif _data.mclass == 'String':
        return load_string(_file, _data)
    elif _data.mclass == 'LinkedList':
        return load_linkedlist(_file, _data)
    elif _data.mclass == 'Document':
        return load_document(_file, _data)
    elif _data.mclass == 'Dic':
        return load_dic(_file, _data)
    elif _data.mclass == 'TfidfRow':
        return load_tfidfrow(_file, _data)
    elif _data.mclass == 'function':
        return load_function(_file, _data)

    #Only used when an _object contains multiple types
    elif _data.mclass == 'int':
        return load_int(_file, _data)
    elif _data.mclass == 'float':
        return load_float(_file, _data)
    elif _data.mclass == 'str':
        return load_str(_file, _data)

def data_extractor(_line : str) -> Extractor:
    """ Extracts data from line of the file"""

    def extract_class(_line : str, _ : int):
        """ Extract class """

        data : Extractor = Extractor()
        init : int = _
        for _ in range(init, len(_line)):
            if _line[_] == '<':
                __ = _ + 1
            elif _line[_] == '>':
                data.mclass = _line[__:_]
            elif _line[_] == '{':
                __ = _ + 1
            elif _line[_] == '}':
                if data.subclass == None:
                    data.subclass = _line[__:_]
                else:
                    data.length = int(_line[__:_])
        return data

    def extract_value(_line : str, _ : int):
        """ Extract value or class """

        if _line[_] == '!':
            return extract_class(_line, _)
        return Extractor(_value = _line[_:len(_line)])

    length = len(_line)
    for _ in range(length):
        if _line[_] == '!':
            return extract_class(_line, _)
        elif _line[_] == '-':
            return extract_value(_line, _+2)

def native_type(_string : str, _type : str):
    """ Convert string in _type """

    if _type == 'int':
        return int(_string)
    if _type == 'float':
        return float(_string)
    if _type == 'str':
        return _string

def load_int(_file, _data : Extractor, _hierarchy : str = '') -> int:
    """ Return int type """

    value : int = int(data_extractor(_file.readline()).value)
    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return value

def load_float(_file, _data : Extractor, _hierarchy : str = '') -> float:
    """ Return float type """

    value : float = float(data_extractor(_file.readline()).value)
    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return value

def load_str(_file, _data : Extractor, _hierarchy : str = '') -> str:
    """ Return str type """

    value : str = data_extractor(_file.readline()).value
    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return value

def load_function(_file, _data : Extractor, _hierarchy : str = ''): # -> ?
    """ Return function string_hash_function """

    value : str = data_extractor(_file.readline()).value
    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return string_hash_function(int(value))

def load_array(_file, _data : Extractor, _hierarchy : str = '') -> Array:
    """ Return Array object """

    def load_native_types(_file, _data : Extractor):
        """ Create Array of _type and loads values """

        array : Array = algo1.create_array(_data.length, _data.subclass)
        for _ in range (_data.length):
            line = data_extractor(_file.readline())
            array[_] = native_type(line.value, _data.subclass)
        assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
        return array


    if is_recursive_type(_data.subclass):
        array : Array = algo1.create_array(_data.length, _data.subclass)
        for _ in range(_data.length):
            array[_] = rec_load(_file, data_extractor(_file.readline()))
        assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
        return array

    else:
        return load_native_types(_file, _data)

def load_string(_file, _data : Extractor) -> String:
    """ Return String object """

    line : Extractor = data_extractor(_file.readline())
    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return String(line.value[0:len(line.value)-1]) # Delete '\n'

def load_linkedlist(_file, _data : Extractor) -> LinkedList:
    """ Return LinkedList object """

    def load_native_types(_file, _data : Extractor, _deep : int = 0) -> LinkedList:
        """ Recursive function for loading a linkedlist with native types """
        if _deep < _data.length-1:
            value = native_type(data_extractor(_file.readline()).value, _data.subclass)
            return linkedlist.cons(value, load_native_types(_file, _data, _deep+1))
        else:
            value = native_type(data_extractor(_file.readline()).value, _data.subclass)
            return linkedlist.cons(value, linkedlist.empty())

    def load_no_native_types(_file, _data : Extractor, _deep : int = 0) -> LinkedList:
        """ Recursive function that calls rec_load """
        if _deep < _data.length-1:
            value = rec_load(_file, data_extractor(_file.readline()))
            return linkedlist.cons(value, load_no_native_types(_file, _data, _deep+1))
        else:
            value = rec_load(_file, data_extractor(_file.readline()))
            return linkedlist.cons(value, linkedlist.empty())

    if is_recursive_type(_data.subclass):
        llist : LinkedList = load_no_native_types(_file, _data)
    else:
        llist : LinkedList = load_native_types(_file, _data)

    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return llist

def load_dic(_file, _data : Extractor) -> Dic:
    """ Return Dic object """

    # There is not subclass for Dic type
    # I should check that the headers are
    # present before assigning them to the attribute

    # Size
    size = rec_load(_file, data_extractor(_file.readline()))

    # Hash Function
    hash_function = rec_load(_file, data_extractor(_file.readline()))

    # Create Dic
    diccionary : Dic = Dic(size, hash_function)

    # Table
    diccionary.table = rec_load(_file, data_extractor(_file.readline()))

    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return diccionary

def load_document(_file, _data : Extractor) -> Document:
    """ Return Document object """

    # There is not subclass for Document type
    # Title
    title : String = rec_load(_file, data_extractor(_file.readline()))

    # Content
    llist : LinkedList = rec_load(_file, data_extractor(_file.readline()))

    # Create Document
    doc : Document = Document(title, llist)

    # Uuid
    doc.uuid : int = rec_load(_file, data_extractor(_file.readline()))

    # directory
    doc.directory : Dic = rec_load(_file, data_extractor(_file.readline()))

    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return doc

def load_tfidfrow(_file, _data : Extractor) -> TfidfRow:
    """ Return TfidfRow object """

    tfidfr : TfidfRow = TfidfRow(rec_load(_file, data_extractor(_file.readline())))
    assert _data.mclass == data_extractor(_file.readline()).mclass, "Error reading the file"
    return tfidfr
