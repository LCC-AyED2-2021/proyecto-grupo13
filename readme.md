A virtual library of documents with querying capabilities.

# Documentation

```
usage: personal_library.py [-h] [--create] [--search SEARCH] lib

positional arguments:
  lib              Where to store/search for files

optional arguments:
  -h, --help       show this help message and exit
  --create         Create a document
  --search SEARCH  Search a term
```

# Details

## Loading

```
python personal_library.py -create <local_path>
```

It shows:

```
Title: ?
Example title.

Content: ?
Example content.
```

### Details

The destination folder is flat. I.e. it has no sub-folders.

It has to persist the document in the file system.

* Avoid overwrite. At least ask.

### Default Library

Load some documents and save them to the repo.

## Querying

### Research

[Tfidf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)

Possibly, hash from word to a list document and the weights.

```
python personal_library.py --search word

* Index everything. O(d*lg)
	For each file: count word frequency.
	Save in the table (tfidf)

* Find the query in the table:
	Compute the ranking.
	Sort.
	Show.
```

## Future

```
python personal_library.py -search <query> --sort
```
