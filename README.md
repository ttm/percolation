# percolation
the percolation python package for harnessing open linked social data

## install with:
If you are running Ubuntu, you may want to install pygraphviz from standard (apt) package manager.

    $ pip install percolation
or
    $ python setup.py install
For greater control of customization (and debugging), clone the repo and install with pip with -e:
    $ git clone https://github.com/ttm/percolation.git
    $ pip install -e <path_to_repo>
This install method is especially useful when reloading modified module in subsequent runs of percolation
(usually with the standard importlib).

Percolation may use social, music and visuals packages to enable anthropological physics experiments and social harnessing:
- https://github.com/ttm/social
- https://github.com/ttm/music
- https://github.com/ttm/visuals


## core features
  - Provide routines for percolation in social systems by experiments and processes.
  - Ease knowledge about the networked self.
  - Analyses of social systems through textual, topological, temporal statistics within a typology framework of agents and networks.
  - Art and games from social structures, such as music and animation.
  - Integration of resources through RDF data and OWL ontologies.
  - Cross provenance resource recommendation, extending facilities from the Participation package.
  - WWW integration to provide data and media.

## coding conventions
A function name has a verb if it changes state of initialized objects, if it only "returns something", it is has no verb in name.
This rule is extended for the cases where instead of return triples, they are added to the percolation\_graph.

Classes, functions and variables are writen in CamelCase, headlessCamelCase and lowercase, respectively.
Underline is used only in variable names where the words in variable name make something unreadable (usually because the resulting name is big).

The code is the documentation. Code should be very readable to avoid writing unnecessary documentation and duplicating routine representations. This adds up to using docstrings to give context to the objects or omitting the docstrings.

Tasks might have c("some status message") which are printed with time interval in seconds between P.check calls.
These messages are turned of by setting P.QUIET=True or calling P.silence() which just sets P.QUIET=True

The usual variables in scripts are: P for percolation, NS for P.rdf.NS for namespace, a for NS.rdf.type, c for P.utils.check, S for social, M for music, V for visuals, n for numpy, p for pylab, r for rdflib, x for networkx

The file cureimport.py in newtests avoids cluttering the header of the percolation file while hacking framework. In using the Python interpreter, subsequent runs of scripts don't reload or raise error with importlib if the prior error was on load. Just load it first: import cureimport, percolation as P, etc.

The variable P.percolation\_graph is a ConjunctiveGraph with all execution state information metadata and translates and with each variable value as value, a bag (unordered, e.g. word sizes) or a collection (ordered, principal components, etc).

Every feature should be related to at least one legacy/ outline.

Routines should be oriented towards making or navigating percolation graph paths directly or through numeric computation and rendering of new triples in Open Linked Social Data and external resources such as the DBpedia sparql endpoint: http://dbpedia.org/sparql

### package structure
Data and metadata is in the P.percolation\_graph=rdflib.ConjunctiveGraph()
which is persistent across runs in the system and is initialized by bootstrap.py
and developed by user with rdf or automatically while other percolation tasks are run.
The statistics module have routines for obtaining statistics from data, which are applied
to data in measures.
The analyses module make (qualitative) assertions about the measures in social structures.
The utils eases file navigation and sharing in local system and web, percolation status register and small features that fit nowhere else.
The help module have some directions on percolation usage while legacy module have diverse usage outlines.

#### the modules are: 
bootstrap.py for PercolationServer and the canonic startup

legacy/\* for standard usage outlines, analyses and media rendering from legacy data (Open Linked Open Data)
- harnessing/\*.py for percolative procedures (e.g. experiments), resource recommendation, self-knowledge and information collection and diffusion.
- mediaRendering/ for general output of media (music.py, image.py, animation.py, table.py, game.py).
- rdf 
- analyses/\*.py for canonical percolation analysis of structures, results in assertions and data endorsements
- measures/\*.py for measurement routines, data structures and values from initial data
- triples/\*.py triples with information about files and notes
  - datasets.py for triples on the datasets of open linked social data with local and remote filenames
  - linksets.py for triples that link datasets (e.g. irc:Participant#hybrid po:sameAs fb:Participant#renato.fabbri)
  - enrichments.py for hand notes and other structures for enrichment of the percolation status (be traslated to rdf)
  - notes.py for hand notes and other structures for enrichment of the percolation status (be traslated to rdf)
  - software.py for triples of software and ontologies pertinent to percolation environment

rdf/\* for rdf data managing
- ontology.py triples and organization of the participation ontology (po), an umbrella ontology
- reasoning.py reasoning on specific rdfs and owl rules to enhance performance and benchmarking among approaches
- rdflib.py facilities for rdflib graph manipulation
- sparql.py facilities for querying and connecting through sparql

statistics/\* for computing statistics appropriated to Open Linked Social Data
- kolmogorv\_smirnov.py for obtaining KS distance and c statistics
- unit\_root\_test.py for e.g. the augmented Dickey–Fuller test
- pca.py for correlation and principal component analysis
- outliers.py for the detection of outliers in data
- circular.py for circular statistics
- localization.py for mean, standard deviation, skewness and kurtosis
- grouping/\*.py for obtaining meaningful groups of entities through Erdos sectorialization, k-means, k-nn, Kohonen, genetic algorithms, etc.

measures/\* for taking measures of social structures. It takes data and produces more informative data which is used in the analyses
- text/\*.py for taking measures from chars, tokens, sentences, paragraphs of a single text
- topology/\*.py for making networks and taking topological measures from a single structure
- time/\*.py for taking circular measures of 
- integrated/\*.py 
  - pca.py for application of principal component analysis to grouped entities and appropriated data
  - power\_law.py for measures about the optimum fit of the power-law 
  - kolmogorov\_smirnov.py for KS-distance and c statistics between the grouped entities.
- multi/\* for measures of multiple structures
  - grouping.py for obtaining meaningful groups of entities. Basic grouping of texts is the message, basic grouping for topology and time is the participant. The topmost grouping is the snapshot or collection of snapshots.
  - scale.py for measures in multiple scales (e.g. snapshots, snapshot, sector, user, message)
  - timeline.py for timeline sequences of structures, make unit root test and pca averages and stds
  - scale\_timeline.py for multiple scale timelines, find best fit for power-law and 

analysis/\* for deriving assertions from social structures (e.g. mean(token size) above mean of OLSD legacy. Same file tree as measures

utils/\*.py
  - general.py for general purpose utilities that fit nowhere else, e.g. randomNick
  - status.py for 
  - file.py for navigating and modifying file structure
  - web/\* for integration to the WWW

help/\* for helper routines (e.g. wizard or steps to make something)

## usage example
```python
import percolation as P

P.start() # starts percolation server and session with metadata about open linked social data
P.analyse() # take measures and deliver assertions
P.legacy.media_rendering.render() # make tables, music and animation
P.web() # start server to make data and media accessible in the Web
```

## further information
The percolation package is a work in progress.

### notes
In the integrated measures, see if networks that have peculiar distribution of measures in Erdos sectors also have smaller KS-distance between histograms of degrees and other topological measures. Generalizing, see if structures with an outlier of a measure (or set of measures) is correlated with other measures characteristics, such as the correlation histogram.

Are there benchmark datasets and results for the statistics used in percolation? If so, integrate them into legacy.statistics.tests.
Otherwise, make benchmarks from synthesized and empirical data.

Percolation makes use of other packages designed for percolation for direct use or through the rendered RDF they deliver.
These are:
- The social package for rendering RDF data from social networking platforms and protocols (e.g. facebook, twitter, irc, instagram, noosfero, diaspora)
- The gmane package for rendering RDF data from public Gmane email lists (e.g. apache, c++ stdlib)
- The participation package for rendering RDF data from social participation platforms (e.g. participabr, cidade democratica, aa)
- The scientific package (ToDo) for rendering RDF data from scientific resources such as FAPESP
- The music package to render music from open linked social data
- The visuals package to render images and movies from open linked social data

See legacy.triples for further notes.

See percolationLegacy issues at: https://github.com/ttm/percolationLegacy/issues

See this deprecated document for some of the intended goals:
https://github.com/ttm/percolationlegacy/blob/master/latex/percolation-article.pdf
