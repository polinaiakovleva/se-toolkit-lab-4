import pytest

def test_get_interactions_returns_200(client):
    """Test 1: GET /interactions/ returns HTTP status code 200"""
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_items_have_expected_fields(client):
    """Test 2: Response items contain expected fields"""
    response = client.get("/interactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        item = data[0]
        assert "id" in item
        assert "item_id" in item
        assert "created_at" in item


def test_get_interactions_filter_includes_boundary(client):
    """Test 3: Filter with max_item_id=1 returns items with item_id <= 1"""
    response = client.get("/interactions/?max_item_id=1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert item["item_id"] <= 1