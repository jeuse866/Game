# battleship_mini.py
import random

BOARD_SIZE = 5
SHIP_SIZES = [2, 2, 2]  # Three ships, each size 2
MAX_TURNS = 10

def create_board():
    return [["~"] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def print_board(board, hide_ships=False):
    print("  " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for idx, row in enumerate(board):
        display_row = []
        for cell in row:
            if hide_ships and cell == "S":
                display_row.append("~")
            else:
                display_row.append(cell)
        print(f"{idx} " + " ".join(display_row))

def place_ships(board):
    ships = []
    for size in SHIP_SIZES:
        placed = False
        while not placed:
            orientation = random.choice(["H", "V"])
            if orientation == "H":
                row = random.randint(0, BOARD_SIZE - 1)
                col = random.randint(0, BOARD_SIZE - size)
                if all(board[row][col+i] == "~" for i in range(size)):
                    for i in range(size):
                        board[row][col+i] = "S"
                    ships.append({"positions": [(row, col+i) for i in range(size)], "hits": 0})
                    placed = True
            else:  # Vertical
                row = random.randint(0, BOARD_SIZE - size)
                col = random.randint(0, BOARD_SIZE - 1)
                if all(board[row+i][col] == "~" for i in range(size)):
                    for i in range(size):
                        board[row+i][col] = "S"
                    ships.append({"positions": [(row+i, col) for i in range(size)], "hits": 0})
                    placed = True
    return ships

def check_sunk(ship):
    return ship["hits"] == len(ship["positions"])

def play_game():
    print("🚢 Welcome to Mini Battleship!")
    hidden_board = create_board()
    guess_board = create_board()
    ships = place_ships(hidden_board)
    hits_needed = sum(SHIP_SIZES)

    turns = 0
    hits = 0
    ships_remaining = len(ships)

    while turns < MAX_TURNS:
        print(f"\nTurn {turns + 1} of {MAX_TURNS}")
        print_board(guess_board)

        try:
            row = int(input(f"Guess Row (0-{BOARD_SIZE-1}): "))
            col = int(input(f"Guess Col (0-{BOARD_SIZE-1}): "))
        except ValueError:
            print("❌ Please enter numbers only.")
            continue

        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            print("❌ Out of bounds. Try again.")
            continue

        if guess_board[row][col] != "~":
            print("⚠️ You already guessed that spot.")
            continue

        # Check hit
        hit_ship = None
        for ship in ships:
            if (row, col) in ship["positions"]:
                hit_ship = ship
                break

        if hit_ship:
            print("🎯 Hit! (Free shot, no turn lost)")
            guess_board[row][col] = "X"
            hits += 1
            hit_ship["hits"] += 1
            if check_sunk(hit_ship):
                ships_remaining -= 1
                print(f"💥 You sunk a ship! 🚢 Ships left: {ships_remaining}")
                if ships_remaining == 0:
                    print("\n🏆 You sank all the ships! You win!")
                    return  # End game immediately
        else:
            print("🌊 Miss!")
            guess_board[row][col] = "O"
            turns += 1  # Only misses cost turns

    # Game over (ran out of turns)
    print("\n💀 Out of turns. You lose.")
    print("The enemy ships were at:")
    print_board(hidden_board)

def main():
    while True:
        play_game()
        again = input("\nPlay again? [y/n]: ").lower().strip()
        if again != "y":
            print("Thanks for playing Mini Battleship!")
            break

if __name__ == "__main__":
    main()
