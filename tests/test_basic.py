import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'


def test_shorten_url(client):
    response = client.post('/api/shorten', json={"url": "www.google.com"})
    assert response.status_code == 200
    data = response.get_json()
    assert "short_code" in data
    assert "short_url" in data