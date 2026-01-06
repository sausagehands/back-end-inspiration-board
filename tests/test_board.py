from app.models.board import Board
import pytest

########## TEST BOARD MODEL:

def test_to_dict_no_missing_data():
    # Arrange
    test_data = Board(id = 1, title="New Board", owner="Madi Rei", cards = [])

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] == "New Board"
    assert result["owner"] == "Madi Rei"
    assert result["cards"] == []

def test_to_dict_missing_id():
    # Arrange
    test_data = Board(title="New Board", owner="Madi Rei", cards = [])

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] is None
    assert result["title"] == "New Board"
    assert result["owner"] == "Madi Rei"
    assert result["cards"] == []

def test_to_dict_missing_title():
    # Arrange
    test_data = Board(id=1, owner="Madi Rei", cards=[])

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] is None
    assert result["owner"] == "Madi Rei"
    assert result["cards"] == []

def test_from_dict_returns_board():
    # Arrange
    board_data = {"title": "New Board", "owner": "Madi Rei"}

    # Act
    new_board = Board.from_dict(board_data)

    # Assert
    assert new_board.title == "New Board"

def test_from_dict_with_no_title():
    # Arrange
    board_data = {"owner": "Madi Rei"}

    # Act & Assert
    with pytest.raises(KeyError) as error:
        Board.from_dict(board_data)

    assert error.value.args[0] == "title"

def test_from_dict_with_extra_keys():
    # Arrange
    board_data = {
        "extra": "some stuff",
        "title": "New Board",
        "owner": "Madi Rei",
        "cards": [],
        "another": "last value"
    }
    
    # Act
    new_board = Board.from_dict(board_data)

    # Assert
    assert new_board.title == "New Board"

########## TEST BOARD ROUTES:

def test_create_one_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "New Board",
        "owner": "Madi Rei"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Board",
        "owner": "Madi Rei",
        "cards": []
    }

def test_create_one_board_no_title(client):
    # Arrange
    test_data = {
        "owner": "Madi Rei"
    }

    # Act
    response = client.post("/boards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {'details': 'Invalid request: missing title'}

def test_create_one_board_with_extra_keys(client):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Board",
        "owner": "Madi Rei",
        "another": "last value"
    }

    # Act
    response = client.post("/boards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "title": "New Board",
        "owner": "Madi Rei",
        "cards": []
    }

def test_get_all_boards_one_saved_board(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Build a habit of going outside daily",
        "owner": "Alice",
        "cards": []
    }

def test_get_all_boards_no_saved_board(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []    

def test_create_card_with_board(client, one_board):
    # Arrange
    test_data = {
        "message": "Card 1"
    }

    # Act
    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "message": "Card 1",
        "like_count": 0,
        "board_id": 1
    }

def test_create_card_with_nonexistant_board(client):
    # Arrange
    test_data = {
        "message": "Card 1"
    }

    # Act
    response = client.post("/boards/1/cards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details": "Board 1 not found"}

def test_create_card_with_bad_board_id(client):
    # Arrange
    test_data = {
        "message": "Card 1"
    }

    # Act
    response = client.post("/boards/cat/cards", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"details":"Board cat invalid"}

def test_get_cards_by_board_expects_two_cards(client, board_with_two_cards):
    response = client.get(f"/boards/{board_with_two_cards.id}/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2

    messages = {card["message"] for card in response_body}

    assert messages == {
        "A Message",
        "Another Message"
    }

    for card in response_body:
        assert card["like_count"] == 0
        assert card["board_id"] == board_with_two_cards.id
        assert "id" in card

def test_get_cards_by_board_with_no_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []
    
def test_update_board(client, one_board):
    # Arrange
    test_data = {
        "title": "New Board",
        "owner": "Madi Rei"
    }

    # Act
    response = client.put("/boards/1", json=test_data)

    # Assert
    assert response.status_code == 204
    assert response.content_length is None

def test_update_board_missing_record(client, one_board):
    # Arrange
    test_data = {
        "title": "New Board",
        "owner": "Madi Rei"
    }

    # Act
    response = client.put("/boards/3", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details": "Board 3 not found"}

def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")

    # Assert
    assert response.status_code == 204
    assert response.content_length is None


def test_delete_board_missing_record(client, one_board):
    # Act
    response = client.delete("/boards/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"details": "Board 3 not found"}