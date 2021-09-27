# MetDisKG
*Metadata Disambiguation for Knowledge Graphs*

MetDisKG is a framework to disambiguate metadata to insert it into a knowledge graph. It can extract metadata from a given dataset and disambiguate it. The framework uses two different methods to disambiguate the given metadata. The first method compares the metadata with data from an external resource to disambiguate it. The second method uses the given features of the metadata to disambiguate it. The result of the application of the framework to a given dataset of metadata is disambiguated metadata which can be inserted into a knowledge graph. 

# Requirements
- Python 3.8.10 or above
- Libarys used:
  - ``` import pandas ```
  - ``` import requests ```
  - ``` import pyorcid ```
  - ``` from nameparser import HumanName ```
  - ``` import logging ```
  - ``` import time ```
  - ``` import json ```
  - ``` from _collection_abc import Iterable ```

# How to use the framework
Every step of using the framework will be explained in the coming sections
## Give a dataset
### Requirements for the dataset
- metadata about autornames and titels of their publications
- dataset has to be a csv file

Let the framework read the csv file with:
```
data = pd.read_csv('NameOfFile.csv', sep=',', engine='python')
```
- Note that the seperator can be modified to the seperator which is used in the csv file (usually , or ; )

## Disambiguate the metadata
The framework will automatically disambiguate the given metadata. For every intermediate step in the process of disambiguation a csv file with the intermediate results will be generated. The intermediate results are:
- For autorname disambiguation:
  1. A dataframe of authors and their corresponding titles ```auttitle.csv```
  2. A dataframe of the first batch of disambiguated authors ```ergebnisorcid1.csv```
  3. A dataframe of the second batch of disambiguated authors ```ergebnisorcid2.csv```
  4. A dataframe of the third batch of disambiguated authors ```ergebnisorcid3.csv```
- The result of the disambiguation is also saved in a csv file ```ergebnisorcid.csv```

- The result of the disambiguation of institution names is saved in a csv file ```rorerg.csv```

## TODO
- [ ] Test the disambiguation of metadata based on the given features 

## Licensing
- This framework uses the nameparser library as a library and does not change the library in any way.
- This framework used a subset of the TRY-Initative dataset of publication CC-BY TRY Creative Commons Attribution
