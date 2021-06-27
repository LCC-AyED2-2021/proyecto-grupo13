A virtual library of documents with querying capabilities.

# Documentation

```
usage: personal_library.py [-h] [--create FOLDER] [--search TERM]

optional arguments:
  -h, --help       show this help message and exit
  --create FOLDER  Create the index
  --search TERM    Search a term
```

## Example run

```
$ python personal_library.py books --search network

Searching: network
Load index...
string_hash_function
Load directory...
multiplicative_hash_function
Freq	title	relevance
56	reviewtxt_comprehensive_a_classification_text_learningbased_deep	0.0018238144110960361
37	taggingtxt_sequence_for_models_lstmcrf_bidirectional	0.004781216569857937
26	networktxt_neural_convolutional_a_of_understanding	0.005605544850562544
5	prospectstxt_and_perspectives_trends_learning_machine	0.000520068412785073
2	reviewtxt_scientific_a_diabetes_and_health_of_determinants_social	6.359148445504086e-05
1	covidtxt_and_diabetes	0.0008536295327092922

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

## Persistence

We write a module that persists the structures used. It supports:

* Array
* String
* LinkedList
* Dic
* Document

The module saves a file in a plain text format, `*.def`

Determines the class of the object and creates the dump file.

The header contains two subsections:

```
* !!python/object: beginning of a structure.
* <_class_>: type of structure.
```

And two optional subsections:

* `{_subclass_}`: indicates the type contained in the structure
* `{_int_}`: length of the structure.

The footer contains only two subsections:

* `!!python/object`: ending of a structure.
* `<_class_>`: type of structure.

### Examples

Matrix 2x3 in dump file.

```
M =
[49, 18, 44]
[15, 58, 51]

output.def:

!!python/object<Array>{Array}{2}
- !!python/object<Array>{int}{3}
  - 49
  - 18
  - 44
- !!python/end<Array>
- !!python/object<Array>{int}{3}
  - 15
  - 58
  - 51
- !!python/end<Array>
!!python/end<Array>
```

LinkedList[Array].
LinkedList: 5 elements.
Array: 3 elements.

```
L = [[30, 25, 40],[30, 25, 40],[30, 25, 40],[30, 25, 40],[30, 25, 40],]

output.def

!!python/object<LinkedList>{Array}{5}
- !!python/object<Array>{int}{3}
  - 30
  - 25
  - 40
- !!python/end<Array>
- !!python/object<Array>{int}{3}
  - 30
  - 25
  - 40
- !!python/end<Array>
- !!python/object<Array>{int}{3}
  - 30
  - 25
  - 40
- !!python/end<Array>
- !!python/object<Array>{int}{3}
  - 30
  - 25
  - 40
- !!python/end<Array>
- !!python/object<Array>{int}{3}
  - 30
  - 25
  - 40
- !!python/end<Array>
!!python/end<LinkedList>
```

## Future

```
python personal_library.py -search <query> --sort
```

# Acknowledgments

```
The Project Gutenberg EBook of Aesop’s Fables, by Aesop

This eBook is for the use of anyone anywhere at no cost and with
almost no restrictions whatsoever.  You may copy it, give it away or
re-use it under the terms of the Project Gutenberg License included
with this eBook or online at www.gutenberg.org


Title: Aesop’s Fables

Author: Aesop

Translator: George Fyler Townsend

Posting Date: June 25, 2008 [EBook #21]
Release Date: September 30, 1991
Last Updated: October 28, 2016

Language: English

Character set encoding: UTF-8
```
