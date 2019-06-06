from flask import url_for
import unittest.mock as mock
import pandas


def test_users_list(client, admin_header):

    response = client.get(url_for('admin.get_users'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200


def test_no_access(client, header):

    response = client.get(url_for('admin.get_users'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header)

    assert response.status_code==403


def test_create_user(client, admin_header):

    new_user = {
        'username': 'johnsnow',
        'first_name': 'John',
        'last_name': 'Snow',
        'email': 'john@stark.wst',
        'password': 'winteriscoming',
    }

    response = client.post(url_for('admin.create_user'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header,
                          json=new_user)

    assert response.status_code==201

    # Password too short
    new_user = {
        'username': 'tyrion',
        'first_name': 'Tyrion',
        'last_name': 'Lannister',
        'email': 'ty@lan.wst',
        'password': 'tyrion',
    }

    response = client.post(url_for('admin.create_user'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header,
                          json=new_user)

    assert response.status_code==400


def test_no_such_role_createuser(client, admin_header):

    new_user = {
        'username': 'nedstark',
        'first_name': 'Ned',
        'last_name': 'Stark',
        'email': 'ned@stark.wst',
        'password': 'winteriscoming',
        'role': 'NOSUCHROLE'
    }

    response = client.post(url_for('admin.create_user'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header,
                          json=new_user)

    assert response.status_code==404


def test_create_admin_user(client, admin_header):

    new_user = {
        'username': 'nedstark',
        'first_name': 'Ned',
        'last_name': 'Stark',
        'email': 'ned@stark.wst',
        'password': 'winteriscoming',
        'role': 'admin'
    }

    response = client.post(url_for('admin.create_user'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header,
                          json=new_user)

    assert response.status_code==201


def test_update_password(client, admin_header):

    data = {'password': 'Erlangen1'}

    response = client.put(url_for('admin.put_user_password', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header,
                          json=data)


    assert response.status_code==200


def test_delete_user(client, admin_header):

    new_user = {
        'username': 'johnsnow',
        'first_name': 'John',
        'last_name': 'Snow',
        'email': 'john@stark.wst',
        'password': 'winteriscoming',
    }

    response = client.post(url_for('admin.create_user'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header,
                          json=new_user)

    response = client.delete(url_for('admin.delete_user', username='johnsnow'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200


def test_delete_admin_user(client, admin_header):

    response = client.delete(url_for('admin.delete_user', username='admin'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==409


def test_get_items(client, admin_header):

    response = client.get(url_for('admin.get_analysis'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200

    response = client.get(url_for('admin.get_discourseme'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200

    response = client.get(url_for('admin.get_discursive_position'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200


def test_delete_discourseme(client, header, admin_header):

    data = {'name': 'foobar', 'items': ['foobar', 'barfoo']}
    response = client.post(url_for('discourseme.create_discourseme', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    response = client.delete(url_for('admin.delete_discourseme', discourseme=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200


def test_delete_position(client, header, admin_header):

    data = {'name': 'foobar', 'discoursemes': [1]}
    response = client.post(url_for('discursive_position.create_discursive_position', username='student1'),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=header,
                          json=data)

    response = client.delete(url_for('admin.delete_discursive_position', discursive_position=1),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==200


def test_delete_analysis_noanalysis(client, header, admin_header):

    response = client.delete(url_for('admin.delete_analysis', analysis=2),
                          follow_redirects=True,
                          content_type='application/json',
                          headers=admin_header)

    assert response.status_code==404
