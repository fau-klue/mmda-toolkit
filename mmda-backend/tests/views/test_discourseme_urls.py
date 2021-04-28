from flask import url_for
import unittest.mock as mock
import pytest
import pandas


@pytest.mark.api
def test_discourseme_create(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==201

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                           json={})

    assert response.status_code==400

@pytest.mark.api
def test_discourseme_read_all(client, header):

    response = client.get(url_for('discourseme.get_discoursemes', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discourseme_read(client, header):

    response = client.get(url_for('discourseme.get_discourseme',
                                  username='student1',
                                  discourseme=1),
                                  follow_redirects=True,
                                  content_type='application/json',
                                  headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_discourseme_update(client, header):

    data = {'name': 'newname', 'items': ['something']}
    response = client.put(url_for('discourseme.update_discourseme',
                                     username='student1',
                                     discourseme=1),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=header,
                             json=data)

    assert response.status_code==200


@pytest.mark.api
@mock.patch('backend.views.analysis_views.generate_semantic_space')
def test_discourseme_update_topic(mock_coords, client, header):
    # old behaviour: You cannot edit a topic discourseme
    # new behaviour: You can! Why not? (many-to-many mapping)

    mock_coords.return_value = pandas.DataFrame(
        data=[[1.0, 2.0, 3.0, 4.0]],
        columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'],
        index=['foo', 'bar']
    )

    data = {'discourseme': 'foobar',
            'name': 'foobar',
            'corpus': 'GERMAPARL1318',
            'items': ['Merkel'],
            'p_query': 'word',
            's_break': 's'}

    response = client.post(url_for('analysis.create_analysis', username='student1'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=header,
                           json=data)

    analysis_id = response.json['msg']

    response = client.get(url_for('analysis.get_analysis',
                                  username='student1',
                                  analysis=analysis_id),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    discourseme_id = response.json['topic_id']
    data = {'name': 'newname',
            'items': ['something']}

    response = client.put(url_for('discourseme.update_discourseme',
                                  username='student1',
                                  discourseme=discourseme_id),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)
    print(response.json)

    assert response.status_code == 200


@pytest.mark.api
def test_discourseme_delete(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(
        url_for('discourseme.create_discourseme', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )
    discourseme_id = response.json['msg']

    response = client.delete(url_for('discourseme.delete_discourseme',
                                     username='student1',
                                     discourseme=discourseme_id),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=header)

    assert response.status_code==200
