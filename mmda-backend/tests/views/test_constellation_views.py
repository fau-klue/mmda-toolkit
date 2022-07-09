import unittest.mock as mock
import pandas
from flask import url_for
import pytest


@pytest.mark.api
def test_constellation_create(client, header):

    data = {'name': 'foobar', 'discoursemes': [1]}
    response = client.post(url_for('constellation.create_constellation', username='student1'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=header,
                           json=data)

    assert response.status_code == 201

    response = client.post(url_for('constellation.create_constellation', username='student1'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=header,
                           json={})

    assert response.status_code == 400


@pytest.mark.api
def test_constellation_get_concordance_not_params(client, header):

    # Missing corpora
    wrong_analysis = 'analysis=123'
    response = client.get(url_for('constellation.get_constellation_concordance',
                                  username='student1', constellation=1),
                          query_string=wrong_analysis,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code == 404

    # # Missing analysis
    # just_corpus = 'corpus=GERMAPARL_1114'
    # response = client.get(url_for('constellation.get_constellation_concordance',
    #                               username='student1', constellation=1),
    #                       query_string=just_corpus,
    #                       follow_redirects=True,
    #                       content_type='application/json',
    #                       headers=header)

    # assert response.status_code == 400


@pytest.mark.api
@mock.patch('backend.views.collocation_views.generate_semantic_space')
def test_constellation_get_concordance(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(
        data=[[1.0, 2.0, 3.0, 4.0]],
        columns=['x', 'y', 'x_user', 'y_user'],
        index=['foo', 'bar']
    )
    # TODO
    # data = {'name': 'foobar', 'discoursemes': [1]}
    # response = client.post(url_for('constellation.create_constellation', username='student1'),
    #                        follow_redirects=True,
    #                        content_type='application/json',
    #                        headers=header,
    #                        json=data)

    # response = client.get(
    #     url_for('constellation.get_constellation_concordance',
    #             username='student1', constellation=response.json['msg']),
    #     query_string=data,
    #     follow_redirects=True,
    #     content_type='application/json',
    #     headers=header
    # )

    # assert response.status_code == 200


@pytest.mark.api
def test_constellation_read(client, header):

    response = client.get(url_for('constellation.get_constellation',
                                  username='student1',
                                  constellation=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code == 200


@pytest.mark.api
def test_constellation_read_notthere(client, header):

    response = client.get(url_for('constellation.get_constellation',
                                  username='student1',
                                  constellation=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code == 404


@pytest.mark.api
def test_constellation_read_all(client, header):

    response = client.get(url_for('constellation.get_constellations',
                                  username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code == 200


@pytest.mark.api
def test_constellation_update(client, header):

    data = {'name': 'newname'}
    response = client.put(url_for('constellation.update_constellation',
                                  username='student1',
                                  constellation=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code == 200


@pytest.mark.api
def test_constellation_update_notthere(client, header):

    data = {'name': 'newname'}
    response = client.put(url_for('constellation.update_constellation',
                                  username='student1',
                                  constellation=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code == 404


@pytest.mark.api
def test_put_discourseme_into_constellation(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=header,
                           json=data)

    response = client.put(url_for('constellation.put_discourseme_into_constellation',
                                  username='student1',
                                  constellation=1,
                                  discourseme=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code == 200


@pytest.mark.api
def test_put_discourseme_into_constellation_notthere(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.put(url_for('constellation.put_discourseme_into_constellation',
                                  username='student1',
                                  constellation=1337,
                                  discourseme=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code == 404


@pytest.mark.api
def test_get_discoursemes_for_constellation(client, header):

    response = client.get(url_for('constellation.get_discoursemes_for_constellation',
                                  username='student1',
                                  constellation=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code == 200


@pytest.mark.api
def test_get_discoursemes_for_constellation_notthere(client, header):

    response = client.get(url_for('constellation.get_discoursemes_for_constellation',
                                  username='student1',
                                  constellation=1337),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code == 404


@pytest.mark.api
def test_delete_discourseme_from_constellation(client, header):

    response = client.delete(url_for('constellation.delete_discourseme_from_constellation',
                                     username='student1',
                                     constellation=1,
                                     discourseme=1),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=header)

    assert response.status_code == 200


@pytest.mark.api
def test_constellation_delete(client, header):

    response = client.delete(url_for('constellation.update_constellation',
                                     username='student1',
                                     constellation=1),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=header)

    assert response.status_code == 200


@pytest.mark.api
def test_constellation_delete_notthere(client, header):

    response = client.delete(url_for('constellation.update_constellation',
                                     username='student1',
                                     constellation=1337),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=header)

    assert response.status_code == 404
