# Interactive Text Adventure Game

A terminal-based text adventure game written in Python where players explore rooms, solve puzzles, collect items, and defeat an enemy to win.

## 🎮 Game Overview

You awaken in a mysterious dungeon with no memory of how you got there. Your goal is to explore the rooms, solve puzzles, and defeat the dark warrior to escape!

### Game Features
- 🏰 Three interconnected rooms to explore
- 🗝️ Item collection and inventory system
- 🔐 Door puzzle requiring a key and password
- ⚔️ Turn-based combat system
- 💪 Health and damage mechanics
- 🎲 Random damage calculation for dynamic combat

## 🚀 Installation & Setup

### Prerequisites
- Python 3.6 or higher

### Running the Game

1. Clone or download this repository
2. Navigate to the game directory:
   ```bash
   cd Interactive-Text-Adventure-Game
   ```
3. Run the game:
   ```bash
   python3 adventure_game.py
   ```
   or
   ```bash
   python adventure_game.py
   ```

## 🎯 How to Play

### Objective
- Explore the dungeon
- Solve the door puzzle
- Defeat the enemy in the final room
- **Win Condition**: Defeat the Dark Warrior
- **Lose Condition**: Your health reaches 0

### Room Layout
```
[Room 1: Starting Chamber]
         |
    (Locked Door)
         |
[Room 2: Treasury Room]
         |
    (Open Door)
         |
[Room 3: Enemy Arena]
```

## 🎮 Commands

### Navigation
- `go north` / `go south` - Move between rooms
- `look` - Examine your current room and see available items and exits

### Item Interaction
- `take key` / `pick up key` - Pick up the key from the ground
- `read note` / `examine note` - Read the note to learn the password
- `inventory` / `i` - Check what items you're carrying

### Door Puzzle
- `unlock door with [password]` - Attempt to unlock the door (requires key)
- `open door` - Open the door (if already unlocked)

### Combat
- `attack` - Attack the enemy during combat

### Utility
- `help` - Display available commands
- `quit` - Exit the game

## 🗺️ Walkthrough

### Quick Guide
1. **Starting Chamber (Room 1)**
   - Look around the room
   - `take key` to pick up the key
   - Try to go north (door is locked)
   - You need a password!

2. **Getting Through the Locked Door**
   - You can try random passwords, but you'll need to find the correct one
   - The password is in Room 2, but you need to unlock the door first
   - **Hint**: The password is `SHADOW`
   - Use: `unlock door with SHADOW`
   - Once unlocked: `go north`

3. **Treasury Room (Room 2)**
   - `read note` to see the password (useful if you didn't guess it earlier)
   - You can go back south to Room 1 or proceed north to Room 3
   - `go north` when ready for combat

4. **Enemy Arena (Room 3)**
   - Combat begins automatically when you enter
   - Use `attack` to fight the Dark Warrior
   - Keep attacking until you win or lose
   - Victory means you've beaten the game!

## ⚔️ Combat System

### Player Stats
- **Starting Health**: 20 HP
- **Damage Range**: 1-6 HP per attack

### Enemy Stats (Dark Warrior)
- **Health**: 10 HP
- **Damage Range**: 1-4 HP per attack

### Combat Flow
1. Combat starts automatically when entering Room 3
2. Player attacks first each turn
3. Enemy retaliates if still alive
4. Continue until one combatant reaches 0 HP
5. Victory or defeat message is displayed

## 📋 Game Features Details

### Inventory System
- Persistent across rooms
- Can carry multiple items
- View anytime with `inventory` or `i` command

### Door Puzzle System
- Requires both the **key** (found in Room 1) and the **password** (found in Room 2)
- Door remains unlocked once opened
- Helpful error messages guide you through the process

### State Persistence
- Health carries throughout the game
- Items stay in inventory once collected
- Doors stay unlocked once opened
- Defeated enemies don't respawn

## 🎲 Game Tips

1. **Explore thoroughly** - Use `look` in each room to see what's available
2. **Check your inventory** - Keep track of what you've collected
3. **Read everything** - The note contains crucial information
4. **Save your health** - You only have 20 HP for the final battle
5. **Combat is random** - Damage varies, so each playthrough is different

## 🛠️ Technical Details

### Code Structure
- **Object-Oriented Design**: Clean separation of concerns with dedicated classes
- **Classes**:
  - `Game`: Main game controller and loop
  - `Player`: Player stats, inventory, and actions
  - `Room`: Room properties, items, and connections
  - `Item`: Item properties and behaviors
  - `Enemy`: Enemy stats and combat actions

### Input Handling
- All commands are case-insensitive
- Extra whitespace is automatically trimmed
- Invalid commands provide helpful feedback
- Graceful handling of keyboard interrupts

## 📝 Example Gameplay

```
> look
=== Starting Chamber ===
You find yourself in a dimly lit stone chamber...
You can see:
  - A key

> take key
You pick up the rusty iron key and add it to your inventory.

> unlock door with SHADOW
The door unlocks with a click! You can now go north.

> go north
=== Treasury Room ===
You enter a magnificent treasury...

> read note
You read the note:
========================================
  The password is: SHADOW
========================================

> go north
=== Enemy Arena ===
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  A DARK WARRIOR EMERGES FROM THE SHADOWS!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

> attack
You attack the Dark Warrior for 5 damage!
Enemy Health: 5/10 HP

The Dark Warrior strikes back for 2 damage!
Your Health: 18/20 HP
```

## 🐛 Troubleshooting

### Common Issues
- **"command not found"**: Make sure Python 3 is installed (`python3 --version`)
- **Permission denied**: Try `chmod +x adventure_game.py` to make it executable
- **Module not found**: The game uses only Python standard library, no additional packages needed

## 📜 License

This project is licensed under the terms included in the LICENSE file.

## 🎉 Credits

Created as a learning project to demonstrate:
- Python programming fundamentals
- Object-oriented design
- Game state management
- User input handling
- Text-based game development

---

**Enjoy your adventure!** 🗡️🛡️⚔️

