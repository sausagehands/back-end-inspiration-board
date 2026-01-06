from app.models.board import Board
import pytest

# TEST BOARD MODEL:

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

# TEST BOARD ROUTES:

