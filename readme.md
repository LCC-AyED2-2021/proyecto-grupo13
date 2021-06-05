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

## Example run

```
$ python personal_library.py books --search Fox

Searching: Fox
Relevance	id	title
0.028985507246376812	216	The Wolf, the Fox, and the Ape
0.026041666666666668	251	The Eagle and the Fox
0.02564102564102564	52	The Farmer and the Fox
0.022099447513812154	44	The Fox and the Woodcutter
0.02040816326530612	271	The Lion and the Fox
0.0189873417721519	69	The Lion, the Fox, and the Ass
0.017543859649122806	311	The Fox and the Crane
0.016129032258064516	122	The Bear and the Fox
0.015873015873015872	234	The Quack Frog
0.015789473684210527	235	The Lion, the Wolf, and the Fox
0.015625	39	The Wild Boar and the Fox
0.014925373134328358	243	The Ass in the Lion’s Skin
0.014285714285714285	256	The Jackdaw and the Fox
0.013513513513513514	77	The Crab and the Fox
0.013333333333333334	212	The Dog, the Cock, and the Fox
0.013215859030837005	131	The Fox and the Goat
0.012048192771084338	106	The Fox and the Monkey
0.011627906976744186	155	The Lion, the Mouse, and the Fox
0.00980392156862745	43	The Swollen Fox
0.009259259259259259	125	The Ass, the Fox, and the Lion
0.00819672131147541	194	The Fox and the Crow
0.008064516129032258	167	The Fox and the Monkey
0.007575757575757576	83	The Bowman and Lion
0.007462686567164179	117	The Hare and the Tortoise
0.006493506493506494	138	The Sick Lion

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
