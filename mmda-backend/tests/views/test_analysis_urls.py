from flask import url_for
import unittest.mock as mock
import pandas
import pytest


@pytest.mark.api
@mock.patch('backend.views.analysis_views.generate_semantic_space')
def test_create_analysis(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(
        data=[[1.0, 2.0, 3.0, 4.0]],
        columns=['x', 'y', 'x_user', 'y_user'],
        index=['foo', 'bar']
    )

    data = {'name': 'foobar',
            'discourseme': 'foobar',
            'corpus': 'GERMAPARL1318',
            'items': ['Merkel'],
            'p_query': 'word',
            's_break': 's'}

    response = client.post(
        url_for('analysis.create_analysis', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )

    assert response.status_code == 201


@pytest.mark.api
def test_get_analysis_discoursemes(client, header):

    response = client.get(
        url_for('analysis.get_discoursemes_for_analysis',
                username='student1', analysis=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
@mock.patch('backend.views.analysis_views.generate_items_coordinates')
def test_put_discourseme_into_analysis(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(
        data=[[1.0, 2.0, 3.0, 4.0]],
        columns=['x', 'y', 'x_user', 'y_user'],
        index=['foo', 'bar']
    )

    data = {'name': 'foobar', 'items': ['Merkel', 'Seehofer']}

    response = client.post(
        url_for('discourseme.create_discourseme', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )

    response = client.put(
        url_for('analysis.put_discourseme_into_analysis',
                username='student1', analysis=1, discourseme=2),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert mock_coords.call_count == 1
    assert response.status_code == 200


@pytest.mark.api
def test_remove_discourseme_from_analysis(client, header):

    response = client.delete(
        url_for('analysis.delete_discourseme_from_analysis',
                username='student1', analysis=1, discourseme=2),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_all_analysis(client, header):

    response = client.get(
        url_for('analysis.get_all_analysis', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_analysis(client, header):

    response = client.get(
        url_for('analysis.get_analysis', username='student1', analysis=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_update_analysis(client, header):

    data = {'name': 'somethingnew', 's_break': 's', 'p_query': 'word', 'window_size': 5}
    response = client.put(
        url_for('analysis.update_analysis', username='student1', analysis=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_collocate_for_analysis(client, header):

    data = 'collocate=Merkel&collocate=Seehofer&window_size=10'
    response = client.get(
        url_for('analysis.get_collocate_for_analysis', username='student1', analysis=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_collocate_for_analysis_discourseme_id(client, header):

    data = 'discourseme=1&window_size=10'
    response = client.get(
        url_for('analysis.get_collocate_for_analysis', username='student1', analysis=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_concordance_for_analysis(client, header):

    data = 'window_size=1'
    response = client.get(
        url_for('analysis.get_concordance_for_analysis',
                username='student1', analysis=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_concordance_for_analysis_with_items(client, header):

    data = 'window_size=1&item=Seehofer&item=Angela'
    response = client.get(
        url_for('analysis.get_concordance_for_analysis',
                username='student1', analysis=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_concordance_for_analysis_with_discourseme_id(client, header):

    data = 'window_size=1&discourseme=1'
    response = client.get(
        url_for('analysis.get_concordance_for_analysis',
                username='student1', analysis=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_delete_analysis(client, header):

    response = client.delete(
        url_for('analysis.update_analysis', username='student1', analysis=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200
