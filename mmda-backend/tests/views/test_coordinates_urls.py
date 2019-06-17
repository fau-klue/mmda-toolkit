from flask import url_for
import unittest.mock as mock
import pandas
import pytest


@pytest.mark.api
@mock.patch('backend.views.analysis_views.generate_semantic_space')
def test_get_coordinates(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(data=[[1.0, 2.0, 3.0, 4.0]],columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'], index=['foo', 'bar'])

    data = {'name': 'foobar', 'corpus': 'SZ_SMALL', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('analysis.create_analysis', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    response = client.get(url_for('coordinates.get_coordinates',
                                  username='student1',
                                  analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert mock_coords.call_count == 1
    assert response.status_code == 200


@pytest.mark.api
@mock.patch('backend.views.coordinates_views.generate_semantic_space')
def test_reload_coordinates(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(data=[[1.0, 2.0, 3.0, 4.0]],columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'], index=['foo', 'bar'])

    response = client.put(url_for('coordinates.reload_coordinates',
                                  username='student1',
                                  analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert mock_coords.call_count == 1
    assert response.status_code == 200


@pytest.mark.api
def test_update_coordinates(client, header):

    data = {'das': {'user_x': 100, 'user_y': 100}}

    response = client.put(url_for('coordinates.update_coordinates',
                                  username='student1',
                                  analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code == 200


@pytest.mark.api
def test_delete_coordinates(client, header):

    data = {'das': {'user_x': 100, 'user_y': 100}}

    response = client.delete(url_for('coordinates.delete_coordinates',
                                  username='student1',
                                  analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code == 200
