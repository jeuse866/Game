# tic_tac_toe_ai.py
import random

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
    print("\n")

def check_winner(board, player):
    # Check rows
    for row in board:
        if all(s == player for s in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_cells(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def play_game():
    board = [[" "] * 3 for _ in range(3)]
    human = "X"
    computer = "O"

    print("🎮 Welcome to Tic Tac Toe!")
    print("You are X, the computer is O.")

    while True:
        # Human turn
        print_board(board)
        print("Your turn.")
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
        except ValueError:
            print("❌ Please enter valid numbers.")
            continue

        if not (0 <= row < 3 and 0 <= col < 3):
            print("❌ Out of bounds, try again.")
            continue

        if board[row][col] != " ":
            print("⚠️ That spot is already taken.")
            continue

        board[row][col] = human

        if check_winner(board, human):
            print_board(board)
            print("🎉 You win!")
            break

        if is_full(board):
            print_board(board)
            print("🤝 It's a tie!")
            break

        # Computer turn
        print("Computer's turn...")
        row, col = random.choice(get_empty_cells(board))
        board[row][col] = computer

        if check_winner(board, computer):
            print_board(board)
            print("💻 Computer wins!")
            break

        if is_full(board):
            print_board(board)
            print("🤝 It's a tie!")
            break

def main():
    while True:
        play_game()
        again = input("Play again? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing Tic Tac Toe!")
            break

if __name__ == "__main__":
    main()
