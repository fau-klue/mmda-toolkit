from flask import url_for


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

def test_discourseme_read_all(client, header):

    response = client.get(url_for('discourseme.get_discoursemes', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


def test_discourseme_read(client, header):

    response = client.get(url_for('discourseme.get_discourseme',
                                  username='student1',
                                  discourseme=1),
                                  follow_redirects=True,
                                  content_type='application/json',
                                  headers=header)

    assert response.status_code==200


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


def test_discourseme_delete(client, header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    response = client.delete(url_for('discourseme.delete_discourseme',
                                     username='student1',
                                     discourseme=2),
                             follow_redirects=True,
                             content_type='application/json',
                             headers=header)

    assert response.status_code==200
