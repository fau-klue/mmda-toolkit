#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Handling word embeddings and their two-dimensional coordinates.
"""

from logging import getLogger

from numpy import matmul, where, errstate
from pandas import DataFrame, concat
from pymagnitude import Magnitude
from sklearn.metrics.pairwise import cosine_similarity

log = getLogger('mmda-logger')


class SemanticSpace:

    def __init__(self, path=None):
        """

        :param str path: path to a .magnitude embeddings file.

        """
        self.database = path
        if self.database is not None:
            self.embeddings = Magnitude(self.database)
        self.coordinates = None

    def _embeddings(self, tokens):
        """
        get embeddings for tokens into a DataFrame.

        :param set tokens: set of tokens to get embeddings for

        :return: Dataframe containing embeddings
        :rtype: Dataframe
        """

        items = list(set(tokens))
        embeddings = [self.embeddings.query(item) for item in items]
        df = DataFrame(index=items, data=embeddings)

        return df

    def generate2d(self, tokens, method='umap'):
        """creates 2d-coordinates for a list of tokens

        :param list tokens: list of tokens to generate coordinates for
        :param str method: umap / tsne

        :return: pandas.Dataframe with x and y coordinates
        :rtype: pandas.Dataframe

        """

        # load vectors
        embeddings = self._embeddings(tokens)

        # if no vectors are loaded
        if embeddings.empty:
            return DataFrame()

        # just in case
        embeddings = embeddings.dropna()

        # set up transformer
        if method == 'tsne':
            from sklearn.manifold import TSNE
            transformer = TSNE(n_components=2,
                               metric='euclidean',
                               perplexity=10.,
                               verbose=0,
                               init='pca',
                               learning_rate='auto')

        elif method == 'umap':
            from umap import UMAP
            transformer = UMAP()

        else:
            raise NotImplementedError(f'transformation "{method}" not supported')

        # generate 2d coordinates and save as DataFrame
        coordinates = DataFrame(
            data=transformer.fit_transform(embeddings),
            index=embeddings.index,
            columns=['x', 'y']
        )
        coordinates.index.name = 'item'

        # save as own coordinates
        self.coordinates = coordinates

        return coordinates

    def add(self, items, cutoff=.2):
        """caclulates coordinates for new items based on their cosine
        similarity to the items spanning self.coordinates.

        :param str items: items to add
        :param float cutoff: cut-off value for cosine similarity

        :return: new coordinates (columns 'x' and 'y', indexed by items)
        :rtype: DataFrame

        """

        # get embedding for item
        item_embeddings = self._embeddings(items)
        base_embeddings = self._embeddings(self.coordinates.index)
        base_coordinates = self.coordinates

        # cosine similaritiy matrix (n_items times n_base)
        sim = cosine_similarity(item_embeddings, base_embeddings)

        # apply cut-off
        # sim = where(sim < cutoff, 0, sim)

        # norm rows to use as convex combination
        simsum = sim.sum(axis=1)
        sim = (sim.T/simsum).T

        # matrix multiplication takes care of linear combination
        new_coordinates = matmul(sim, base_coordinates)

        # convert to DataFrame
        new_coordinates = DataFrame(new_coordinates)
        new_coordinates.index = items

        # append
        self.coordinates = concat([self.coordinates, new_coordinates])

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
    return semspace._embeddings(tokens)


def generate_semantic_space(tokens, vectors_filepath, method='tsne'):
    """Generate 2D coordinates or a list of items.  This function returns
    a DataFrame with two sets of coordinates: x, y from an automatic
    dimensionality reduction method and x, y placeholders for
    coordinates from a user.

    :param list tokens: List of tokens to generate coordinates for.
    :return: pandas.Dataframe with x,y coordinates (tsne, user)
    :rtype: pandas.Dataframe

    """

    semspace = SemanticSpace(vectors_filepath)
    coordinates = semspace.generate2d(tokens, method)

    # init user coordinates
    coordinates['x_user'] = None
    coordinates['y_user'] = None

    return coordinates


def generate_items_coordinates(items, base_coordinates, vectors_filepath):
    """Generate 2D coordinates for additional items. This method places
    the given items withn the given base coordinates, taking into
    consideration their similarities.

    :param list items: List of items to generate coordinates for
    :param pandas.DataFrame base_coordinates: TODO
    :param str vectors_filepath: Path to a *.pymagnitude vectors file.
    :return: pandas.Dataframe with x,y coordinates (tsne, user)
    :rtype: pandas.Dataframe

    """

    # Check if some of the items are already in the base_coordinates,
    # If so remove those items
    intersect_items = set(items).intersection(set(base_coordinates.index))
    items = list(set(items) - intersect_items)

    # Handle empty list
    if not items:
        return DataFrame()

    semspace = SemanticSpace(vectors_filepath)
    semspace.coordinates = base_coordinates[['x', 'y']]

    new_coordinates = semspace.add(items)

    # init user coordinates
    new_coordinates['x_user'] = None
    new_coordinates['y_user'] = None

    return new_coordinates
