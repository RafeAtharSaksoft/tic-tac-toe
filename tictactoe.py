"""CLI Tic-Tac-Toe for two players (Python 3). No external dependencies."""

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
    (0, 4, 8), (2, 4, 6),              # diagonals
]


def new_board():
    return [str(i + 1) for i in range(9)]


def render(board):
    rows = [
        f" {board[0]} | {board[1]} | {board[2]} ",
        "---+---+---",
        f" {board[3]} | {board[4]} | {board[5]} ",
        "---+---+---",
        f" {board[6]} | {board[7]} | {board[8]} ",
    ]
    return "\n".join(rows)


def check_winner(board):
    for a, b, c in WIN_LINES:
        if board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board):
    return all(cell in ("X", "O") for cell in board)


def apply_move(board, position, player):
    try:
        pos = int(position)
    except (ValueError, TypeError):
        raise ValueError(f"'{position}' is not a valid number. Enter 1-9.")

    if pos < 1 or pos > 9:
        raise ValueError(f"{pos} is out of range. Enter 1-9.")

    if board[pos - 1] in ("X", "O"):
        raise ValueError(f"Position {pos} is already taken. Choose another.")

    updated = board[:]
    updated[pos - 1] = player
    return updated


def next_player(current):
    return "O" if current == "X" else "X"


def main():
    board = new_board()
    player = "X"

    print(render(board))

    while True:
        raw = input(f"\nPlayer {player}, enter position (1-9): ").strip()

        try:
            board = apply_move(board, raw, player)
        except ValueError as exc:
            print(f"Invalid input: {exc}")
            continue

        print("\n" + render(board))

        winner = check_winner(board)
        if winner:
            print(f"\nPlayer {winner} wins!")
            raise SystemExit(0)

        if is_draw(board):
            print("\nIt's a draw!")
            raise SystemExit(0)

        player = next_player(player)


if __name__ == "__main__":
    main()
