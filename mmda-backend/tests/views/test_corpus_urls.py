from flask import url_for
import pytest


@pytest.mark.api
def test_corpora(client, header):

    response = client.get(url_for('corpus.get_corpora'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_corpus(client, header):

    response = client.get(url_for('corpus.get_corpus', corpus='SZ_SMALL'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200
