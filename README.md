# Word_V_World

## Background

This is a new project that uses Wikipedia as a corpus from which to extract word co-occurrences. These co-occurrences will later be utilized as experimental stimuli to understand how regularities in language interact with our knowledge about regularities in the world.


## To-do

* better documentation of how corpora were generated
    * move some of the important variables from the wiki-extractor code to params.py
    * add other important variables related to corpus processing to params.py
    
## Running the script

The corpus-creation is computationally expensive and is designed to be run iin parallel across multiple machines.
To do so, ```ludwigcluster``` is used. 
Jobs are submitted by invoking the its command line interface:

```
ludwig -r 1 -c data/ wikiExtractor/
```

The ```-r``` flag indicates how many times to run a job on each ```ludwigcluster``` machine. This should always be set to 1. 
The ```-c``` flag ensures that all required data and additional source code directories are uploaded to each machine.
Third-party code for Wikipedia-template expansion and preprocessing is available at [/wikiExtractor](../blob/master/wikiExtractor)

## Technical Notes

Tested on Ubuntu 16.04 and MacOs using Python=>3.6.