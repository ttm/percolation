# percolation
the percolation python package for harnessing open linked social data

## core features

    - Provide routines for percolation in social systems by experiments and processes.
    - Ease knowledge about the networked self.
    - Analyses of social systems through textual, topological, temporal statistics within a typology framework of agents and networks.
    - Art and games from social structures, such as music and animation.
    - Integration of resources through RDF data and OWL ontologies.
    - Cross provenance resource recommendation, extending facilities from the Participation package.
    - WWW integration to provide data and media.

## install with:

    $ pip install percolation

or

    $ python setup.py install

For greater control of customization (and debugging), clone the repo and install with pip with -e:

    $ git clone https://github.com/ttm/percolation.git
    $ pip install -e <path_to_repo>

This install method is especially useful when reloading modified module in subsequent runs of percolation
(usually with the standard importlib).

Percolation uses social, music and visuals packages to enable anthropological physics experiments and social harnessing:

  - https://github.com/ttm/social
  - https://github.com/ttm/music
  - https://github.com/ttm/visuals

See this deprecated document for some of the intended goals:

  - https://github.com/ttm/percolationlegacy/blob/master/latex/percolation-article.pdf


## coding conventions

A function name has a verb if it changes state of initialized objects, if it only "returns something", it is has no verb in name.

Classes, functions and variables are writen in CamelCase, headlessCamelCase and lowercase, respectively. Underline is used only in variable names where the words in variable name make something unreadable (usually because the resulting name is big).

The code is the documentation. Code should be very readable to avoid writing unnecessary documentation and duplicating routine representations. This adds up to using docstrings to give context to the objects or omitting the docstrings.

The usual variables in scripts are: P for percolation, NS for P.rdf.NS for namespace, a for NS.rdf.type, c for P.utils.check, S for social, M for music, V for visuals, n for numpy, p for pylab, r for rdflib, x for networkx

The file cureimport.py in newtests avoids cluttering the header of the percolation file while hacking framework. In using the Python interpreter, subsequent runs of scripts don't reload or raise error with importlib if the prior error was on load. Justo load it first: import cureimport, percolation as P, etc.

The variable P.percolation\_graph is a ConjunctiveGraph with all execution state information metadata and translates and with each variable value as value, a bag (unordered, e.g. word sizes) or a collection (ordered, principal components, etc).

Every feature should be related to at least one legacy/ outline.

Routines should be oriented towards making or navigating percolation graph paths directly or through numeric computation and rendering of new triples in Open Linked Social Data and external resources such as the DBpedia sparql endpoint: http://dbpedia.org/sparql

### Notes

In the integrated measures, see if networks that have peculiar distribution of measures in erdos sectors also have smaller KS-distance between histograms of degrees and other topological measures. Generalizing, see if structures with an outlier of a measure (or set of measures) is correlated with other measures characteristics, such as the correlation histogram.

See legacy.triples for further notes.

### the modules are: 

bootstrap.py for PercolationServer and the canonic startup

legacy/\* for standard usage outlines, analyses and media rendering from legacy data (Open Linked Open Data)

- harnessing/\*.py for percolatory procedures (e.g. experiments), resource recommendation, self-knowledge and information collection and diffusion.
- media\_rendering/ for general output of media (music.py, image.py, animation.py, table.py, game.py).
- rdf 
- analyses/\*.py for standard analysis of some structures, resunts in assertions and data endorsements
- measures/\*.py for measurement routines, data structures and values from initial data
- triples/\*.py triples with information about files and notes

rdf/\* for rdf data managing

- ontology.py triples and organization of the participation ontology (po), an umbrella ontology
- reasoning.py reasoning on specific rdfs and owl rules to enhance performance and benchmarking among approaches
- rdflib.py facilities for rdflib graph manipulation
- sparql.py facilities for queying and connecting through sparql

statistics/\* for computing statistics appropriated to Open Linked Social Data

- kolmogorv\_smirnov.py for obtainance of KS distance and c statistics
- unit\_root\_test.py for e.g. the augmented Dickey–Fuller test
- pca.py for correlation and principal component analysis
- outliers.py for the detection of outliers in data
- circular.py for circular statisics
- localization.py for mean, standard deviation, skewness and curtosis

measures/\* for taking measures of social structures. It takes data and produces more informative data which is used in the analyses

- text/\*.py for taking measures from chars, tokens, sentences, paragraphs of a single text
- topology/\*.py for making networks and taking topological measures from a single structure
- time/\*.py for taking circular measures of 
- integrated/\*.py 

  - pca.py for aplication of principal component analysis to grouped entities and appropriated data
  - power\_law.py for measures about the optimum fit of the power-law 
  - kolmogorov\_smirnov.py for KS-distance and c statistics between the grouped entities.
  - 

- multi/\* for measures of multiple structures

  - grouping.py for obtaining meaningful groups of entities (Erdos sectorialization, k-means, k-nearest neighbors, kohonen). Basic grouping of texts is the message, basic grouping for topology and time is the participant. The topmost grouping is the snapshot or collection of snapshots.
  - scale.py for measures in multiple scales (e.g. snapshots, snapshot, sector, user, message)
  - timeline.py for timeline sequences of structures, make unit root test and pca averages and stds
  - scale\_timeline.py for multiple scale timelines, find best fit for power-law and 

analysis/\* for deriving assertions from social structures (e.g. mean(token size) above mean of OLSD legacy. Same file tree as measures

utils/\*.py

  - file.py for navigating and modifiling file structure
  - web/\* for integration to the WWW

## Usage example

```python
    import percolation as P

    po=P.rdf.ontology() # rdflib.Graph()
    metadata=P.rdf.legacyMetadata() # rdflib.Graph()
    percolation_graph=po+metadata # rdflib.Graph()
    snapshot=P.rdf.oneTranslate() # URI
    network=P.topology.makeNetwork(snapshot) # networx network
    topological_analysis=P.topology.analyse(network) # rdflib.Graph()
    textual_analysis=P.text.analyse(snapshot) # rdflib.Graph()
    integrated_analysis=P.integrated.analyse(snapshot) # rdflib.Graph()
    P.tables.make(integrated_analysis,"/tables/") # render latex, js and md tables
    P.audiovisuals.make(integrated_analysis,"/av/") # render sonification in sync with stopmotion animation from data
    user_uri=P.oneUser(integrated_analysis) # uri
    P.audiovisuals.makeMusic(integrated_analysis,"/av/",focus=user_uri) # render music
    P.web.startServer(port=5077) # start server in localhost:5077 or better specify
```

## Further information

The percolation package is a work in progress.
