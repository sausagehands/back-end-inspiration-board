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
    response_body = response.get_json()[0]

    # Assert
    assert response.status_code == 200
    assert response_body["id"] == one_card.id
    assert response_body["message"] == one_card.message
    assert response_body["like_count"] == one_card.like_count


def test_update_card(client, one_card):
    # Arrange
    test_data = {
        "id": 1,
        "message": "Try updated message",
        "like_count": 0,
        "board_id": 1
    }
    # Act
    response = client.put(f"/cards/{one_card.id}", json=test_data)
    # Assert
    assert response.status_code == 200
    assert response.get_json()["message"] == "Try updated message"


def test_update_card_missing_record(client):
    # Arrange
    test_data = {
        "message": "Try updated message",
        "id":100
    }
    # Act
    response = client.put(f"/cards/100", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details": "Card 100 not found"}


def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")

    # Assert
    assert response.status_code == 204
    all_cards = client.get("/cards").get_json()
    assert all_cards == []


def test_delete_card_missing_record(client, one_card):
    # Act
    response = client.delete("/cards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details": "Card 3 not found"}

