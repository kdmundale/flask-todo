import pytest
from flask import g, session
from flasktodo.db import get_db
from flasktodo import db

def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'email': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        cur = db.get_db().cursor()
        cur.execute(
            "SELECT * from users WHERE email = 'a'",
        );
        cur.fetchone()
        assert cur is not None
        cur.close()

# @pytest.mark.parametrize(('email', 'password', 'message'), (
#     ('', '', b'email is required.'),
#     ('a', '', b'password is required.'),
#     ('test', 'test', b'invalid'),
# ))
# def test_register_validate_input(client, email, password, message):
#     response = client.post(
#         '/auth/register',
#         data={'email': email, 'password': password}
#     )
#     assert message in response.data
