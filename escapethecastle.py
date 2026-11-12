#Welcome the player
print("=== ESCAPE THE CASTLE ===")
print("Welcome, adventurer! You find yourself trapped in a mysterious castle. Your goal is to escape by making the right choices. Good luck!")
 
#Get player name, age and character class
playerName = input("What is your name, adventurer? ")
characterClass = input("Choose your character class (Warrior, Mage, Rogue): ")
characterAge = int(input("How old are you, adventurer? "))

#Set starting values
health = 100
gold = 20
hasKey = False
 
#Display the character profile
print(f"\n=== CHARACTER PROFILE ===")
print(f"Name: {playerName}")
print(f"Age: {characterAge}")
print(f"Class: {characterClass}")
print(f"Health: {health}")
print(f"Gold: {gold}")
print(f"Has Key: {hasKey}")
 
#Begin the story
print(f"\n{playerName}, you wake up in a dimly lit room.")
print("Your adventure begins now. What will you do?")

# # ==========================================
# # ESCAPE THE CASTLE - SCENE 1: THE CELL
# # ==========================================
 
# Introduce the scene to the player
print("You wake up in a dimly lit room, as daylight filters through the bars, you see a door, a window and an old bed.")
print("What do you want to investigate?")

# Ask the player what they want to investigate
# .lower() converts their answer to lowercase
choice = input("Enter your choice (door, window, bed): ").lower()

# Check whether the player chose the door
if choice == "door":
    print("You approach the door and try the handle. It's locked.")

# Check whether the player chose the window
elif choice == "window":
    print("You look through the window and see a beautiful garden outside. But it's too high to jump.")
    print("The window is too small to climb through.")

# Check whether the player chose the bed
elif choice == "bed":
    print("You approach the bed and see a small Iron Key hidden under the pillow.")

else:
    print("This item doesn't seem to hide anything.")


# # ==========================================
# # ESCAPE THE CASTLE - SCENE 2: THE CORRIDOR
# # ==========================================

# Create a list to store the player's inventory
# We are assuming the player already found the Iron Key
inventory = ["Iron Key"]

# Introduce the scene
print("You enter a long, dark corridor.")
print("You notice an old wooden door with a strange symbol on it.")

choice = input("Do you want to try to open the door? yes/no: ").lower()

if choice == "yes":
    print("You try to open the door.")
    print("Inside, you find a rusty sword and a small pouch of gold coins.")
    print("You open the pouch and find 20 gold coins inside.")

    inventory.append("Rusty Sword")
    inventory.append("20 Gold Coins")

    print("You pick up the rusty sword and the pouch of gold coins.")

elif choice == "no":
    print("You decide to leave the door alone and continue down the corridor.")

print(f"\n Your inventory: {inventory}")


# ==========================================
# ESCAPE THE CASTLE - SCENE 3: THE ROOM
# ==========================================

def encounter(creature):
 
    print(f"\nA {creature} appears!")
 
    
    if creature == "Guard":
        print("The guard draws their sword!")
 
    elif creature == "Ghost":
        print("The ghost floats towards you!")
    elif creature == "draugr":
        print("the draugr wakes up and slowly walks towards you")


encounter("Guard")
encounter("Ghost")
encounter("draugr")


# ==========================================
# ESCAPE THE CASTLE - CORRIDOR ENCOUNTER
# ==========================================

import random

def encounter(creature):
 
    
    if creature == "Guard":
        print("The guard draws their sword!")
 
    elif creature == "Ghost":
        print("A ghost floats towards you!")
    elif creature == "draugr":
        print("the draugr wakes up and slowly walks towards you")

    print(f"A {creature} appears!!!")


def corridor():
    print("You walk down a dark castle corridor")
    print("You hear a strange noise ahead...")

    creatures = ["Guard", "Ghost", "Draugr"]

    random_creature = random.choice(creatures)
    encounter(random_creature)

corridor()
