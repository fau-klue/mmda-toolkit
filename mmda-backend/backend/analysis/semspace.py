"""
Module to manage dimensionality transformations.
"""

from logging import getLogger
from pandas import DataFrame
from pymagnitude import Magnitude
from scipy.spatial.distance import cosine


log = getLogger('mmda-logger')


class SemanticSpace:

    def __init__(self, database_path):
        """
        :param str database_path: Path to a .pymagnitude embeddings file.
        """
        self.database = database_path

        if self.database is not None:
            try:
                self.embeddings = Magnitude(self.database)

            except RuntimeError:
                log.error('Could not load Magnitude file at %s', self.database)
                self.embeddings = None
                self.database = None

    def _get_vectors(self, tokens):
        """
        Loads a subset (tokens) of all WordVectors into Pandas Dataframe.

        :param list tokens: List of tokens to load word embeddings for.
        :return: pandas.Dataframe containing word vectors for the list of tokens.
        :rtype: pandas.Dataframe
        """
        if self.embeddings is None:
            return DataFrame()

        # pymagnitude will find most similar vectors for OOV tokens
        vectors = []
        for token in tokens:
            vectors.append(self.embeddings.query(token))

        # create df
        df = DataFrame(data=vectors, index=tokens)
        df.drop_duplicates(inplace=True)

        return df

    def generate_semspace(self, tokens, method='tsne'):
        """
        creates 2d-coordinates for a list of tokens

        :param list tokens: list of tokens to generate coordinates for
        :return: pandas.Dataframe with x and y coordinates
        :rtype: pandas.Dataframe
        """

        # load vectors
        vectors = self._get_vectors(tokens)

        # if no vectors are loaded (tokens are empty)
        if vectors.empty:
            return DataFrame()

        # set up transformer
        if method == 'tsne':
            from sklearn.manifold import TSNE
            transformer = TSNE(n_components=2,
                               metric='euclidean',
                               perplexity=10.,
                               verbose=0)

        elif method == 'umap':
            from umap import UMAP
            transformer = UMAP()

        else:
            raise NotImplementedError(
                'transformation "%s" not supported' % method
            )

        # generate 2d embeddings
        embeddings = transformer.fit_transform(vectors)

        # create data frame
        coordinates = DataFrame(data=embeddings,
                                index=vectors.index,
                                columns=['x', 'y'])

        self.coordinates = coordinates
        return coordinates

    def add_item(self, item, base_coordinates=None, cutoff=.2):
        """
        Calculate new coordinates for one embedding, based on embedding similarity.

        :param list item_embedding: TODO
        :param pandas.DataFrame base_embeddings: TODO
        :param pandas.DataFrame base_coordinates: TODO
        :param float cutoff: TODO
        :return: TODO
        :rtype: TODO
        """

        # get item_embeddings
        item_embedding = self._get_vectors([item])

        # use own coordinates if none provided
        if base_coordinates is None:
            base_coordinates = self.coordinates
        base_embeddings = self._get_vectors(base_coordinates.index)

        # calculate similarity scores
        similarities = []
        for base_item, base_embedding in zip(base_embeddings.index,
                                             base_embeddings.values):
            similarity = 1 - cosine(item_embedding, base_embedding)

            if similarity >= cutoff:
                similarities.append(similarity)
            else:
                similarities.append(0)

        # check if there's any similar items
        global_similarity_index = sum(similarities)

        if global_similarity_index == 0:
            # put in global center
            new_coordinates = base_coordinates.sum() / len(base_coordinates)
        else:
            # weighted average
            tmp_coordinates = base_coordinates.apply(lambda x: x * similarities)
            new_coordinates = tmp_coordinates.sum() / global_similarity_index

        return new_coordinates


def load_vectors(tokens, vectors_filepath):
    """
    Loads a subset (tokens) of all WordVectors into Pandas Dataframe.

    :param list tokens: List of tokens to load word embeddings for.
    :param str vectors_filepath: Path to a *.pymagnitude vectors file.
    :return: pandas.Dataframe containing word vectors the list of tokens.
    :rtype: pandas.Dataframe
    """

    semspace = SemanticSpace(vectors_filepath)
    return semspace._get_vectors(tokens)


def generate_semantic_space(tokens, vectors_filepath, method='umap'):
    """
    Generates 2D coordinates (via word embeddings) for a list of tokens.
    This function returns a DataFrame with two sets of coordinates: x,y from TSNE and x,y placeholders for coordinates from a user.

    :param list tokens: List of tokens to generate coordinates for.
    :return: pandas.Dataframe with x,y coordinates (tsne, user)
    :rtype: pandas.Dataframe
    """

    semspace = SemanticSpace(vectors_filepath)
    coordinates = semspace.generate_semspace(tokens, method)

    # init user coordinates
    coordinates['x_user'] = None
    coordinates['y_user'] = None

    return coordinates


def generate_discourseme_coordinates(items, base_coordinates, vectors_filepath):
    """
    Generate 2D coordinates for discourse items.

    :param list items: List of items to generate coordinates for
    :param pandas.DataFrame base_coordinates: TODO
    :param str vectors_filepath: Path to a *.pymagnitude vectors file.
    :return: pandas.Dataframe with x,y coordinates (tsne, user)
    :rtype: pandas.Dataframe
    """

    # Check if some if the items are already in the base_coordinates,
    # If so remove those items
    intersect_items = set(items).intersection(set(base_coordinates.index))
    items = list(set(items) - intersect_items)

    # Handle empty list
    if not items:
        return DataFrame()

    semspace = SemanticSpace(vectors_filepath)

    x = []
    y = []

    for item in items:
        new_coordinates = semspace.add_item(item, base_coordinates)
        x.append(new_coordinates['x'])
        y.append(new_coordinates['y'])

    new_coordinates = DataFrame({'x': x, 'y': y}, index=items)

    # init user coordinates
    new_coordinates['user_x'] = None
    new_coordinates['user_y'] = None

    return new_coordinates
