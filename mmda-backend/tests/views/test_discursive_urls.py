import unittest.mock as mock
import pandas
from flask import url_for
import pytest


@pytest.mark.api
def test_discursive_create(client, header):

    data = {'name': 'foobar', 'discoursemes': [1]}
    response = client.post(url_for('discursive_position.create_discursive_position', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==201

    response = client.post(url_for('discursive_position.create_discursive_position', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json={})

    assert response.status_code==400


@pytest.mark.api
def test_discursive_get_concordance_not_params(client, header):

    # Missing corpora
    just_items = 'analysis=123'
    response = client.get(url_for('discursive_position.get_discursive_position_concordances', username='student1', discursive_position=1),
                          query_string=just_items,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==400

    # Missing analysis
    just_corpus = 'corpus=SZ_SMALL'
    response = client.get(url_for('discursive_position.get_discursive_position_concordances', username='student1', discursive_position=1),
                          query_string=just_corpus,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==400


@pytest.mark.api
@pytest.mark.xfail
@mock.patch('backend.views.analysis_views.generate_semantic_space')
def test_discursive_get_concordance(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(data=[[1.0, 2.0, 3.0, 4.0]],columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'], index=['foo', 'bar'])

    data = {'name': 'foobar', 'corpus': 'SZ_SMALL', 'items': ['Merkel'], 'p_query': 'word', 's_break': 's'}
    client.post(url_for('analysis.create_analysis', username='student1'),
                follow_redirects=True,
                content_type='application/json',
                headers=header,
                json=data)

    data = 'analysis=1&corpus=SZ_SMALL'
    response = client.get(url_for('discursive_position.get_discursive_position_concordances', username='student1', discursive_position=1),
                          query_string=data,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discursive_read(client, header):

    response = client.get(url_for('discursive_position.get_discursive_position',
                                  username='student1',
                                  discursive_position=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discursive_read_notthere(client, header):

    response = client.get(url_for('discursive_position.get_discursive_position',
                                  username='student1',
                                  discursive_position=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==404


@pytest.mark.api
def test_discursive_read_all(client, header):

    response = client.get(url_for('discursive_position.get_discursive_positions',
                                  username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discursive_update(client, header):

    data = {'name': 'newname'}
    response = client.put(url_for('discursive_position.update_discursive_position',
                                  username='student1',
                                  discursive_position=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==200


@pytest.mark.api
def test_discursive_update_notthere(client, header):

    data = {'name': 'newname'}
    response = client.put(url_for('discursive_position.update_discursive_position',
                                  username='student1',
                                  discursive_position=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==404


@pytest.mark.api
def test_put_discourseme_into_discursive_position(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    response = client.put(url_for('discursive_position.put_discourseme_into_discursive_position',
                                  username='student1',
                                  discursive_position=1,
                                  discourseme=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==200


@pytest.mark.api
def test_put_discourseme_into_discursive_position_notthere(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.put(url_for('discursive_position.put_discourseme_into_discursive_position',
                                  username='student1',
                                  discursive_position=1337,
                                  discourseme=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==404


@pytest.mark.api
def test_get_discoursemes_for_discursive_position(client, header):

    response = client.get(url_for('discursive_position.get_discoursemes_for_discursive_position',
                                  username='student1',
                                  discursive_position=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_get_discoursemes_for_discursive_position_notthere(client, header):

    response = client.get(url_for('discursive_position.get_discoursemes_for_discursive_position',
                                  username='student1',
                                  discursive_position=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==404


@pytest.mark.api
def test_delete_discourseme_from_discursive_position(client, header):

    response = client.delete(url_for('discursive_position.delete_discourseme_from_discursive_position',
                                  username='student1',
                                  discursive_position=1,
                                  discourseme=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discursive_delete(client, header):

    response = client.delete(url_for('discursive_position.update_discursive_position',
                                  username='student1',
                                  discursive_position=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discursive_delete_notthere(client, header):

    response = client.delete(url_for('discursive_position.update_discursive_position',
                                  username='student1',
                                     discursive_position=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==404
