import pytest
import unittest.mock as mock
import pandas as pd
from pandas.util.testing import assert_frame_equal

from backend.analysis.semspace import load_vectors
from backend.analysis.semspace import generate_semantic_space
from backend.analysis.semspace import generate_discourseme_coordinates
from backend.analysis.semspace import SemanticSpace


VECTORS_FILEPATH = "~/corpora/wectors/magnitude/enWikiWord2Vec.magnitude"
t = {
    'tokens': ['Angela', 'Merkel', 'test', 'fasd'],
    'base': ['resorbent', 'unshelled', 'geodynamical', 'claustrophile', 'nonhormonal', 'tributary', 'tricolon', 'Tyndareus', 'petalous', 'catalases', 'catechizer', 'sheepsheads', 'reassemblage', 'beknown', 'retired', 'privations', 'stock-punished', 'belongeth', 'yard-master', 'dowerless', 'bilker', 'annihilate', 'appreciatingly', 'retiracy', 'expands', 'insolubly', 'reflags', 'tom-toms', 'regimental', 'permanency', 'transference', 'factfinder', 'lopus', 'tempestive', 'hallowed', 'besnowed', 'besought', 'photoprotection', 'Moirae', 'semichronic', 'laughably', 'corn-tassel', 'do-rags', 'mournfully', 'discrepance', 'hedge-bantling', 'villarsia', 'replume', 'gossamer', 'Homburg'],
    'method': 'umap'
}


@pytest.mark.old
def test_coord_load_vectors_fail():
    actual = load_vectors(['token1', 'token2', 'token1'],
                          '/tmp/imnothere.pymagnitude')
    expected = pd.DataFrame()
    assert_frame_equal(actual, expected)


@pytest.mark.old
@mock.patch('backend.analysis.semspace.Magnitude')
def test_coord_load_vectors(mock_pymag):

    mock_pymag.return_value.query.side_effect = [[1, 1, 1], [2, 2, 2], [1, 1, 1]]

    expected = pd.DataFrame(data=[
        [1, 1, 1],
        [2, 2, 2]],
        index=['token1', 'token2'])

    actual = load_vectors(['token1', 'token2', 'token1'],
                          '/tmp/foo.pymagnitude')

    mock_pymag.assert_called_with('/tmp/foo.pymagnitude')
    assert_frame_equal(actual, expected)


@pytest.mark.old
def test_generate_semantic_space_old():

    coordinates = generate_semantic_space(
        t['tokens'], VECTORS_FILEPATH, method=t['method'])

    assert len(coordinates) == len(t['tokens'])


def test_generate_semantic_space_new():

    semspace = SemanticSpace(VECTORS_FILEPATH)
    coordinates = semspace.generate_semspace(t['base'], method=t['method'])

    # init user coordinates
    coordinates['user_x'] = None
    coordinates['user_y'] = None

    assert len(coordinates) == len(t['base'])


def test_add_item():
    semspace = SemanticSpace(VECTORS_FILEPATH)
    semspace.generate_semspace(t['base'], method=t['method'])
    new_coordinates = semspace.add_item(t['tokens'][0])
    assert isinstance(new_coordinates, pd.Series)


@pytest.mark.now
def test_generate_discourseme_coordinates():
    semspace = SemanticSpace(VECTORS_FILEPATH)
    coordinates = semspace.generate_semspace(t['base'], method=t['method'])
    a = generate_discourseme_coordinates(
        t['tokens'], coordinates, VECTORS_FILEPATH
    )
    print(a)
