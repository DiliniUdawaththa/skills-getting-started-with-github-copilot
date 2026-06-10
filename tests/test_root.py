"""
Tests for the root endpoint (GET /)
"""
import pytest


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to /static/index.html"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_follows_redirect(client):
    """Test that following the redirect from / works"""
    response = client.get("/", follow_redirects=True)
    
    # After following redirect, we get HTML content
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
