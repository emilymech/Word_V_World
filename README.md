# Word_V_World

## Background

This is a new project that uses Wikipedia as a corpus from which to extract word co-occurrences. These co-occurrences will later be utilized as experimental stimuli to understand how regularities in language interact with our knowledge about regularities in the world.


## To-do

* better documentation of how corpora were generated
    * move some of the important variables from the wiki-extractor code to params.py
    * add other important variables related to corpus processing to params.py
* add script that combines output files created by multiple machines with same params to form a single corpus
* do not save bodies.txt to shred drive during job - do only after job completed
 
## Running the script

The corpus-creation is computationally expensive and is designed to be run iin parallel across multiple machines.
To do so, ```ludwigcluster``` is used. 
Jobs are submitted by invoking the its command line interface:

```
ludwig -r 1 -c data/ wikiExtractor/
```

The ```-r``` flag indicates how many times to run a job on each ```ludwigcluster``` machine. This should always be set to 1. 
The ```-c``` flag ensures that all required data folders and source code folders are uploaded to each machine.
Third-party code for Wikipedia-template expansion, available at [/wikiExtractor](../blob/master/wikiExtractor), is not part of source code folder, and therefore must be uploaded explicitly. 
Source code that is in a folder with a name that is equivalent to the name of the root folder will be uploaded to each machine automatically.
Note that folders specified by the ```-c``` flag are not uploaded to each machine, but are uploaded to the remote root folder (on the shared drive), which is accessible by each machine.
Python processes started by ```ludwigcluster``` can import modules found on the remote root folder because it is automatically appended to ```sys.path```.

Note that ```-c data/ wikiExtractor/``` must only be specified once, and can be omitted on subsequent calls to save time. 
Don't forget to specify ```-c data/ wikiExtractor/``` when changes to files in either folder have been made. 

## Technical Notes

Tested on Ubuntu 16.04 and MacOs using Python=>3.6.