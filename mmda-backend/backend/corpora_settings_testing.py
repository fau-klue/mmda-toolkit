"""
Corpus specific settings
Contains the available corpora on the system

name: Human-readable name
name_api: CWB handle
embeddings: Path to pymagnitude word vectors
language: Language of corpus
genre: Genre of the corpus
"""

CORPORA = {
    'GERMAPARL_1114': {
        'name': 'GermaParl',
        'name_api': 'GERMAPARL_1114',
        'embeddings': '/home/ausgerechnet/corpora/embeddings/magnitude/deWikiWord2Vec.magnitude',
        'language': 'de',
        'genre': 'Newspaper'
    },
}
