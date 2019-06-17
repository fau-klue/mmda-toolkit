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
