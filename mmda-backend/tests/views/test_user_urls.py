from flask import url_for


def test_user_info(client, header):

    response = client.get(url_for('user.get_user', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==200


def test_user_password(client, header):

    data = {'password': 'Erlangen1'}
    response = client.put(url_for('user.put_user_password', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    assert response.status_code==200
