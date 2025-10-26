#!/usr/bin/env python3
"""
Interactive Text Adventure Game
A terminal-based adventure where players explore rooms, solve puzzles, and defeat enemies.
"""

import random
import sys


class Item:
    """Represents an item in the game."""
    
    def __init__(self, name, description, takeable=True):
        self.name = name
        self.description = description
        self.takeable = takeable
    
    def __str__(self):
        return self.name


class Room:
    """Represents a room in the game world."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.items = []
        self.north = None
        self.south = None
        self.north_door_locked = False
        self.visited = False
    
    def get_full_description(self):
        """Returns the full room description including items."""
        desc = f"\n=== {self.name} ===\n{self.description}\n"
        
        if self.items:
            desc += "\nYou can see:\n"
            for item in self.items:
                desc += f"  - A {item.name}\n"
        
        # Show available exits
        exits = []
        if self.north:
            exits.append("north")
        if self.south:
            exits.append("south")
        
        if exits:
            desc += f"\nExits: {', '.join(exits)}"
        
        return desc
    
    def add_item(self, item):
        """Adds an item to the room."""
        self.items.append(item)
    
    def remove_item(self, item_name):
        """Removes an item from the room by name."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                return item
        return None
    
    def get_item(self, item_name):
        """Gets an item from the room by name without removing it."""
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None


class Player:
    """Represents the player character."""
    
    def __init__(self):
        self.inventory = []
        self.health = 20
        self.max_health = 20
        self.min_damage = 1
        self.max_damage = 6
    
    def add_item(self, item):
        """Adds an item to inventory."""
        self.inventory.append(item)
    
    def has_item(self, item_name):
        """Checks if player has an item."""
        return any(item.name.lower() == item_name.lower() for item in self.inventory)
    
    def get_item(self, item_name):
        """Gets an item from inventory."""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
    def show_inventory(self):
        """Returns inventory as a string."""
        if not self.inventory:
            return "\nYour inventory is empty."
        
        inv_str = "\n=== Inventory ===\n"
        for item in self.inventory:
            inv_str += f"  - {item.name}\n"
        return inv_str
    
    def attack(self):
        """Returns damage dealt by player."""
        return random.randint(self.min_damage, self.max_damage)
    
    def take_damage(self, damage):
        """Reduces player health."""
        self.health -= damage
        if self.health < 0:
            self.health = 0


class Enemy:
    """Represents an enemy in combat."""
    
    def __init__(self, name, health, min_damage, max_damage):
        self.name = name
        self.health = health
        self.max_health = health
        self.min_damage = min_damage
        self.max_damage = max_damage
    
    def attack(self):
        """Returns damage dealt by enemy."""
        return random.randint(self.min_damage, self.max_damage)
    
    def take_damage(self, damage):
        """Reduces enemy health."""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def is_alive(self):
        """Checks if enemy is still alive."""
        return self.health > 0


class Game:
    """Main game controller."""
    
    def __init__(self):
        self.player = Player()
        self.current_room = None
        self.rooms = {}
        self.door_unlocked = False
        self.password = "SHADOW"  # The correct password
        self.game_over = False
        self.game_won = False
        self.in_combat = False
        self.enemy = None
        self.enemy_defeated = False
        
        self.setup_game()
    
    def setup_game(self):
        """Sets up the game world."""
        # Create rooms
        room1 = Room(
            "Starting Chamber",
            "You find yourself in a dimly lit stone chamber. The walls are cold and damp.\n"
            "A heavy wooden door stands to the north."
        )
        
        room2 = Room(
            "Treasury Room",
            "You enter a magnificent treasury filled with ancient artifacts and golden treasures.\n"
            "The room sparkles with an otherworldly glow."
        )
        
        room3 = Room(
            "Enemy Arena",
            "You step into a vast arena. The air is thick with tension.\n"
            "A menacing shadow moves in the darkness ahead!"
        )
        
        # Create items
        key = Item("key", "A rusty iron key")
        note = Item("note", "A weathered piece of parchment with writing on it", takeable=False)
        
        # Place items in rooms
        room1.add_item(key)
        room2.add_item(note)
        
        # Connect rooms
        room1.north = room2
        room1.north_door_locked = True
        
        room2.south = room1
        room2.north = room3
        
        room3.south = room2
        
        # Store rooms
        self.rooms = {
            "room1": room1,
            "room2": room2,
            "room3": room3
        }
        
        # Set starting room
        self.current_room = room1
    
    def show_intro(self):
        """Displays the game introduction."""
        print("\n" + "="*60)
        print("         WELCOME TO THE SHADOW DUNGEON")
        print("="*60)
        print("\nYou awaken in a mysterious chamber with no memory of how you")
        print("arrived here. Your only choice is to venture forward and")
        print("discover what lies ahead...")
        print("\nType 'help' for a list of commands.")
        print("="*60)
        print(self.current_room.get_full_description())
    
    def show_help(self):
        """Displays available commands."""
        help_text = """
=== Available Commands ===

Navigation:
  go north / go south  - Move between rooms
  look                 - Examine current room

Interaction:
  take key             - Pick up the key
  pick up key          - Pick up the key
  read note            - Read the note
  examine note         - Read the note
  inventory / i        - Check your items
  unlock door with [password] - Unlock the door
  open door            - Open the door

Combat:
  attack               - Attack the enemy

Utility:
  help                 - Show this help message
  quit                 - Exit game
"""
        print(help_text)
    
    def process_command(self, command):
        """Processes player commands."""
        command = command.lower().strip()
        
        if not command:
            return
        
        # Combat commands
        if self.in_combat:
            if command == "attack":
                self.combat_turn()
            else:
                print("\nYou're in combat! You can only 'attack' or 'quit'.")
            return
        
        # Parse command
        parts = command.split()
        action = parts[0] if parts else ""
        
        # Utility commands
        if command == "help":
            self.show_help()
        
        elif command in ["quit", "exit", "q"]:
            print("\nThanks for playing! Goodbye.")
            self.game_over = True
        
        # Navigation commands
        elif command.startswith("go "):
            direction = command[3:].strip()
            self.move(direction)
        
        elif command == "look":
            print(self.current_room.get_full_description())
        
        # Inventory
        elif command in ["inventory", "i"]:
            print(self.player.show_inventory())
        
        # Item interaction
        elif command in ["take key", "pick up key", "get key"]:
            self.take_key()
        
        elif command in ["read note", "examine note", "look at note"]:
            self.read_note()
        
        # Door interaction
        elif command.startswith("unlock door with "):
            password = command[17:].strip().upper()
            self.unlock_door(password)
        
        elif command in ["open door", "open north door"]:
            self.open_door()
        
        else:
            print("\nI don't understand that command. Type 'help' for available commands.")
    
    def move(self, direction):
        """Handles room navigation."""
        direction = direction.lower()
        
        if direction == "north":
            if self.current_room.north:
                # Check if door is locked
                if self.current_room.north_door_locked:
                    print("\nThe door is locked. You need to unlock it first.")
                    return
                
                self.current_room = self.current_room.north
                print(self.current_room.get_full_description())
                
                # Check if entering Room 3 (Enemy Arena)
                if self.current_room.name == "Enemy Arena" and not self.enemy_defeated:
                    self.start_combat()
            else:
                print("\nYou can't go that way.")
        
        elif direction == "south":
            if self.current_room.south:
                self.current_room = self.current_room.south
                print(self.current_room.get_full_description())
            else:
                print("\nYou can't go that way.")
        
        else:
            print("\nYou can only go 'north' or 'south'.")
    
    def take_key(self):
        """Handles taking the key."""
        key = self.current_room.get_item("key")
        if key:
            self.current_room.remove_item("key")
            self.player.add_item(key)
            print("\nYou pick up the rusty iron key and add it to your inventory.")
        else:
            print("\nThere's no key here.")
    
    def read_note(self):
        """Handles reading the note."""
        note = self.current_room.get_item("note")
        if note:
            print(f"\nYou read the note:")
            print("="*40)
            print(f"  The password is: {self.password}")
            print("="*40)
        else:
            print("\nThere's no note here to read.")
    
    def unlock_door(self, password):
        """Handles unlocking the door with a password."""
        if self.door_unlocked:
            print("\nThe door is already unlocked.")
            return
        
        if not self.player.has_item("key"):
            print("\nYou don't have a key.")
            return
        
        if password == self.password:
            print("\nThe door unlocks with a click! You can now go north.")
            self.door_unlocked = True
            self.rooms["room1"].north_door_locked = False
        else:
            print("\nThe password is incorrect.")
    
    def open_door(self):
        """Handles opening the door."""
        if self.current_room.name == "Starting Chamber":
            if self.door_unlocked or not self.current_room.north_door_locked:
                print("\nThe door is already open. You can go north.")
            else:
                print("\nThe door is locked. You need to unlock it first.")
        else:
            print("\nThere's no door to open here.")
    
    def start_combat(self):
        """Initiates combat with the enemy."""
        print("\n" + "!"*60)
        print("  A DARK WARRIOR EMERGES FROM THE SHADOWS!")
        print("!"*60)
        print("\nThe enemy blocks your path. You must fight!")
        
        self.enemy = Enemy("Dark Warrior", 10, 1, 4)
        self.in_combat = True
        
        print(f"\nEnemy Health: {self.enemy.health}/{self.enemy.max_health} HP")
        print(f"Your Health: {self.player.health}/{self.player.max_health} HP")
        print("\nType 'attack' to fight!")
    
    def combat_turn(self):
        """Handles a turn of combat."""
        if not self.enemy or not self.in_combat:
            return
        
        # Player attacks first
        player_damage = self.player.attack()
        self.enemy.take_damage(player_damage)
        
        print(f"\nYou attack the {self.enemy.name} for {player_damage} damage!")
        print(f"Enemy Health: {self.enemy.health}/{self.enemy.max_health} HP")
        
        # Check if enemy is defeated
        if not self.enemy.is_alive():
            print("\n" + "="*60)
            print("  VICTORY!")
            print("="*60)
            print(f"\nYou defeated the {self.enemy.name}!")
            print("\n🎉 CONGRATULATIONS! YOU WIN! 🎉")
            print("\nYou have conquered the Shadow Dungeon!")
            print("="*60)
            
            self.in_combat = False
            self.enemy_defeated = True
            self.game_won = True
            self.game_over = True
            return
        
        # Enemy attacks
        enemy_damage = self.enemy.attack()
        self.player.take_damage(enemy_damage)
        
        print(f"\nThe {self.enemy.name} strikes back for {enemy_damage} damage!")
        print(f"Your Health: {self.player.health}/{self.player.max_health} HP")
        
        # Check if player is defeated
        if self.player.health <= 0:
            print("\n" + "="*60)
            print("  DEFEAT!")
            print("="*60)
            print("\nYou have been defeated. Game Over.")
            print("\nThe darkness consumes you...")
            print("="*60)
            
            self.in_combat = False
            self.game_over = True
            return
        
        print("\nWhat will you do?")
    
    def run(self):
        """Main game loop."""
        self.show_intro()
        
        while not self.game_over:
            try:
                command = input("\n> ").strip()
                self.process_command(command)
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
            except EOFError:
                print("\n\nGame ended. Thanks for playing!")
                break


def main():
    """Entry point for the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

