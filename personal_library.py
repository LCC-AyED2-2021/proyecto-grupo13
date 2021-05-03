"""
A virtual library of documents with querying capabilities.
"""
#pylint: disable=too-few-public-methods,no-else-return

class Document:
    """ The document representation """
    def __init__(self,
            _title : str):
        self.title = _title

def main():
    """ The entry point """
    print("Hello, World!")

if __name__ == '__main__':
    main()
