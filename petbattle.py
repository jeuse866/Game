# pet_battle_campaign_two_elements.py
import random
import time

ELEMENTS = ["Fire", "Water", "Grass"]

def type_effectiveness(move_type, target_type):
    if (move_type == "Fire" and target_type == "Grass") or \
       (move_type == "Grass" and target_type == "Water") or \
       (move_type == "Water" and target_type == "Fire"):
        return 1.5  # super effective
    elif (move_type == "Fire" and target_type == "Water") or \
         (move_type == "Grass" and target_type == "Fire") or \
         (move_type == "Water" and target_type == "Grass"):
        return 0.5  # not effective
    return 1  # normal

class Pet:
    def __init__(self, name, element1, element2, level=1):
        self.name = name
        self.element1 = element1
        self.element2 = element2
        self.level = level
        self.max_hp = 100 + (level - 1) * 10
        self.hp = self.max_hp
        self.xp = 0
        self.moves = {
            f"{element1} Attack": {"power": 12, "type": element1},
            f"{element2} Attack": {"power": 12, "type": element2}
        }

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        print(f"🎉 {self.name} leveled up! Now level {self.level}.")

def print_status(player, enemy):
    print(f"\n{player.name} ({player.element1}/{player.element2}) - {player.hp}/{player.max_hp} HP")
    print(f"{enemy.name} ({enemy.element1}) - {enemy.hp}/{enemy.max_hp} HP\n")

def player_turn(player, enemy):
    print("Choose your move:")
    for i, move in enumerate(player.moves, 1):
        print(f"{i}. {move} ({player.moves[move]['type']}, Power {player.moves[move]['power']})")

    while True:
        try:
            choice = int(input("Enter move number: "))
            move_name = list(player.moves.keys())[choice - 1]
            break
        except (ValueError, IndexError):
            print("❌ Invalid choice, try again.")

    move = player.moves[move_name]
    effectiveness = type_effectiveness(move["type"], enemy.element1)
    dmg = int(move["power"] * effectiveness * random.uniform(0.85, 1.15))
    enemy.hp -= dmg
    enemy.hp = max(0, enemy.hp)

    if effectiveness > 1:
        eff_msg = "It's super effective!"
    elif effectiveness < 1:
        eff_msg = "It's not very effective..."
    else:
        eff_msg = ""

    print(f"🪶 {player.name} used {move_name} and dealt {dmg} damage! {eff_msg}")

def enemy_turn(enemy, player):
    # Smart AI: choose super effective move if available
    best_move = None
    best_effect = 0
    for move_name, move in enemy.moves.items():
        effect = type_effectiveness(move["type"], player.element1)
        if effect > best_effect:
            best_effect = effect
            best_move = move_name

    if not best_move:
        best_move = random.choice(list(enemy.moves.keys()))

    move = enemy.moves[best_move]
    effectiveness = type_effectiveness(move["type"], player.element1)
    dmg = int(move["power"] * effectiveness * random.uniform(0.85, 1.15))
    player.hp -= dmg
    player.hp = max(0, player.hp)

    if effectiveness > 1:
        eff_msg = "It's super effective!"
    elif effectiveness < 1:
        eff_msg = "It's not very effective..."
    else:
        eff_msg = ""

    print(f"💻 {enemy.name} used {best_move} and dealt {dmg} damage! {eff_msg}")

def battle(player, enemy):
    print(f"\n🎮 Battle Start! {player.name} ({player.element1}/{player.element2}) vs {enemy.name} ({enemy.element1})")
    time.sleep(1)

    turn = random.choice(["player", "enemy"])

    while player.hp > 0 and enemy.hp > 0:
        print_status(player, enemy)
        time.sleep(0.5)

        if turn == "player":
            player_turn(player, enemy)
            turn = "enemy"
        else:
            enemy_turn(enemy, player)
            turn = "player"
        time.sleep(1)

    print_status(player, enemy)
    if player.hp > 0:
        print(f"🏆 You defeated {enemy.name}! Gained 50 XP.")
        player.xp += 50
        if player.xp >= 100:
            player.level_up()
            player.xp -= 100
        return True
    else:
        print(f"💀 {player.name} was defeated by {enemy.name}!")
        return False

def play_campaign():
    player_name = input("Enter your pet's name: ")
    element1, element2 = random.sample(ELEMENTS, 2)
    player = Pet(player_name, element1, element2)

    num_battles = 5
    for i in range(1, num_battles + 1):
        print(f"\n⚔️ Battle {i} of {num_battles}")
        enemy_name = f"Wild Monster {i}"
        enemy_element = random.choice(ELEMENTS)
        enemy_level = random.randint(max(1, player.level - 1), player.level + 1)
        enemy = Pet(enemy_name, enemy_element, enemy_element, level=enemy_level)

        if not battle(player, enemy):
            print("\n💔 Campaign over!")
            break
        else:
            heal = int(player.max_hp * 0.3)
            player.hp = min(player.max_hp, player.hp + heal)
            print(f"💖 {player.name} healed {heal} HP between battles!")

    print("\n🎉 Campaign finished!")
    print(f"{player.name} reached level {player.level} with {player.xp} XP.")

def main():
    while True:
        play_campaign()
        again = input("\nPlay another campaign? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing Pet Battle Campaign RPG!")
            break

if __name__ == "__main__":
    main()
