import sys
import typing

class ArgumentParser:
    """ The replacement of argparser """

    def __init__(self,
            _arguments : list[str]):

        def error(_required : str) -> None:
            """ Returns error message """

            print('usage: personal_library.py [-h] [--create] [--search SEARCH] lib')
            print('error: the following arguments are required:', end=' ')
            print(_required)

        def add_lib(_is_create : bool) -> None:
            """ Adds args.lib """

            if _is_create:
                if len(_arguments) > 2:
                    self.lib = _arguments[2]
                else: error('lib')
            else:
                if len(_arguments) > 3:
                    self.lib = _arguments[3]
                else: error('lib')

        def add_search():
            """ Adds args.search """
            if len(_arguments) > 2:
                self.search = _arguments[2]
            else: error('SEARCH')

        self.create = None
        self.search = None
        self.lib = None

        if len(_arguments) > 1:
            if _arguments[1] == '--create':
                self.create = '--create'
                self.search = ''
                add_lib(True)
            elif _arguments[1] == '--search':
                self.create = ''
                add_search()
                add_lib(False)
            else: error('--search, --create')
        else: error('ALL')
