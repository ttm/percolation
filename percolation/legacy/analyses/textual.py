import percolation as P


class TextualAnalysis:
    def __init__(self, text='a string'):
        self.text_dict = P.measures.topology.directMeasures.topologicalMeasures(text)
