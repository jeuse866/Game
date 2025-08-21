# dungeon_dice_rpg_full.py
import random
import time

def roll_die(sides=6):
    return random.randint(1, sides)

class Character:
    def __init__(self, name, hp, attack_die=6, defense_die=6):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_die = attack_die
        self.defense_die = defense_die

    def attack(self):
        roll = roll_die(self.attack_die)
        crit = False
        if random.random() <= 0.1:
            crit = True
            roll *= 2
        print(f"{self.name} rolls an attack: {roll}" + (" 🔥 Critical!" if crit else ""))
        return roll

    def defend(self):
        roll = roll_die(self.defense_die)
        crit = False
        if random.random() <= 0.1:
            crit = True
            roll *= 2
        print(f"{self.name} rolls a defense: {roll}" + (" 🛡️ Critical!" if crit else ""))
        return roll

class Player(Character):
    def __init__(self, name, hero_class):
        hp = 50
        attack_die = 6
        defense_die = 6
        super().__init__(name, hp, attack_die, defense_die)
        self.hero_class = hero_class
        self.special_used = False
        self.inventory = {"Potion": 1, "Sword": 0}

    def use_special(self):
        if self.special_used:
            print("❌ Special ability already used!")
            return 0
        self.special_used = True
        if self.hero_class == "Warrior":
            print("⚔️ Warrior Power Strike! +3 attack")
            return 3
        elif self.hero_class == "Rogue":
            print("🗡️ Rogue Sneak Attack! +5 attack if crit")
            return 0  # handled in attack roll
        elif self.hero_class == "Mage":
            print("🔥 Mage Fireball! +4 attack")
            return 4
        return 0

    def attack(self, use_special=False):
        roll = roll_die(self.attack_die)
        if use_special:
            roll += self.use_special()
        # Rogue crit bonus
        crit = False
        if random.random() <= 0.1:
            crit = True
            if self.hero_class == "Rogue":
                roll *= 2.5
            else:
                roll *= 2
        print(f"{self.name} rolls an attack: {int(roll)}" + (" 🔥 Critical!" if crit else ""))
        return int(roll)

    def heal(self):
        if self.inventory["Potion"] > 0:
            heal_amount = 20
            self.hp = min(self.max_hp, self.hp + heal_amount)
            self.inventory["Potion"] -= 1
            print(f"💖 {self.name} used a potion and healed {heal_amount} HP!")
        else:
            print("❌ No potions left!")

class Monster(Character):
    def __init__(self, name, hp, attack_die=6, defense_die=6, is_boss=False):
        super().__init__(name, hp, attack_die, defense_die)
        self.is_boss = is_boss

    def attack(self):
        if self.is_boss:
            # Boss can attack twice
            roll1 = roll_die(self.attack_die)
            roll2 = roll_die(self.attack_die)
            roll = max(roll1, roll2)
            print(f"{self.name} rolls a boss attack: {roll1} & {roll2} => {roll}")
            return roll
        return super().attack()

def fight(player, monster):
    print(f"\n⚔️ {player.name} encounters a {monster.name}!")
    time.sleep(1)
    while player.hp > 0 and monster.hp > 0:
        print(f"\n{player.name} HP: {player.hp}/{player.max_hp}")
        print(f"{monster.name} HP: {monster.hp}/{monster.max_hp}\n")

        action = input("Choose action: 'attack(a)', 'special(s)', 'heal(h)': ").lower().strip()
        if action in ["attack", "a"]:
            use_special = False
        elif action in ["special", "s"]:
            use_special = True
        elif action in ["heal", "h"]:
            player.heal()
            continue
        else:
            print("❌ Invalid action! Try again.")
            continue

        player_roll = player.attack(use_special)
        monster_def = monster.defend()
        dmg = max(0, player_roll - monster_def)
        monster.hp -= dmg
        print(f"➡️ {player.name} deals {dmg} damage!")
        time.sleep(1)

        if monster.hp <= 0:
            print(f"🏆 {player.name} defeated {monster.name}!")
            # Loot drop
            loot_chance = random.random()
            if loot_chance < 0.5:
                player.inventory["Potion"] += 1
                print("🍾 Loot: Potion added to inventory!")
            elif loot_chance < 0.8:
                player.inventory["Sword"] += 1
                player.attack_die += 1
                print("⚔️ Loot: Sword! Attack die +1")
            break

        input("Press Enter for monster attack...")
        monster_roll = monster.attack()
        player_def = player.defend()
        dmg = max(0, monster_roll - player_def)
        player.hp -= dmg
        print(f"⬅️ {monster.name} deals {dmg} damage!")
        time.sleep(1)

        if player.hp <= 0:
            print(f"💀 {player.name} was defeated by {monster.name}!")
            break

def dungeon_run():
    print("🏰 Welcome to Dungeon Dice RPG!")
    name = input("Enter your hero's name: ")
    print("Choose a class: Warrior, Rogue, Mage")
    while True:
        hero_class = input("Class: ").capitalize()
        if hero_class in ["Warrior", "Rogue", "Mage"]:
            break
        print("❌ Invalid class!")
    player = Player(name, hero_class)

    monsters = [
        Monster("Goblin", 20),
        Monster("Skeleton", 25),
        Monster("Orc", 30),
        Monster("Troll", 35),
        Monster("Dragon Boss", 50, attack_die=8, is_boss=True)
    ]

    for monster in monsters:
        fight(player, monster)
        if player.hp <= 0:
            print("\n💔 Your dungeon run is over!")
            break
        else:
            # Heal a bit between battles
            heal = min(10, player.max_hp - player.hp)
            player.hp += heal
            print(f"💖 {player.name} recovers {heal} HP before next fight!")
            player.special_used = False
            time.sleep(1)

    print("\n🎉 Dungeon run complete!")
    print(f"Inventory: {player.inventory}")

def main():
    while True:
        dungeon_run()
        again = input("\nPlay another dungeon run? (y/n): ").lower().strip()
        if again != "y":
            print("Thanks for playing Dungeon Dice RPG Full Edition!")
            break

if __name__ == "__main__":
    main()
