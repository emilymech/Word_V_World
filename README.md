# Word vs. World


This repository contains research code for extracting co-occurrence statistics from Wikipedia articles.
These co-occurrences will later be utilized as experimental stimuli to understand how regularities in language interact with our knowledge about regularities in the world.

## Usage

The input text files are stored on the [UIUC Learning & Language Lab](http://learninglanguagelab.org/) file server.
The Python package `Ludwig` is used to interact with files on the server.
More information about `Ludwig` can be found [here](https://github.com/phueb/Ludwig).

### The corpus as an abstraction

To `Ludwig`, a corpus is an abstraction.
That is, there is no single text file to uniquely identify a Wikipedia corpus.
Instead, a corpus is made up of multiple text files that exist in `research_data/CreateWikiCorpus/runs`.
Moreover, there are multiple corpora saved on the server.
But, each text file is only associated with a single corpus. 

### Retrieving text files
 
So, how are all text files associated with a single corpus retrieved?
This is where a parameter configuration comes in. 
Each text file is co-located with a `param2val.yaml` file, which represents its parameter configuration.
A parameter configuration is simply the set of parameters used to create a single corpus.
Thus, in order to retrieve a single corpus, all text files associated with the same parameter configuration must be retrieved.
The following code retrieves all articles as string objects and saves them in a list called `all_articles`: 

```python
from word_v_world.articles import generate_articles

all_articles = []
for article in generate_articles(paths_to_articles):
    all_articles.append(article)
```

But first, we must define `paths_to_articles` in order to restrict retrieval to articles that belong to a single corpus.
To do so:

```python
from word_v_world.articles import get_paths_to_articles

paths_to_articles = []
for p in get_paths_to_articles(param2requests):
    paths_to_articles.append(p)
```

Notice, that we need to define `param2requests`.
This is a Python dictionary, which represents the unique parameter configuration we are interested in.
It is up to the user to define this object.
The default is:

```python
param2requests = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'num_machines': [7],
                  'input_file_name': ['dummy_input.xml']}
```                      

Putting it all together:

```python
from word_v_world.articles import generate_articles, get_paths_to_articles

param2requests = {'part': [0, 1, 2, 3, 4, 5, 6],
                  'num_machines': [7],
                  'input_file_name': ['dummy_input.xml']}

paths_to_articles = []
for p in get_paths_to_articles(param2requests):
    paths_to_articles.append(p)
    
all_articles = []
for article in generate_articles(paths_to_articles):
    all_articles.append(article)
```

## Usage

on MacOs

```bash
ludwig -mnt /Volumes/research_data -e data
```

In order to successfully execute the above code, a user must have a local copy of [CreateWikiCorpus](https://github.com/UIUCLearningLanguageLab/CreateWikiCorpus), and must point `config.LocalDirs.wiki` to its location.
This is required in order to obtain a a full list of the default parameter configuration used to generate Wikipedia corpora.
This allows the `param2requests` object to be incomplete; the remaining parameters (`keep_tables`, `expand_templates`, etc.) will be set to their default.