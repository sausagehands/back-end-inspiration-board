def test_get_all_cards_with_no_records(client):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_cards(client, one_card):
    # Act
    response = client.get("/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Alice travel to Newyork",
        "owner": "Alice",
        "message":"Try something new every day",    
        "board_id": None,
    }]

def test_create_one_card(client):
    # Act
    response = client.post("/cards", json={
        "message": "Try something new every day",
        "like_count": 0
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "owner": "Alice",
        "title": "Alice travel to Newyork",
        "message": "Try something new every day",
        "like_count": 0,    
        "board_id": None,
    }
def test_create_card_missing_message(client):
    # Act
    response = client.post("/cards", json={
        "like_count": 0
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data: message is required"
    }