# Paquete algo1.py 
# jue oct 12 13:26:46 ART 2017
# Algoritmos y Estructuaras de datos I
# Funciones de carga de valores

#pylint: disable=too-few-public-methods, invalid-name

from typing import TypeVar, Generic, Callable, List
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

        for (idx, _) in enumerate(string):
            self.arr[idx] = string[idx]

    def __getitem__(self,index):
        return self.arr[index]

    def __setitem__(self,index,value):
        self.arr[index]=value

    def __str__(self):
        return ''.join(self.arr.data)

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
# def wrong_concat(s,c):
#     """ Concatenate """
#     return String(s.arr.data+c)

# O(|s|)
def concat_string(_s: String, _c : String) -> String:
    """ Concatenate """
    return String(_s.arr.data+_c.arr.data)

def is_letter(_code : int) -> bool:
    """ Detect letter """
    lower : bool = _code >= 65 and _code <= 90
    upper : bool = _code >= 97 and _code <= 122
    #space_lowdash : bool = _code == 95 or _code == 32
    space : bool = _code == 32
    if lower or upper or space:
        return True
    return False

def delete_symbols(_name: String) -> String:
    """ Delete symbols (except '_' and ' ') """

    new_name : String = String('')
    code : int

    for _ in range(strlen(_name)):
        code = ord(_name[_])
        if is_letter(code):
            new_name = concat_string(new_name, String(_name[_]))
    return new_name


def str_strip(_str: String) -> String:
    """ Delete first and last ' '. Clean multiple ' ' """

    start : int = 0

    while _str[start] == ' ' and start < strlen(_str):
        start = start + 1

    end = strlen(_str) - 1

    while end >= start and _str[end] == ' ':
        end = end - 1

    return substr(_str, start, end)

def join_space(_name: String, _union: str) -> String:
    """ Join character in ' ' """

    new_name : String = String('')

    for _ in range(strlen(_name)):
        if _name[_] == ' ':
            new_name = concat_string(new_name, String(_union))
        else:
            new_name = concat_string(new_name, _name[_])
    return new_name

def lower(_str: String) -> String:
    """ Convert to lowercase """

    result : String = String(' ' * strlen(_str))

    for idx in range(strlen(_str)):
        code : int = ord(_str[idx])
        if 65 <= code <= 90:
            code += 32
        result[idx] = chr(code)

    return result
