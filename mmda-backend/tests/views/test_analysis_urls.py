from flask import url_for
import unittest.mock as mock
import pandas
import pytest


@pytest.mark.api
@mock.patch('backend.views.analysis_views.generate_semantic_space')
def test_create_analysis(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(data=[[1.0, 2.0, 3.0, 4.0]],columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'], index=['foo', 'bar'])

    data = {'name': 'foobar', 'corpus': 'SZ_SMALL', 'items': ['foobar', 'barfoo'], 'p_query': 'word', 's_break': 's'}
    response = client.post(url_for('analysis.create_analysis', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==201


@pytest.mark.api
def test_get_analysis_discoursemes(client, header):

    response = client.get(url_for('analysis.get_discoursemes_for_analysis', username='student1', analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
@mock.patch('backend.views.analysis_views.generate_discourseme_coordinates')
def test_put_discourseme_into_analysis(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(data=[[1.0, 2.0, 3.0, 4.0]],columns=['tsne_x', 'tsne_y', 'user_x', 'user_y'], index=['foo', 'bar'])

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    response = client.put(url_for('analysis.put_discourseme_into_analysis', username='student1', analysis=1, discourseme=2),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert mock_coords.call_count == 1
    assert response.status_code == 200


@pytest.mark.api
def test_remove_discourseme_from_analysis(client, header):

    response = client.delete(url_for('analysis.delete_discourseme_from_analysis', username='student1', analysis=1, discourseme=2),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_get_all_analysis(client, header):

    response = client.get(url_for('analysis.get_all_analysis', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_get_analysis(client, header):

    response = client.get(url_for('analysis.get_analysis', username='student1', analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_update_analysis(client, header):

    data = {'name': 'somethingnew'}
    response = client.put(url_for('analysis.update_analysis', username='student1', analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==200


@pytest.mark.api
def test_get_collocate_for_analysis(client, header):

    data = 'collocate=foobar&collocate=barfoo'
    response = client.get(url_for('analysis.get_collocate_for_analysis', username='student1', analysis=1),
                          query_string=data,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_get_concordance_for_analysis(client, header):

    data = 'window_size=1'
    response = client.get(url_for('analysis.get_concordance_for_analysis', username='student1', analysis=1),
                          query_string=data,
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


@pytest.mark.api
def test_delete_analysis(client, header):

    response = client.delete(url_for('analysis.update_analysis', username='student1', analysis=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200
