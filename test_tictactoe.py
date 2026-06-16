import pytest
from tictactoe import (
    WIN_LINES,
    apply_move,
    check_winner,
    is_draw,
    new_board,
    next_player,
    render,
)


# --- new_board ---

def test_new_board_has_9_cells():
    assert len(new_board()) == 9


def test_new_board_positions_1_to_9():
    assert new_board() == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


# --- render: AC-1 (positions 1-9 visible on start) ---

def test_render_shows_positions_1_to_9():
    output = render(new_board())
    for i in range(1, 10):
        assert str(i) in output


def test_render_shows_placed_marks():
    board = new_board()
    board[0] = "X"
    board[4] = "O"
    output = render(board)
    assert "X" in output
    assert "O" in output


# --- check_winner: all 8 win lines ---

WIN_LINE_PARAMS = [
    (0, 1, 2, "top row"),
    (3, 4, 5, "middle row"),
    (6, 7, 8, "bottom row"),
    (0, 3, 6, "left col"),
    (1, 4, 7, "mid col"),
    (2, 5, 8, "right col"),
    (0, 4, 8, "main diagonal"),
    (2, 4, 6, "anti diagonal"),
]


@pytest.mark.parametrize("a,b,c,desc", WIN_LINE_PARAMS)
def test_check_winner_x_wins_each_line(a, b, c, desc):
    board = new_board()
    board[a] = board[b] = board[c] = "X"
    assert check_winner(board) == "X", f"X should win on {desc}"


@pytest.mark.parametrize("a,b,c,desc", WIN_LINE_PARAMS)
def test_check_winner_o_wins_each_line(a, b, c, desc):
    board = new_board()
    board[a] = board[b] = board[c] = "O"
    assert check_winner(board) == "O", f"O should win on {desc}"


def test_check_winner_no_winner_on_empty_board():
    assert check_winner(new_board()) is None


def test_check_winner_no_winner_partial_board():
    board = new_board()
    board[0] = "X"
    board[1] = "O"
    assert check_winner(board) is None


# --- is_draw: AC-6 ---

def test_is_draw_full_board_no_winner():
    # X O X / O X O / O X O — draw (X wins centre col, but main purpose is draw test)
    # Use a genuine draw arrangement: no three in a row
    board = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
    assert check_winner(board) is None
    assert is_draw(board) is True


def test_is_draw_not_full():
    assert is_draw(new_board()) is False


def test_is_draw_partially_filled():
    board = new_board()
    board[0] = "X"
    assert is_draw(board) is False


# --- apply_move: AC-3, AC-4 ---

def test_apply_move_places_mark():
    board = new_board()
    result = apply_move(board, "5", "X")
    assert result[4] == "X"


def test_apply_move_does_not_mutate_original():
    board = new_board()
    apply_move(board, "1", "X")
    assert board[0] == "1"


def test_apply_move_non_numeric_input():
    with pytest.raises(ValueError, match="not a valid number"):
        apply_move(new_board(), "abc", "X")


def test_apply_move_empty_string():
    with pytest.raises(ValueError):
        apply_move(new_board(), "", "X")


def test_apply_move_float_string():
    with pytest.raises(ValueError, match="not a valid number"):
        apply_move(new_board(), "1.5", "X")


def test_apply_move_out_of_range_high():
    with pytest.raises(ValueError, match="out of range"):
        apply_move(new_board(), "10", "X")


def test_apply_move_out_of_range_zero():
    with pytest.raises(ValueError, match="out of range"):
        apply_move(new_board(), "0", "X")


def test_apply_move_negative():
    with pytest.raises(ValueError, match="out of range"):
        apply_move(new_board(), "-1", "X")


def test_apply_move_occupied_cell():
    board = new_board()
    board[4] = "O"
    with pytest.raises(ValueError, match="already taken"):
        apply_move(board, "5", "X")


# --- next_player: AC-7 (strictly alternating, X first) ---

def test_next_player_x_gives_o():
    assert next_player("X") == "O"


def test_next_player_o_gives_x():
    assert next_player("O") == "X"


def test_turns_alternate_starting_with_x():
    player = "X"
    sequence = [player]
    for _ in range(5):
        player = next_player(player)
        sequence.append(player)
    assert sequence == ["X", "O", "X", "O", "X", "O"]
