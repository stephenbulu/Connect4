import pytest

from connect import Game


def test_is_column_full_single_column():
    game = Game(1, 2)

    game.board = [[0, 1]]
    assert not game.is_column_full(0)

    game.board = [[1, 0]]
    assert game.is_column_full(0)


def test_is_column_full_multicolumn():
    game = Game(3, 2)

    game.board = [[1, 0, 1], [1, 1, 1]]
    assert not game.is_column_full(1)

    game.board = [[0, 1, 0], [0, 0, 0]]
    assert game.is_column_full(1)
