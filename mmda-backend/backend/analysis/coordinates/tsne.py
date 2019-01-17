"""
Module to manage dimensionality transformations.
"""

from logging import getLogger
from pandas import DataFrame
from pymagnitude import Magnitude
from sklearn.manifold import TSNE
from scipy.spatial.distance import cosine


LOGGER = getLogger('mmda-logger')


def load_vectors(tokens, vectors_filepath):
    """
    Loads a subset (tokens) of all WordVectors into Pandas Dataframe.

    :param list tokens: List of tokens to load word embeddings for.
    :param str vectors_filepath: Path to a *.pymagnitude vectors file.
    :return: pandas.Dataframe containing word vectors the list of tokens.
    :rtype: pandas.Dataframe
    """

    try:
        embeddings = Magnitude(vectors_filepath)
    except RuntimeError:
        LOGGER.error('Word vector file not found')
        LOGGER.debug('Filepath: %s', vectors_filepath)
        return DataFrame()

    vectors = []

    # Pymagnitude will find most similar vectors for Out-of-Vocab tokens
    for token in tokens:
        vectors.append(embeddings.query(token))

    ret_dataframe = DataFrame(data=vectors, index=tokens)
    ret_dataframe.drop_duplicates(inplace=True)

    return ret_dataframe


def generate_semantic_space(tokens, vectors_filepath):
    """
    Generates 2D coordinates (via word embeddings) for a list of tokens.
    This function returns a DataFrame with two sets of coordinates: x,y from TSNE and x,y placeholders for coordinates from a user.

    :param list tokens: List of tokens to generate coordinates for.
    :return: pandas.Dataframe with x,y coordinates (tsne, user)
    :rtype: pandas.Dataframe
    """

    vectors = load_vectors(tokens, vectors_filepath)
    if vectors.empty:
        LOGGER.error('Could not load Word Embeddings')
        raise RuntimeError('Could not load Word Embeddings')

    tsne_data = TSNE(n_components=2,
                     metric='euclidean',
                     perplexity=10.,
                     verbose=0)

    tsne_data.fit_transform(vectors)

    coordinates = DataFrame(data=tsne_data.embedding_,
                            index=vectors.index,
                            columns=['tsne_x', 'tsne_y'])

    # because it's a placeholder. Dont use None or NaN cause it will break Flask.jsonify
    coordinates['user_x'] = None
    coordinates['user_y'] = None

    return coordinates


def calculate_item_coordinates(item_embedding, base_embeddings, base_coordinates, cutoff=.2):
    """
    Calculate new coordinates for one embedding, based on embedding similarity.

    :param list item_embedding: TODO
    :param pandas.DataFrame base_embeddings: TODO
    :param pandas.DataFrame base_coordinates: TODO
    :param float cutoff: TODO
    :return: pandas.Series with ['tsne_x', 'tsne_y', 'user_x', 'user_y'] for
    :rtype: pandas.Series
    """

    similarities = []

    for base_embedding in base_embeddings.values:
        similarity = 1 - cosine(item_embedding, base_embedding)

        if similarity >= cutoff:
            similarities.append(similarity)
        else:
            similarities.append(0)

    global_similarity_index = sum(similarities)
    if global_similarity_index == 0:
        # Put in global center
        new_coordinates = base_coordinates.sum() / len(base_coordinates)
    else:
        # Weighted average:
        tmp_coordinates = base_coordinates.apply(lambda x: x * similarities)
        new_coordinates = tmp_coordinates.sum() / global_similarity_index

    return new_coordinates


def generate_discourseme_coordinates(items, base_coordinates, vectors_filepath):
    """
    Generate 2D coordinates for discourse items.

    :param list items: List of items to generate coordinates for
    :param pandas.DataFrame base_coordinates: TODO
    :param str vectors_filepath: Path to a *.pymagnitude vectors file.
    :return: pandas.Dataframe with x,y coordinates (tsne, user)
    :rtype: pandas.Dataframe
    """

    # TODO: Add Comment: whats happending here
    intersect_items = set(items).intersection(set(base_coordinates.index))
    if len(intersect_items) > 0:
        items = list(set(items) - intersect_items)

    base_embeddings = load_vectors(base_coordinates.index, vectors_filepath)
    new_embeddings = load_vectors(items, vectors_filepath)

    user_x = []
    user_y = []
    tsne_x = []
    tsne_y = []

    for new_embedding in new_embeddings.values:
        # TODO: Add error handling
        combined_coordinates = calculate_item_coordinates(new_embedding, base_embeddings, base_coordinates)
        user_x.append(combined_coordinates[0])
        user_y.append(combined_coordinates[1])
        tsne_x.append(combined_coordinates[2])
        tsne_y.append(combined_coordinates[3])

    new_coordinates = DataFrame({
        'tsne_x': tsne_x,
        'tsne_y': tsne_y,
        'user_x': user_x,
        'user_y': user_y
    }, index=items)

    return new_coordinates
