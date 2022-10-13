import pytest
from flask import url_for


@pytest.mark.api
def test_get_all_keywords(client, header):

    response = client.get(
        url_for('keyword.get_all_keywords', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200


@pytest.mark.api
def test_create_keyword(client, header):

    response = client.get(
        url_for('keyword.create_keyword', username='student1'),
        follow_redirects=True,
        content_type='application/json',
        headers=header
    )

    assert response.status_code == 200
