# Paquete algo1.py 
# jue oct 12 13:26:46 ART 2017
# Algoritmos y Estructuaras de datos I
# Funciones de carga de valores

#pylint: disable=too-few-public-methods, invalid-name

from typing import TypeVar, Generic, Callable, List
from linkedlist import LinkedList
import linkedlist
import functools

import copy
def input_int( str ):
	try:
		ingreso=int(float(input( str )))
	except:
		ingreso=0
	return ingreso

def input_real( str ):
	try:
		ingreso=float(input( str ))
	except:
		ingreso=0.0
	return ingreso

def input_str( str ):
	try:
		ingreso=input( str )
	except:
		ingreso=""
	return ingreso

V = TypeVar('V')

# Clase arreglos
class Array(Generic[V]):
    """ Hell on Mars """
    data : List[V] =[]
    def __init__(self,size=None,init_value=0):
        if size is None:
            self.size=0
        else:
            self.size=size
            if isinstance(init_value, Array):
                self.data= [copy.deepcopy(None) for i in range(0,size)]
            else:
                self.data= [copy.deepcopy(init_value) for i in range(0,size)]
            self.type = type(init_value)

    def __getitem__(self,index):
        if index > self.size:
            raise Exception("IndexError: index Out of bounds")

        return self.data[index]
    def __setitem__(self,index,value):
        if index > self.size:
            print ("IndexError: index Out of bounds")
            #elif type(value) != self.type and value!=None:
            #        print ("TypeError: value error")
        else:
            self.data[index]=value
    def __str__(self):
        return str([self.data[i] for i in range(0,len(self.data))])

    def __len__(self):
        return self.size

@functools.total_ordering
class String:
    """Hell on Earth"""
    def __init__(self,string):
        self.arr=Array(len(string),'c')
        self.arr.data=string

    def __getitem__(self,index):
        return self.arr[index]

    def __setitem__(self,index,value):
        self.arr[index]=value

    def __str__(self):
        return str(self.arr.data)

    def __len__(self):
        return len(self.arr)

    def __lt__(self, other):
        return self.arr.data < other.arr.data

    def __eq__(self, other):
        return self.arr.data == other.arr.data

def strlen(_s : String) -> int:
    """ The length """
    return len(_s)

def substr(t : String ,start : int,end : int):
    """ A substring """
    assert start >= 0
    assert end >= 0
    return String(''.join([t[i] for i in range(start,end)] ))

# O(t+1). Donde t es la cantidad de caracteres que matchearon y 1 es para el caso de t=0
def strcmp(t : String ,p : String):
    """ Compare strings """
    for i in range(strlen(p)):
        if t[i] != p[i]:
            return False
    return True

# O(|s|)
def concat(s,c):
    """ Concatenate """
    return String(s.arr.data+c)

# O(|s|)
def concat_string(_s: String, _c : String) -> String:
    """ Concatenate """
    return String(_s.arr.data+_c.arr.data)

def is_letter(_code : int) -> bool:
    """ Detect letter """
    lower : bool = _code >= 65 and _code <= 90
    upper : bool = _code >= 97 and _code <= 122
    space_lowdash : bool = _code == 95 or _code == 32
    if lower or upper or space_lowdash:
        return True
    return False

def delete_symbols(_name: String) -> String:
    """ Delete symbols (except '_' and ' ') """

    new_name : String = String('')
    code : int

    for _ in range(strlen(_name)):
        code = ord(_name[_])
        if is_letter(code):
            new_name = concat(new_name, _name[_])
    return new_name

def strip(_name: String) -> String:
    """ Delete first and last ' '. Clean multiple ' ' """

    spaces : int = 0
    status : bool = True
    new_name : String = String('')

    for _ in range(strlen(_name)):
        if status:
            if _name[_] != ' ':
                new_name = concat(new_name, _name[_])
                status = False
        else:
            if _name[_] != ' ':
                if spaces != 0:
                    new_name = concat(new_name, ' ')
                    spaces = 0
                new_name = concat(new_name, _name[_])
            else:
                spaces += 1
    return new_name

def split(_text: String, _limit : str) -> LinkedList[String]:
    """ Return words in LinkedList. """

    words : LinkedList = linkedlist.empty()
    init : int = 0
    end : int = 0

    for _ in range(strlen(_text)):
        if _text[_] == _limit:
            if init != end:
                words = linkedlist.cons(substr(_text, init, end), words)
            init = end + 1
        end += 1
    if init != end:
        words = linkedlist.cons(substr(_text, init, end), words)
    return words

def join(_words : LinkedList[String], _union : str) -> String:
    """ Joins words with _union character """

    text : String = String('')

    for _ in range(linkedlist.length(_words)):
        assert not _words.content is None
        head = _words.content[0]
        tail = _words.content[1]
        #head tiene el primer elemento
        text = concat_string(text, head)
        text = concat(text, _union)
        # tail tiene el resto de la lista
        _words = tail
    return substr(text, 0, strlen(text)-1)

def join_space(_name: String, _union: str) -> String:
    """ Join character in ' ' """

    new_name : String = String('')

    for _ in range(strlen(_name)):
        if _name[_] == ' ':
            new_name = concat(new_name, _union)
        else:
            new_name = concat(new_name, _name[_])
    return new_name

def lower(_name: String) -> String:
    """ Convert to lowercase """

    code : int
    new_name : String = String('')

    for _ in range(strlen(_name)):
        code = ord(_name[_])
        if 65 <= code <= 90:
            code += 32
        new_name = concat(new_name, chr(code))
    return new_name
