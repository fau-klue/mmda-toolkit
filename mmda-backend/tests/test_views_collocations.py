import unittest.mock as mock

import pandas
import pytest
from flask import url_for


@pytest.mark.api
@pytest.mark.now
@mock.patch('backend.views.collocation_views.generate_semantic_space')
def test_create_collocation(mock_coords, client, header):

    mock_coords.return_value = pandas.DataFrame(
        data=[[1.0, 2.0, 3.0, 4.0]],
        columns=['x', 'y', 'x_user', 'y_user'],
        index=['foo', 'bar']
    )

    data = {'name': 'foobar',
            'discourseme': 'foobar',
            'corpus': 'GERMAPARL1386',
            'items': ['Seehofer'],
            'p_query': 'word',
            's_break': 's'}

    response = client.post(
        url_for('collocation.create_collocation', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )

    assert response.status_code == 201


@pytest.mark.api
def test_get_collocation_discoursemes(client, header):

    response = client.get(
        url_for('collocation.get_discoursemes_for_collocation',
                username='student1', collocation=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.now
@mock.patch('backend.views.collocation_views.generate_items_coordinates')
def test_put_discourseme_into_collocation(mock_coords, client, header):

    # mock_coords.return_value = pandas.DataFrame(
    #     data=[[1.0, 2.0, 3.0, 4.0]],
    #     columns=['x', 'y', 'x_user', 'y_user'],
    #     index=['foo', 'bar']
    # )

    data = {'name': 'foobar', 'items': ['Seehofer']}

    response = client.post(
        url_for('discourseme.create_discourseme', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )

    response = client.put(
        url_for('collocation.put_discourseme_into_collocation',
                username='student1', collocation=1, discourseme=2),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    # assert mock_coords.call_count == 1
    assert response.status_code == 200


@pytest.mark.api
def test_remove_discourseme_from_collocation(client, header):

    response = client.delete(
        url_for('collocation.delete_discourseme_from_collocation',
                username='student1', collocation=1, discourseme=2),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_all_collocation(client, header):

    response = client.get(
        url_for('collocation.get_all_collocation', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_collocation(client, header):

    response = client.get(
        url_for('collocation.get_collocation', username='student1', collocation=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_update_collocation(client, header):

    data = {'name': 'somethingnew', 's_break': 's', 'p_query': 'word', 'window_size': 5}
    response = client.put(
        url_for('collocation.update_collocation', username='student1', collocation=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header,
        json=data
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_collocate_for_collocation(client, header):

    data = 'collocate=Merkel&collocate=Seehofer&window_size=10'
    response = client.get(
        url_for('collocation.get_collocate_for_collocation', username='student1', collocation=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_collocate_for_collocation_discourseme_id(client, header):

    data = 'discourseme=1&window_size=10'
    response = client.get(
        url_for('collocation.get_collocate_for_collocation', username='student1', collocation=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_concordance_for_collocation(client, header):

    data = 'window_size=1'
    response = client.get(
        url_for('collocation.get_concordance_for_collocation',
                username='student1', collocation=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_concordance_for_collocation_with_items(client, header):

    data = 'window_size=1&item=Seehofer&item=Angela'
    response = client.get(
        url_for('collocation.get_concordance_for_collocation',
                username='student1', collocation=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_get_concordance_for_collocation_with_discourseme_id(client, header):

    data = 'window_size=1&discourseme=1'
    response = client.get(
        url_for('collocation.get_concordance_for_collocation',
                username='student1', collocation=1),
        query_string=data,
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_delete_collocation(client, header):

    response = client.delete(
        url_for('collocation.update_collocation', username='student1', collocation=1),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200
