import pytest
from datetime import datetime

def test_todo_list(client):
    # View the home page and check to see the header and a to-do item
    response = client.get('/')
    assert b'<h1>a simple to-do application</h1>' in response.data
    assert b'clean room' in response.data

    # Mock data should show three to-do items, one of which is complete
    assert response.data.count(b'<span class="') == 3
    assert response.data.count(b'<span class="completed') == 1

def test_add_task(client):
    response = client.post('/',
    data={'action': 'test'})
    assert b'test' in response.data
