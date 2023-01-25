from random import randrange # imports random so it can be used by the computer to choose a cell
import time
from typing import List
import os

# array of cells that can be used to win when all three contain the same sign
WINNING_MOVES = [[1, 5, 9], [3, 5, 7], [1, 2, 3], [1, 4, 7], [2, 5, 8], [3, 6, 9], [4, 5, 6], [7, 8, 9]]
PLAYER_X = "X"
PLAYER_O = "O"
PLAYERS = [PLAYER_X, PLAYER_O]
NAMES = {
    PLAYER_X: 'Computer',
    PLAYER_O: 'Player',
}


class MoveError(Exception):
    """Thrown when the user attempts an illegal move."""

def str_to_board(raw: str) -> List:
    """Convert a 9 character string to a board.
    (Or the first 9 characters if the string is longer ;-)
    If string isn't long enough, the cells will be considered empty
    """
    board = init_board()
    print(f"Length: {len(raw)}")
    for index in range(0,9):   # 0..8
        if index >= len(raw):
            player = None
        else:
            player = raw[index]
        # Blank any spurious cells
        if player not in PLAYERS:
            player = None
        
        move = index+1
        if player:
            set_board_cell(board, move, player)
    return board


def board_to_str(board: List) -> str:
    """Return a string representation of the board.
    Empty cells are represented by a space.
    """
    cells = []
    for move in range(1,10):
        cell = get_board_cell(board, move)
        if cell not in PLAYERS:
            cell = " "
        cells.append(cell)
    return "".join(cells)


def init_board() -> List:
    """Initialise a new board state with the first move.
    The board returned is a 3x3 list of lists.
    Initial values are the numbers 1..9
    """
    board = [[3 * j + i + 1 for i in range(3)] for j in range(3)] # creates the game board array
    # board[1][1] = PLAYER_X # set first 'X' in the middle
    return board


def cli_display_board(board) -> None:
    os.system('clear')
    """The function accepts one parameter containing the board's current status and prints it out to the console"""
    print("+-------" * 3 + "+", sep="") # prints the top line
    for row in range(3): # for 3 iterations, the program will...
        print("|       " * 3, "|", sep="") # print seperators that appear above and below each number
        for col in range(3): # for 3 * 3 iterations, the program will...
            print("|   " + str(board[row][col]) + "   ", end="") # print rows with a number in them
        print("|") # print last wall at end of previous row
        print("|       " * 3, "|", sep="") # print last row before end
        print("+-------" * 3, "+", sep="") # print end row/wall


def cli_enter_move(board):
    """function that asks the user to enter a move"""
    move = input("Enter your move (1-9):") # asks user to enter a cell no.
    return enter_move(board, move, PLAYER_O)


def cli_display_last_move(move: int):
    print(f"Your opponent chose: {move}")


def cli_exit_if_winner(board, player):
    if player in PLAYERS:
        cli_display_board(board)
        print(f"{NAMES[player]} has won!")
        exit()


def cli_exit_if_draw(board):
    if is_draw(board):
        cli_display_board(board)
        print("And the game ends in a tie :(")
        exit()


def is_draw(board) -> bool:
    return len(find_free_cells(board)) < 1


def get_board_cell(board: list, move: int) -> str:
    offset = move - 1 # changes the user input to integer - 1 so the later division works correctly 
    row = offset // 3 # row = input divided by 3 then rounded down, e.g. original 6 input - 1 // 3 = 1
    col = offset % 3 # col = remainder of input divided by 3
    return board[row][col]


def set_board_cell(board: list, move: int, player: str) -> None:
    offset = move - 1
    row = offset // 3
    col = offset % 3
    board[row][col] = player
   

def enter_move(board: list, move, player: str) -> List:
    """Update the board with the latest move.

    :raises MoveError: When the move is invalid
    """
    try:
        move = int(move)
        if not (1 <= move <= 9):
            raise MoveError("Your move was outside the board bounds. Try again.")

        cell = get_board_cell(board, move)
        if cell in PLAYERS:
            raise MoveError("Cell occupied, choose another")
        set_board_cell(board, move, player)
    except MoveError:
        raise
    except:
        raise MoveError("Your move was not recognised")

    return board


def find_free_cells(board) -> List:
    cells = []
    for move in range(1,10):
        cell = get_board_cell(board, move)
        if cell not in PLAYERS:
            cells.append(cell)
    return cells

def find_winner(board: List) -> str:
    for combo in WINNING_MOVES:
        cells = [
            get_board_cell(board, combo[0]),
            get_board_cell(board, combo[1]),
            get_board_cell(board, combo[2]),
        ]
        if cells == [PLAYER_X, PLAYER_X, PLAYER_X]:
            return PLAYER_X
        elif cells == [PLAYER_O, PLAYER_O, PLAYER_O]:
            return PLAYER_O


def computer_choose_move(board) -> int:
    """Calculate move (randomly) for the computer."""
    moves = find_free_cells(board)
    if len(moves) == 0:
        return None
    elif len(moves) == 1:
        return moves[0]
    else:
        choice = randrange(0, len(moves))
        return moves[choice]


if __name__ == "__main__":
    board = init_board()

    # Computer goes first
    computer_move = 5
    board = enter_move(board, computer_move, PLAYER_X)

    cells = find_free_cells(board)
    
    while len(cells) > 0:
        cli_display_board(board)
        cli_display_last_move(computer_move)

        # Human...
        # Try again if they guess wrong
        valid_move = False
        while not valid_move:
            try:
                board = cli_enter_move(board)
            except MoveError as e:
                print(e)
                continue
            valid_move = True
        cli_exit_if_winner(board, find_winner(board))

        # Computer
        time.sleep(1)
        computer_move = computer_choose_move(board)
        board = enter_move(board, computer_move, PLAYER_X)
        cli_exit_if_winner(board, find_winner(board))

        # Update the cells for the while loop
        cli_exit_if_draw(board)
        cells = find_free_cells(board)
