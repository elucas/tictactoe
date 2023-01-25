"""Tests to be run using pytest"""
from tictactoe import (
    PLAYER_X,
    PLAYER_O,
    str_to_board,
    board_to_str,
    init_board,
    find_free_cells,
    computer_choose_move,
)

"""Test boards"""
BOARD_EMPTY = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
BOARD_ALL_X = [
    [PLAYER_X, PLAYER_X, PLAYER_X],
    [PLAYER_X, PLAYER_X, PLAYER_X],
    [PLAYER_X, PLAYER_X, PLAYER_X],
]
BOARD_ALL_O = [
    [PLAYER_O, PLAYER_O, PLAYER_O],
    [PLAYER_O, PLAYER_O, PLAYER_O],
    [PLAYER_O, PLAYER_O, PLAYER_O],
]
BOARD_ALTERNATES = [
    [PLAYER_X, PLAYER_O, PLAYER_X],
    [PLAYER_O, PLAYER_X, PLAYER_O],
    [PLAYER_X, PLAYER_O, PLAYER_X],
]
BOARD_PARTIAL = [
    [PLAYER_X, PLAYER_O, PLAYER_X],
    [4, 5, 6],
    [PLAYER_X, PLAYER_O, PLAYER_X],
]
BOARD_LAST_GO = [
    [PLAYER_X, PLAYER_O, PLAYER_X],
    [PLAYER_O, PLAYER_X, PLAYER_O],
    [PLAYER_X, PLAYER_O, 9],
]
BOARD_FIRST_CELL = [
    [1, PLAYER_O, PLAYER_X],
    [PLAYER_O, PLAYER_X, PLAYER_O],
    [PLAYER_X, PLAYER_O, PLAYER_X],
]
BOARD_TWO_CELLS = [
    [1, PLAYER_O, PLAYER_X],
    [PLAYER_O, PLAYER_X, PLAYER_O],
    [PLAYER_X, PLAYER_O, 9],
]
BOARD_INIT = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

def test_str_to_board_empty():
    board = str_to_board("")
    assert board == BOARD_EMPTY, "Empty string should generate an empty board"

def test_str_to_board_gibberish():
    board = str_to_board("oxqwertyuiop")
    assert board == BOARD_EMPTY, "Incorrect cells should be converted to empty"

def test_str_to_board_all_x():
    board = str_to_board("XXXXXXXXX")
    assert board == BOARD_ALL_X, "Load all Xs"

def test_str_to_board_all_o():
    board = str_to_board("OOOOOOOOO")
    assert board == BOARD_ALL_O, "Load all Os"

def test_str_to_board_alternates():
    board = str_to_board("XOXOXOXOX")
    assert board == BOARD_ALTERNATES, "Load alternates"

def test_str_to_board_partial():
    board = str_to_board("XOX   XOX")
    assert board == BOARD_PARTIAL, "Load partial board"


def test_board_to_str_empty():
    out = board_to_str(BOARD_EMPTY)
    assert out == '         ', "Empty board should be 9 spaces"

def test_board_to_str_all_x():
    out = board_to_str(BOARD_ALL_X)
    assert out == 'XXXXXXXXX', "Should be 9 Xs"

def test_board_to_str_all_o():
    out = board_to_str(BOARD_ALL_O)
    assert out == 'OOOOOOOOO', "Should be 9 Os"

def test_board_to_str_partial():
    out = board_to_str(BOARD_PARTIAL)
    assert out == 'XOX   XOX', "Should match the partial board"


def test_init_board():
    out = init_board()
    assert out == BOARD_INIT, "Initial board state should be correct"


def test_find_free_cells_empty():
    cells = find_free_cells(BOARD_EMPTY)
    assert cells == [1,2,3,4,5,6,7,8,9], "Free cells on empty board should include all moves"

def test_find_free_cells_alternates():
    cells = find_free_cells(BOARD_ALTERNATES)
    assert cells == [], "Free cells on a full board should be empty"

def test_find_free_cells_partial():
    cells = find_free_cells(BOARD_PARTIAL)
    assert cells == [4,5,6], "Free cells on partial board should be middle row"

def test_find_free_cells_last_go():
    cells = find_free_cells(BOARD_LAST_GO)
    assert cells == [9], "Find the remaining cell"


def test_computer_choose_move_several():
    move = computer_choose_move(BOARD_PARTIAL)
    assert move in [4,5,6], "Only middle row are free"

def test_computer_choose_move_none():
    move = computer_choose_move(BOARD_ALL_X)
    assert move is None, "No moves left"

def test_computer_choose_move_last_go():
    move = computer_choose_move(BOARD_LAST_GO)
    assert move in [9], "Only last cell is free"

def test_computer_choose_move_first_cell():
    move = computer_choose_move(BOARD_FIRST_CELL)
    assert move in [1], "Only first cell is free"

def test_computer_choose_move_two_cells():
    # Hammer this to flush out randoms
    choices = []
    for x in range(100):
        move = computer_choose_move(BOARD_TWO_CELLS)
        choices.append(move)
    assert 1 in choices, "After 100 attempts, 1st cell should appear least once"
    assert 9 in choices, "After 100 attempts, 9th cell should appear least once"

