# rps.py
import random

CHOICES = ["rock", "paper", "scissors"]

def play_round():
    player = input("Choose Rock, Paper, or Scissors: ").lower().strip()
    if player not in CHOICES:
        print("❌ Invalid choice. Try again.")
        return None

    computer = random.choice(CHOICES)
    print(f"🖥️ Computer chose: {computer.capitalize()}")

    if player == computer:
        print("🤝 It's a tie!")
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        print("🎉 You win!")
    else:
        print("💀 You lose.")

def main():
    print("Welcome to Rock, Paper, Scissors!")
    while True:
        play_round()
        again = input("Play again? [y/n]: ").lower().strip()
        if again != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
