from flask import url_for
from flask_jwt_extended import create_refresh_token, create_access_token
from json import loads


def test_login_urls(client):

    data = {'username': 'student1', 'password': 'Erlangen1'}

    response = client.post(url_for('login.login'),
                           follow_redirects=True,
                           content_type='application/json',
                           json=data)

    assert response.status_code==200

    response_data = loads(response.data)

    headers = {
        'Authorization': 'Bearer {}'.format(response_data['refresh_token'])
    }

    response = client.post(url_for('login.refresh'),
                           follow_redirects=True,
                           content_type='application/json',
                           json=data,
                           headers=headers)

    assert response.status_code==200


def test_login_urls_failure(client):

    data = {'username': 'student1', 'password': 'WRONGPASSWD'}
    response = client.post(url_for('login.login'),
                           follow_redirects=True,
                           content_type='application/json',
                           json=data)

    assert response.status_code==401

    data = {'username': 'nouser', 'password': 'nopassword'}
    response = client.post(url_for('login.login'),
                           follow_redirects=True,
                           content_type='application/json',
                           json=data)

    assert response.status_code==401


def test_user_jwt_token(client):

    access_token = create_access_token('student1')

    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }

    response = client.get(url_for('login.test_login'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=headers)

    assert response.status_code == 200

    response = client.get(url_for('login.test_user', username='student1'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=headers)

    assert response.status_code == 200

    response = client.get(url_for('login.test_user', username='foobar'),
                           follow_redirects=True,
                           content_type='application/json',
                           headers=headers)

    assert response.status_code == 403


def test_admin_jwt(client, admin_header):

    response = client.get(url_for('login.test_admin'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200
