# import pytest
# import unittest.mock as mock
import pandas as pd
# from pandas.util.testing import assert_frame_equal

# from backend.analysis.semspace import load_vectors
# from backend.analysis.semspace import generate_semantic_space
from backend.analysis.semspace import SemanticSpace


def get_vector_path(app, corpus):
    return app.config['CORPORA'][corpus['corpus_name']]['embeddings']


t = {
    'method': 'umap',
    'tokens': ['Angela', 'Merkel', 'test', 'fasd'],
    'base': [
        'resorbent', 'unshelled', 'geodynamical', 'claustrophile',
        'nonhormonal', 'tributary', 'tricolon', 'Tyndareus', 'petalous',
        'catalases', 'catechizer', 'sheepsheads', 'reassemblage',
        'beknown', 'retired', 'privations', 'stock-punished', 'belongeth',
        'yard-master', 'dowerless', 'bilker', 'annihilate',
        'appreciatingly', 'retiracy', 'expands', 'insolubly', 'reflags',
        'tom-toms', 'regimental', 'permanency', 'transference',
        'factfinder', 'lopus', 'tempestive', 'hallowed', 'besnowed',
        'besought', 'photoprotection', 'Moirae', 'semichronic',
        'laughably', 'corn-tassel', 'do-rags', 'mournfully',
        'discrepance', 'hedge-bantling', 'villarsia', 'replume',
        'gossamer', 'Homburg'
    ]
}


def test_generate_semantic_space(app, test_corpus):

    semspace = SemanticSpace(get_vector_path(app, test_corpus))
    coordinates = semspace.generate_semspace(t['base'], method=t['method'])

    # init user coordinates
    coordinates['user_x'] = None
    coordinates['user_y'] = None

    assert len(coordinates) == len(t['base'])


def test_add_item(app, test_corpus):
    semspace = SemanticSpace(get_vector_path(app, test_corpus))
    semspace.generate_semspace(t['base'], method=t['method'])
    new_coordinates = semspace.add_item(t['tokens'][0])
    assert isinstance(new_coordinates, pd.Series)


# TODO: recycle old tests
# @pytest.mark.old
# def test_coord_load_vectors_fail():
#     actual = load_vectors(['token1', 'token2', 'token1'],
#                           '/tmp/imnothere.pymagnitude')
#     expected = pd.DataFrame()
#     assert_frame_equal(actual, expected)


# @pytest.mark.old
# @mock.patch('backend.analysis.semspace.Magnitude')
# def test_coord_load_vectors(mock_pymag):

#     mock_pymag.return_value.query.side_effect = [[1, 1, 1], [2, 2, 2], [1, 1, 1]]

#     expected = pd.DataFrame(data=[
#         [1, 1, 1],
#         [2, 2, 2]],
#         index=['token1', 'token2'])

#     actual = load_vectors(['token1', 'token2', 'token1'],
#                           '/tmp/foo.pymagnitude')

#     mock_pymag.assert_called_with('/tmp/foo.pymagnitude')
#     assert_frame_equal(actual, expected)


# @pytest.mark.old
# def test_generate_semantic_space_old():

#     coordinates = generate_semantic_space(
#         t['tokens'], VECTORS_FILEPATH, method=t['method'])

#     assert len(coordinates) == len(t['tokens'])


# @pytest.mark.now
# def test_generate_discourseme_coordinates():
#     semspace = SemanticSpace(VECTORS_FILEPATH)
#     coordinates = semspace.generate_semspace(t['base'], method=t['method'])
#     a = generate_discourseme_coordinates(
#         t['tokens'], coordinates, VECTORS_FILEPATH
#     )
#     print(a)


# @mock.patch('backend.analysis.tsne.load_vectors')
# def test_coord_generate_2d_coordinates(mock_vectors):

#     mock_data = pandas.DataFrame(data=[[1, 1, 1], [2, 2, 2]],
#                                  index=['token1', 'token2'])
#     mock_vectors.return_value = mock_data

#     actual = tsne.generate_semantic_space(
#         ['token1', 'token2', 'token1'],
#         '/tmp/foo.pymagnitude'
#     )

#     assert list(actual.index) == ['token1', 'token2']
#     assert list(actual['user_x']) == [None, None]
#     assert list(actual['user_y']) == [None, None]


# @mock.patch('backend.analysis.tsne.load_vectors')
# def test_coord_generate_2d_coordinates_error(mock_vectors):

#     fail = tsne.generate_semantic_space(
#         ['token1', 'token2', 'token1'],
#         '/tmp/foo.pymagnitude'
#     )
#     assert fail.empty


# def test_calculate_item_coordinates():

#     mock_coordinates = DataFrame({
#         'user_x': [1, 1, 1],
#         'user_y': [2, 2, 2],
#         'tsne_x': [3, 3, 3],
#         'tsne_y': [4, 4, 4]
#     }, index=['token1', 'token2', 'token3'])

#     mock_embeddings = pandas.DataFrame(data=[[1, 1, 1],
#                                              [2, 2, 2],
#                                              [3, 3, 3]],
#                                        index=['token1', 'token2', 'token3'])

#     expected = pandas.Series(data=[3.0, 4.0, 1.0, 2.0],
#                              index=['tsne_x', 'tsne_y', 'user_x', 'user_y'])

#     actual = tsne.calculate_item_coordinates(
#         [1, 1, 1], mock_embeddings, mock_coordinates
#     )
#     print(expected)
#     print(actual)
#     # TODO
#     # assert expected.equals(actual) == True


# @mock.patch('backend.analysis.tsne.calculate_item_coordinates')
# @mock.patch('backend.analysis.tsne.load_vectors')
# def test_generate_discourse_coordinates(mock_vectors, mock_combine):

#     mock_coordinates = DataFrame({
#         'tsne_x': [3, 3],
#         'tsne_y': [4, 4],
#         'user_x': [None, None],
#         'user_y': [None, None]
#     }, index=['token1', 'token2'])

#     mock_vectors.return_value = pandas.DataFrame(
#         data=[[11, 11], [22, 22]],
#         index=['token1', 'token2']
#     )
#     mock_combine.return_value = pandas.Series(
#         data=[3.0, 4.0, 1.0, 2.0],
#         index=['tsne_x', 'tsne_y', 'user_x', 'user_y']
#     )

#     expected = pandas.DataFrame(
#         data=[[1.0, 2.0, 3.0, 4.0]],
#         columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'],
#         index=['foo', 'bar']
#     )

#     actual = tsne.generate_discourseme_coordinates(
#         ['foo', 'bar'], mock_coordinates, '/tmp/foo.pymagnitude'
#     )

#     assert_frame_equal(actual, expected)


# @mock.patch('backend.analysis.tsne.calculate_item_coordinates')
# @mock.patch('backend.analysis.tsne.load_vectors')
# def test_generate_discourse_coordinates_with_empty_list(mock_vectors, mock_combine):

#     mock_coordinates = DataFrame({
#         'tsne_x': [3, 3],
#         'tsne_y': [4, 4],
#         'user_x': [None, None],
#         'user_y': [None, None]
#     }, index=['foo', 'bar'])

#     mock_vectors.return_value = pandas.DataFrame(
#         data=[[11, 11], [22, 22]], index=['foo', 'bar']
#     )
#     expected = pandas.DataFrame()

#     actual = tsne.generate_discourseme_coordinates(
#         ['foo', 'bar'], mock_coordinates, '/tmp/foo.pymagnitude'
#     )
#     assert_frame_equal(actual, expected)


# @mock.patch('backend.analysis.tsne.calculate_item_coordinates')
# @mock.patch('backend.analysis.tsne.load_vectors')
# def test_generate_discourse_coordinates_with_user(mock_vectors, mock_combine):

#     mock_coordinates = DataFrame({
#         'tsne_x': [3, 3],
#         'tsne_y': [4, 4],
#         'user_x': [1, 2],
#         'user_y': [1, 2]
#     }, index=['token1', 'token2'])

#     mock_vectors.return_value = pandas.DataFrame(
#         data=[[11, 11], [22, 22]],
#         index=['token1', 'token2']
#     )
#     mock_combine.return_value = pandas.Series(
#         data=[3.0, 4.0, 1.0, 2.0],
#         index=['tsne_x', 'tsne_y', 'user_x', 'user_y']
#     # )

#     # expected = pandas.DataFrame(
#     #     data=[[1.0, 2.0, 3.0, 4.0]],
#     #     columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'],
#     #     index=['foo', 'bar']
#     # )

#     # actual = tsne.generate_discourseme_coordinates(
#     #     ['foo', 'bar'], mock_coordinates, '/tmp/foo.pymagnitude'
#     # )

#     # assert_frame_equal(actual, expected)