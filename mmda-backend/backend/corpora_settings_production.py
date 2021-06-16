"""
Corpus specific settings
Contains the available corpora on the system

name: Human-readable name
name_api: CWB handle of the corpus
embeddings: Path to pymagnitude word vectors
[language]: Language of corpus
[register]: Register of corpus
[description]: 
"""

CORPORA = {
    'BREXIT_V190615': {
        'name': 'BREXIT_V190615',
        'name_api': 'Brexit tweets',
        'embeddings': '/opt/embeddings/enTwitterWord2Vec.magnitude',
        'language': 'en',
        'register': 'cmc',
        'description': 'test'
    },
}
