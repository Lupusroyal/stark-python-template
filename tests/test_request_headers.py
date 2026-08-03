def test_request_headers_are_present(client):
    response = client.get("/health")

    assert response.status_code == 200

    assert "X-Process-Time" in response.headers
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"] != ""
