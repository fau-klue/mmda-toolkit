from flask import url_for
import pytest


@pytest.mark.xfail
@pytest.mark.api
def test_corpora(client, header):

    response = client.get(url_for('corpus.get_corpora'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.xfail
@pytest.mark.api
def test_corpus(client, header):

    response = client.get(url_for('corpus.get_corpus', corpus='SZ_SMALL'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.xfail
@pytest.mark.api
def test_concordances(client, header):

    data = {'foo': 'bar'}
    response = client.get(url_for('corpus.get_concordances', corpus='SZ_SMALL'), query_string=data,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==400

    # Test multiple items
    data = 'item=foobar&item=barfoo'
    response = client.get(url_for('corpus.get_concordances', corpus='SZ_SMALL'), query_string=data,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200
