# blackjack_betting.py
import random
import sys

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
VALUES = {**{str(n): n for n in range(2, 11)}, **{"J": 10, "Q": 10, "K": 10, "A": 11}}

def new_deck(num_decks=1):
    deck = [(r, s) for r in RANKS for s in SUITS] * num_decks
    random.shuffle(deck)
    return deck

def hand_value(hand):
    total = sum(VALUES[r] for r, _ in hand)
    aces = sum(1 for r, _ in hand if r == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def show_hand(name, hand, hide_first=False):
    if hide_first:
        print(f"{name}: [??] " + " ".join(f"{r}{s}" for r, s in hand[1:]))
    else:
        print(f"{name}: " + " ".join(f"{r}{s}" for r, s in hand) + f"  (total: {hand_value(hand)})")

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def play_hand(deck, player_hand, dealer, balance, bet):
    # Player’s turn
    doubled = False
    while True:
        move = input("Hit, Stand, or Double? [h/s/d] ").strip().lower()
        if move in ("h", "hit"):
            player_hand.append(deck.pop())
            show_hand("You", player_hand)
            if hand_value(player_hand) > 21:
                print("Bust! You lose this hand.")
                return balance - bet
        elif move in ("s", "stand"):
            break
        elif move in ("d", "double") and len(player_hand) == 2 and balance >= bet * 2:
            bet *= 2
            doubled = True
            player_hand.append(deck.pop())
            show_hand("You", player_hand)
            if hand_value(player_hand) > 21:
                print("Bust after doubling! You lose this hand.")
                return balance - bet
            break
        else:
            print("Invalid move.")
    
    # Dealer’s turn
    print("\nDealer's turn:")
    show_hand("Dealer", dealer)
    while hand_value(dealer) < 17:
        dealer.append(deck.pop())
        show_hand("Dealer", dealer)

    p_total = hand_value(player_hand)
    d_total = hand_value(dealer)

    if d_total > 21 or p_total > d_total:
        print("You win this hand!")
        return balance + bet
    elif p_total < d_total:
        print("Dealer wins this hand.")
        return balance - bet
    else:
        print("Push (tie).")
        return balance

def play_round(deck, balance):
    if balance <= 0:
        print("You’re out of money! Game over.")
        sys.exit()

    # Place bet
    while True:
        try:
            bet = int(input(f"\nYou have ${balance}. Enter your bet: "))
            if 1 <= bet <= balance:
                break
            else:
                print("Invalid bet amount.")
        except ValueError:
            print("Enter a number.")

    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print("\n=== New Round ===")
    show_hand("Dealer", dealer, hide_first=True)
    show_hand("You", player)

    # Check for natural blackjack
    if is_blackjack(player) or is_blackjack(dealer):
        show_hand("Dealer", dealer)
        if is_blackjack(player) and is_blackjack(dealer):
            print("Push! Both have Blackjack.")
            return balance
        elif is_blackjack(player):
            print("Blackjack! You win 1.5x your bet!")
            return balance + int(1.5 * bet)
        else:
            print("Dealer has Blackjack. You lose.")
            return balance - bet

    # Splits
    if player[0][0] == player[1][0]:
        split = input("You have a pair! Do you want to split? [y/n] ").strip().lower()
        if split == "y" and balance >= bet * 2:
            hand1 = [player[0], deck.pop()]
            hand2 = [player[1], deck.pop()]
            print("\nPlaying first split hand:")
            show_hand("You", hand1)
            balance = play_hand(deck, hand1, dealer.copy(), balance, bet)
            print("\nPlaying second split hand:")
            show_hand("You", hand2)
            balance = play_hand(deck, hand2, dealer.copy(), balance, bet)
            return balance

    # Normal play
    return play_hand(deck, player, dealer, balance, bet)

def main():
    print("Welcome to Blackjack with Betting, Double Down, and Splits!")
    deck = new_deck(4)
    balance = 500  # starting money

    while True:
        balance = play_round(deck, balance)
        print(f"\nYour balance: ${balance}")
        again = input("Play again? [y/n] ").strip().lower()
        if again not in ("y", "yes"):
            print(f"Cash out with ${balance}. Thanks for playing!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)

